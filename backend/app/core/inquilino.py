from contextvars import ContextVar
from typing import Optional
from uuid import UUID

_empresa_atual_id: ContextVar[Optional[UUID]] = ContextVar(
    "empresa_atual_id", default=None
)


def definir_empresa_atual_id(empresa_id: UUID | str) -> None:
    if isinstance(empresa_id, str):
        empresa_id = UUID(empresa_id)
    _empresa_atual_id.set(empresa_id)


def obter_empresa_atual_id() -> Optional[UUID]:
    return _empresa_atual_id.get()


def limpar_empresa_atual_id() -> None:
    _empresa_atual_id.set(None)
