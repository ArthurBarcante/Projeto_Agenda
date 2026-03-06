from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.idempotency_key import IdempotencyKey
from app.repositorios.base_repository import BaseRepository


class IdempotencyRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def buscar_por_chave(self, empresa_id: UUID, chave: str) -> IdempotencyKey | None:
        return (
            self.query(IdempotencyKey)
            .filter(
                IdempotencyKey.company_id == empresa_id,
                IdempotencyKey.key == chave,
            )
            .first()
        )

    def salvar_resposta(
        self,
        empresa_id: UUID,
        chave: str,
        endpoint: str,
        metodo: str,
        request_hash: str,
        response_body: dict[str, Any],
        status_code: int,
    ) -> IdempotencyKey:
        registro = IdempotencyKey(
            company_id=empresa_id,
            key=chave,
            endpoint=endpoint,
            method=metodo,
            request_hash=request_hash,
            response_body=response_body,
            status_code=status_code,
        )
        self.add(registro)
        self.commit()
        self.refresh(registro)
        return registro
