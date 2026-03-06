from typing import Generic, TypeVar

from sqlalchemy.orm import Query, Session

from app.models.empresa import Empresa

TipoModelo = TypeVar("TipoModelo")


class RepositorioBase(Generic[TipoModelo]):
    def __init__(self, db: Session, model: type[TipoModelo], empresa_atual: Empresa) -> None:
        self.db = db
        self.model = model
        self.empresa_atual = empresa_atual

    def consulta(self) -> Query:
        if not hasattr(self.model, "company_id"):
            raise AttributeError(
                f"Model {self.model.__name__} does not define company_id"
            )

        return self.db.query(self.model).filter(
            getattr(self.model, "company_id") == self.empresa_atual.id
        )


class BaseRepository(RepositorioBase[TipoModelo]):
    def __init__(self, db: Session, model: type[TipoModelo], current_company: Empresa) -> None:
        super().__init__(db=db, model=model, empresa_atual=current_company)

    def query(self) -> Query:
        return self.consulta()
