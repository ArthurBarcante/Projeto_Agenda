from typing import Generic, TypeVar

from sqlalchemy.orm import Query, Session

from app.models.company import Company

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session, model: type[ModelType], current_company: Company) -> None:
        self.db = db
        self.model = model
        self.current_company = current_company

    def query(self) -> Query:
        if not hasattr(self.model, "company_id"):
            raise AttributeError(
                f"Model {self.model.__name__} does not define company_id for tenant scope"
            )

        return self.db.query(self.model).filter(
            getattr(self.model, "company_id") == self.current_company.id
        )
