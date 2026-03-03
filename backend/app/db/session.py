from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, with_loader_criteria
from sqlalchemy import event

from app.core.config import settings
from app.core.tenant import clear_current_company_id, get_current_company_id

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def _is_tenant_scoped_entity(entity: type) -> bool:
    return bool(getattr(entity, "__tenant_scoped__", False) and hasattr(entity, "company_id"))


@event.listens_for(SessionLocal, "do_orm_execute")
def _enforce_tenant_scope(execute_state):
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
        raise RuntimeError("Tenant context is required for tenant-scoped queries")

    for entity in tenant_entities:
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                entity,
                lambda cls: cls.company_id == current_company_id,
                include_aliases=True,
            )
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        clear_current_company_id()
        db.close()