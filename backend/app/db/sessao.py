from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, with_loader_criteria
from sqlalchemy import event

from app.core.config import settings
from app.core.inquilino import limpar_empresa_atual_id, obter_empresa_atual_id

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

SessaoLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def _eh_entidade_escopo_inquilino(entidade: type) -> bool:
    return bool(getattr(entity, "__tenant_scoped__", False) and hasattr(entity, "company_id"))


@event.listens_for(SessaoLocal, "do_orm_execute")
def _aplicar_escopo_inquilino(estado_execucao):
    if not estado_execucao.is_select:
        return

    declaracao = estado_execucao.statement
    entidades = [
        descricao.get("entity")
        for descricao in declaracao.column_descriptions
        if descricao.get("entity") is not None
    ]

    entidades_inquilino = [entidade for entidade in entidades if _eh_entidade_escopo_inquilino(entidade)]
    if not entidades_inquilino:
        return

    empresa_atual_id = obter_empresa_atual_id()
    if empresa_atual_id is None:
        raise RuntimeError("Contexto de inquilino é obrigatório para consultas com escopo")

    for entidade in entidades_inquilino:
        estado_execucao.statement = estado_execucao.statement.options(
            with_loader_criteria(
                entidade,
                lambda cls: cls.company_id == empresa_atual_id,
                include_aliases=True,
            )
        )


def obter_db():
    db = SessaoLocal()
    try:
        yield db
    finally:
        limpar_empresa_atual_id()
        db.close()