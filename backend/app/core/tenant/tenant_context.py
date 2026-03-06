from contextvars import ContextVar
from typing import Optional
from uuid import UUID

_tenant_atual_id: ContextVar[Optional[UUID]] = ContextVar("tenant_atual_id", default=None)


def set_tenant(tenant_id: UUID | str) -> None:
    if isinstance(tenant_id, str):
        tenant_id = UUID(tenant_id)
    _tenant_atual_id.set(tenant_id)


def get_tenant() -> Optional[UUID]:
    return _tenant_atual_id.get()


def clear_tenant() -> None:
    _tenant_atual_id.set(None)
