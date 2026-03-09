from app.core.tenant.tenant_context import clear_tenant, get_tenant, set_tenant


def set_current_company_id(company_id):
    set_tenant(company_id)


def get_current_company_id():
    return get_tenant()


def clear_current_company_id() -> None:
    clear_tenant()
