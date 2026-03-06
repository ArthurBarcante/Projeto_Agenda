from sqlalchemy.orm import Query, Session


class BaseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, instance):
        self.db.add(instance)
        return instance

    def add_all(self, instances) -> None:
        self.db.add_all(instances)

    def flush(self) -> None:
        self.db.flush()

    def commit(self) -> None:
        self.db.commit()

    def refresh(self, instance) -> None:
        self.db.refresh(instance)

    def query(self, *entities) -> Query:
        return self.db.query(*entities)
