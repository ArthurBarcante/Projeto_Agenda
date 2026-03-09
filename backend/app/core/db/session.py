from sqlalchemy.orm import with_loader_criteria

from app.core.tenant import get_current_company_id

SessionLocal = None


def get_db():
    from app.core.db.session_scope import get_db as get_db_session_scope

    yield from get_db_session_scope()


def _is_tenant_scoped_entity(entity: type) -> bool:
    return bool(getattr(entity, "__tenant_scoped__", False) and hasattr(entity, "company_id"))


def _enforce_tenant_scope(execute_state) -> None:
    if not execute_state.is_select:
        return

    statement = execute_state.statement
    entities = [
        description.get("entity")
        for description in statement.column_descriptions
        if description.get("entity") is not None
    ]

    tenant_entities = [entity for entity in entities if _is_tenant_scoped_entity(entity)]
    if not tenant_entities:
        return

    current_company_id = get_current_company_id()
    if current_company_id is None:
        raise RuntimeError("Tenant context is required")

    for entity in tenant_entities:
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                entity,
                lambda cls: cls.company_id == current_company_id,
                include_aliases=True,
            )
        )
