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
                f"Modelo {self.model.__name__} não define company_id para escopo de inquilino"
            )

        return self.db.query(self.model).filter(
            getattr(self.model, "company_id") == self.empresa_atual.id
        )
