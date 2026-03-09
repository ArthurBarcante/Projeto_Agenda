import hashlib
import json
from typing import Any
from uuid import UUID

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.idempotency.repositories.idempotency_repository import IdempotencyRepository


class IdempotencyService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = IdempotencyRepository(db)

    @staticmethod
    def _obter_chave(request: Request) -> str | None:
        key = request.headers.get("Idempotency-Key")
        if key is None:
            return None

        chave_normalizada = key.strip()
        return chave_normalizada or None

    async def _calcular_request_hash(self, request: Request) -> str:
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

    async def verificar_idempotencia(
        self,
        request: Request,
        company_id: UUID,
    ) -> JSONResponse | None:
        key = self._obter_chave(request)
        if key is None:
            return None

        request_hash = await self._calcular_request_hash(request)
        request.state.idempotency_key = key
        request.state.idempotency_hash = request_hash

        registro = self.repository.buscar_por_chave(company_id=company_id, key=key)
        if registro is None:
            return None

        if registro.request_hash != request_hash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Idempotency-Key already used com payload diferente",
            )

        return JSONResponse(
            content=registro.response_body,
            status_code=registro.status_code,
        )

    async def registrar_resposta(
        self,
        request: Request,
        company_id: UUID,
        response_body: dict[str, Any],
        status_code: int,
    ) -> None:
        key = getattr(request.state, "idempotency_key", None) or self._obter_chave(request)
        if key is None:
            return

        request_hash = getattr(request.state, "idempotency_hash", None)
        if request_hash is None:
            request_hash = await self._calcular_request_hash(request)

        endpoint = request.url.path
        metodo = request.method

        try:
            self.repository.salvar_resposta(
                company_id=company_id,
                key=key,
                endpoint=endpoint,
                metodo=metodo,
                request_hash=request_hash,
                response_body=response_body,
                status_code=status_code,
            )
        except IntegrityError:
            self.db.rollback()
            registro_existente = self.repository.buscar_por_chave(company_id=company_id, key=key)
            if registro_existente is None:
                raise
            if registro_existente.request_hash != request_hash:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Idempotency-Key already used com payload diferente",
                )
