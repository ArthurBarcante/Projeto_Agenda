from contextvars import ContextVar
from typing import Optional
from uuid import UUID

_current_company_id: ContextVar[Optional[UUID]] = ContextVar(
    "current_company_id", default=None
)


def set_current_company_id(company_id: UUID | str) -> None:
    if isinstance(company_id, str):
        company_id = UUID(company_id)
    _current_company_id.set(company_id)


def get_current_company_id() -> Optional[UUID]:
    return _current_company_id.get()


def clear_current_company_id() -> None:
    _current_company_id.set(None)
