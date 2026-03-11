from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.outbox.models.idempotency_key import IdempotencyKey, IdempotencyState
from app.core.db.repositories import BaseRepository


class IdempotencyRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def buscar_por_chave(self, company_id: UUID, key: str) -> IdempotencyKey | None:
        """Busca registro de idempotência por chave, independente do estado."""
        return (
            self.query(IdempotencyKey)
            .filter(
                IdempotencyKey.company_id == company_id,
                IdempotencyKey.key == key,
            )
            .first()
        )

    def buscar_por_chave_e_estado(
        self, company_id: UUID, key: str, state: IdempotencyState
    ) -> IdempotencyKey | None:
        """Busca registro filtrando também pelo estado."""
        return (
            self.query(IdempotencyKey)
            .filter(
                IdempotencyKey.company_id == company_id,
                IdempotencyKey.key == key,
                IdempotencyKey.state == state,
            )
            .first()
        )

    def reivindicar_chave(
        self,
        company_id: UUID,
        key: str,
        endpoint: str,
        metodo: str,
        request_hash: str,
    ) -> tuple[bool, IdempotencyKey | None]:
        """
        Tenta reivindicar uma chave inserindo um registro com estado IN_PROGRESS.
        
        Retorna:
            (True, registro): Se conseguiu reivindicar (primeiro a inserir)
            (False, registro_existente): Se chave já existe (outro reivindica ou completo)
        """
        try:
            registro = IdempotencyKey(
                company_id=company_id,
                key=key,
                endpoint=endpoint,
                method=metodo,
                request_hash=request_hash,
                state=IdempotencyState.IN_PROGRESS,
                response_body=None,
                status_code=None,
            )
            self.add(registro)
            self.commit()
            self.refresh(registro)
            return True, registro
        except Exception:
            # Constraint violation: chave já existe
            self.db.rollback()
            registro_existente = self.buscar_por_chave(company_id=company_id, key=key)
            return False, registro_existente

    def atualizar_para_completo(
        self,
        company_id: UUID,
        key: str,
        response_body: dict[str, Any],
        status_code: int,
    ) -> IdempotencyKey:
        """
        Atualiza o registro de IN_PROGRESS para COMPLETED com a resposta armazenada.
        """
        registro = self.buscar_por_chave(company_id=company_id, key=key)
        if registro is None:
            raise ValueError(f"Registro de idempotência não encontrado: {key}")
        
        registro.state = IdempotencyState.COMPLETED
        registro.response_body = response_body
        registro.status_code = status_code
        registro.updated_at = func.now()
        
        self.add(registro)
        self.commit()
        self.refresh(registro)
        return registro

    def marcar_como_falha(
        self,
        company_id: UUID,
        key: str,
        error_body: dict[str, Any] | None = None,
        status_code: int | None = None,
    ) -> IdempotencyKey:
        """
        Marca o registro como FAILED (operação não completou com sucesso).
        Opcionalmente armazena erro e status_code.
        """
        registro = self.buscar_por_chave(company_id=company_id, key=key)
        if registro is None:
            raise ValueError(f"Registro de idempotência não encontrado: {key}")
        
        registro.state = IdempotencyState.FAILED
        if error_body is not None:
            registro.response_body = error_body
        if status_code is not None:
            registro.status_code = status_code
        registro.updated_at = func.now()
        
        self.add(registro)
        self.commit()
        self.refresh(registro)
        return registro

    def salvar_resposta(
        self,
        company_id: UUID,
        key: str,
        endpoint: str,
        metodo: str,
        request_hash: str,
        response_body: dict[str, Any],
        status_code: int,
    ) -> IdempotencyKey:
        """
        (Legado) Salva resposta diretamente com estado COMPLETED.
        Mantido para compatibilidade.
        """
        registro = IdempotencyKey(
            company_id=company_id,
            key=key,
            endpoint=endpoint,
            method=metodo,
            request_hash=request_hash,
            response_body=response_body,
            status_code=status_code,
            state=IdempotencyState.COMPLETED,
        )
        self.add(registro)
        self.commit()
        self.refresh(registro)
        return registro
