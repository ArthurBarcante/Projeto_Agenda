from typing import Optional
from uuid import UUID

from app.core.tenant.tenant_context import clear_tenant, get_tenant, set_tenant


def definir_empresa_atual_id(empresa_id: UUID | str) -> None:
    set_tenant(empresa_id)


def obter_empresa_atual_id() -> Optional[UUID]:
    return get_tenant()


def limpar_empresa_atual_id() -> None:
    clear_tenant()
