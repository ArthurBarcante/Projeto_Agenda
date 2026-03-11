import asyncio
import hashlib
import json
import logging
from typing import Any
from uuid import UUID

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.modules.idempotency.repositories.idempotency_repository import IdempotencyRepository
from app.modules.outbox.models.idempotency_key import IdempotencyState


logger = logging.getLogger(__name__)


class IdempotencyService:
    """
    Serviço de orquestração de idempotência com suporte a "claim" atômico.
    
    Fluxo seguro contra condição de corrida:
    1. reivindicar_chave() - tenta INSERT com estado IN_PROGRESS (apenas um sucede)
    2. [executa operação de negócio]
    3. finalizar_resposta() - marca como COMPLETED com resposta
    
    Se outro request tenta a mesma chave durante step 2:
    - Encontra registro em IN_PROGRESS
    - Aguarda com retry até que mude para COMPLETED ou FAILED
    """

    # Constantes de retry para aguardar finalização de operações em andamento
    MAX_RETRIES_IN_PROGRESS = 30  # ~15 segundos com 500ms entre retries
    RETRY_DELAY_SECONDS = 0.5

    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = IdempotencyRepository(db)

    @staticmethod
    def _build_log_context(
        *,
        company_id: UUID,
        idempotency_key: str,
        endpoint: str,
        request_hash: str,
        **extra: Any,
    ) -> dict[str, Any]:
        context: dict[str, Any] = {
            "company_id": str(company_id),
            "idempotency_key": idempotency_key,
            "endpoint": endpoint,
            "request_hash": request_hash,
        }
        context.update(extra)
        return context

    @staticmethod
    def _obter_chave(request: Request) -> str | None:
        """Extrai e normaliza chave de idempotência do header."""
        key = request.headers.get("Idempotency-Key")
        if key is None:
            return None

        chave_normalizada = key.strip()
        return chave_normalizada or None

    async def _calcular_request_hash(self, request: Request) -> str:
        """Calcula hash determinístico do corpo da requisição."""
        corpo = await request.body()

        if not corpo:
            return hashlib.sha256(b"").hexdigest()

        try:
            conteudo_json = json.loads(corpo)
            canonical = json.dumps(
                conteudo_json,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            return hashlib.sha256(canonical).hexdigest()
        except (json.JSONDecodeError, TypeError):
            return hashlib.sha256(corpo).hexdigest()

    async def reivindicar_chave(
        self,
        request: Request,
        company_id: UUID,
    ) -> JSONResponse | None:
        """
        Tenta reivindicar a chave de idempotência com "lock" atômico via INSERT.
        
        Fluxo:
        1. Se sem chave: retorna None (sem idempotência)
        2. Tenta INSERT com estado IN_PROGRESS:
           - Sucesso: Retorna None (caller pode prosseguir com negócio)
           - Falha (constraint): verifica registro existente:
             - COMPLETED: retorna JSONResponse armazenada
             - IN_PROGRESS: aguarda com retry, depois devolve resposta quando finalizar
             - FAILED: faz retry ou lança erro conforme política
        
        Args:
            request: Objeto FastAPI Request
            company_id: ID da empresa (tenant)
            
        Returns:
            None: Chave não existe ou foi reivindicada com sucesso (prosseguir com negócio)
            JSONResponse: Resposta de requisição anterior (cache hit) - retornar ao cliente
            
        Raises:
            HTTPException(409): Hash diferente para mesma chave
            HTTPException(503): Operação anterior falhou e ainda está marcada como FAILED
        """
        key = self._obter_chave(request)
        if key is None:
            return None

        endpoint = request.url.path
        metodo = request.method
        request_hash = await self._calcular_request_hash(request)

        # Salva hash e chave em request.state para uso posterior
        request.state.idempotency_key = key
        request.state.idempotency_hash = request_hash

        # Tenta reivindicar a chave (INSERT com estado IN_PROGRESS)
        sucesso_reivindica, registro = self.repository.reivindicar_chave(
            company_id=company_id,
            key=key,
            endpoint=endpoint,
            metodo=metodo,
            request_hash=request_hash,
        )

        if sucesso_reivindica:
            logger.info(
                "idempotency.atomic_claim.success",
                extra=self._build_log_context(
                    company_id=company_id,
                    idempotency_key=key,
                    endpoint=endpoint,
                    request_hash=request_hash,
                    method=metodo,
                ),
            )
            # Primeiro a reivindicar: prosseguir com negócio
            return None

        logger.info(
            "idempotency.atomic_claim.conflict",
            extra=self._build_log_context(
                company_id=company_id,
                idempotency_key=key,
                endpoint=endpoint,
                request_hash=request_hash,
                method=metodo,
            ),
        )

        # Chave já existe - validar e retornar conforme estado
        if registro is None:
            # Shouldn't happen, mas por segurança
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Chave de idempotência em conflito desconhecido",
            )

        # Validar hash - se diferente, erro 409
        if registro.request_hash != request_hash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Idempotency-Key já usada com payload diferente",
            )

        # Hash igual - processar conforme estado
        if registro.state == IdempotencyState.COMPLETED:
            # Operação anterior completa - retornar resposta armazenada
            logger.info(
                "idempotency.response.replayed",
                extra=self._build_log_context(
                    company_id=company_id,
                    idempotency_key=key,
                    endpoint=endpoint,
                    request_hash=request_hash,
                    state=registro.state.value,
                    status_code=registro.status_code,
                ),
            )
            return JSONResponse(
                content=registro.response_body,
                status_code=registro.status_code,
            )

        elif registro.state == IdempotencyState.IN_PROGRESS:
            # Operação anterior em andamento - aguardar finalização com retry
            return await self._aguardar_conclusao(
                company_id=company_id,
                key=key,
                endpoint=endpoint,
                request_hash=request_hash,
            )

        elif registro.state == IdempotencyState.FAILED:
            # Operação anterior falhou - por política, pode:
            # 1. Tentar reprocessar (remover FAILED)
            # 2. Retornar erro anterior
            # Por questão de segurança, retornamos erro anterior
            logger.warning(
                "idempotency.operation.failed_existing",
                extra=self._build_log_context(
                    company_id=company_id,
                    idempotency_key=key,
                    endpoint=endpoint,
                    request_hash=request_hash,
                    state=registro.state.value,
                    status_code=registro.status_code,
                ),
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Idempotency-Key anterior falhou. Tente novamente.",
            )

        # Estado desconhecido
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Estado desconhecido de idempotência: {registro.state}",
        )

    async def _aguardar_conclusao(
        self,
        company_id: UUID,
        key: str,
        endpoint: str,
        request_hash: str,
    ) -> JSONResponse:
        """
        Aguarda até 15 segundos a conclusão de uma operação em andamento.
        
        Usa retry com pequeno delay entre tentativas para não sobrecarregar DB.
        Se não finalizar em tempo, retorna 503 Service Unavailable.
        """
        logger.info(
            "idempotency.wait_retry.started",
            extra=self._build_log_context(
                company_id=company_id,
                idempotency_key=key,
                endpoint=endpoint,
                request_hash=request_hash,
                max_retries=self.MAX_RETRIES_IN_PROGRESS,
                retry_delay_seconds=self.RETRY_DELAY_SECONDS,
            ),
        )

        for tentativa in range(1, self.MAX_RETRIES_IN_PROGRESS + 1):
            await asyncio.sleep(self.RETRY_DELAY_SECONDS)

            registro = self.repository.buscar_por_chave(
                company_id=company_id,
                key=key,
            )

            if registro is None:
                # Registro desapareceu - erro de estado
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Registro de idempotência perdido durante aguardo",
                )

            if registro.state == IdempotencyState.COMPLETED:
                logger.info(
                    "idempotency.wait_retry.completed",
                    extra=self._build_log_context(
                        company_id=company_id,
                        idempotency_key=key,
                        endpoint=endpoint,
                        request_hash=request_hash,
                        retries=tentativa,
                        final_state=registro.state.value,
                        status_code=registro.status_code,
                    ),
                )
                return JSONResponse(
                    content=registro.response_body,
                    status_code=registro.status_code,
                )

            if registro.state == IdempotencyState.FAILED:
                logger.warning(
                    "idempotency.wait_retry.failed",
                    extra=self._build_log_context(
                        company_id=company_id,
                        idempotency_key=key,
                        endpoint=endpoint,
                        request_hash=request_hash,
                        retries=tentativa,
                        final_state=registro.state.value,
                        status_code=registro.status_code,
                    ),
                )
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Idempotency-Key anterior falhou",
                )

            # IN_PROGRESS: continua aguardando
            continue

        # Timeout: operação anterior não finalizou em tempo
        logger.warning(
            "idempotency.wait_retry.timeout",
            extra=self._build_log_context(
                company_id=company_id,
                idempotency_key=key,
                endpoint=endpoint,
                request_hash=request_hash,
                retries=self.MAX_RETRIES_IN_PROGRESS,
            ),
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Timeout aguardando conclusão de operação anterior (idempotência)",
        )

    async def finalizar_resposta(
        self,
        request: Request,
        company_id: UUID,
        response_body: dict[str, Any],
        status_code: int,
    ) -> None:
        """
        Marca a chave como COMPLETED com a resposta armazenada.
        Deve ser chamado apenas APÓS sucesso da operação de negócio.
        
        Args:
            request: Objeto FastAPI Request
            company_id: ID da empresa (tenant)
            response_body: Corpo da resposta (será armazenado em JSONB)
            status_code: Código HTTP da resposta
        """
        key = getattr(request.state, "idempotency_key", None) or self._obter_chave(request)
        if key is None:
            return

        endpoint = request.url.path
        request_hash = getattr(request.state, "idempotency_hash", None) or await self._calcular_request_hash(request)

        try:
            self.repository.atualizar_para_completo(
                company_id=company_id,
                key=key,
                response_body=response_body,
                status_code=status_code,
            )
            logger.info(
                "idempotency.response.completed",
                extra=self._build_log_context(
                    company_id=company_id,
                    idempotency_key=key,
                    endpoint=endpoint,
                    request_hash=request_hash,
                    status_code=status_code,
                ),
            )
        except ValueError:
            # Registro não encontrado - log/warn mas não falha
            logger.warning(
                "idempotency.response.complete_missing_record",
                extra=self._build_log_context(
                    company_id=company_id,
                    idempotency_key=key,
                    endpoint=endpoint,
                    request_hash=request_hash,
                    status_code=status_code,
                ),
            )

    async def marcar_como_falha(
        self,
        request: Request,
        company_id: UUID,
        error_body: dict[str, Any] | None = None,
        status_code: int | None = None,
    ) -> None:
        """
        Marca a chave como FAILED em caso de erro durante operação.
        Can be called from exception handlers.
        
        Args:
            request: Objeto FastAPI Request
            company_id: ID da empresa (tenant)
            error_body: Corpo do erro (opcional)
            status_code: Código HTTP do erro (opcional)
        """
        key = getattr(request.state, "idempotency_key", None) or self._obter_chave(request)
        if key is None:
            return

        endpoint = request.url.path
        request_hash = getattr(request.state, "idempotency_hash", None) or await self._calcular_request_hash(request)

        try:
            self.repository.marcar_como_falha(
                company_id=company_id,
                key=key,
                error_body=error_body,
                status_code=status_code,
            )
            logger.warning(
                "idempotency.operation.failed",
                extra=self._build_log_context(
                    company_id=company_id,
                    idempotency_key=key,
                    endpoint=endpoint,
                    request_hash=request_hash,
                    status_code=status_code,
                ),
            )
        except ValueError:
            # Registro não encontrado - log/warn mas não falha
            logger.warning(
                "idempotency.operation.failed_missing_record",
                extra=self._build_log_context(
                    company_id=company_id,
                    idempotency_key=key,
                    endpoint=endpoint,
                    request_hash=request_hash,
                    status_code=status_code,
                ),
            )

    # === Métodos legados para compatibilidade (deletar após migrar rotas) ===

    async def verificar_idempotencia(
        self,
        request: Request,
        company_id: UUID,
    ) -> JSONResponse | None:
        """
        (LEGADO) Verificar idempotência sem claim atômico.
        Usar `reivindicar_chave()` no novo código.
        """
        return await self.reivindicar_chave(request, company_id)

    async def registrar_resposta(
        self,
        request: Request,
        company_id: UUID,
        response_body: dict[str, Any],
        status_code: int,
    ) -> None:
        """
        (LEGADO) Registrar resposta sem marcar como COMPLETED de forma clara.
        Usar `finalizar_resposta()` no novo código.
        """
        await self.finalizar_resposta(request, company_id, response_body, status_code)
