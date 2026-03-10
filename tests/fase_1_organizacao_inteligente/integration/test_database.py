from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from uuid import uuid4

from app.core.db.repositories.base_repository import BaseRepository
from app.core.db import session_scope
from app.core.tenant_scope import set_current_company_id


class _Base(DeclarativeBase):
    pass


class _Entity(_Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


def test_base_repository_crud_flow():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    _Base.metadata.create_all(engine)

    db = Session()
    repo = BaseRepository(db)

    entity = _Entity(name="first")
    repo.add(entity)
    repo.commit()
    repo.refresh(entity)

    fetched = repo.query(_Entity).filter(_Entity.id == entity.id).first()
    assert fetched is not None
    assert fetched.name == "first"

    fetched.name = "updated"
    repo.commit()

    updated = repo.query(_Entity).filter(_Entity.id == entity.id).first()
    assert updated.name == "updated"

    db.delete(updated)
    repo.commit()

    deleted = repo.query(_Entity).filter(_Entity.id == entity.id).first()
    assert deleted is None


def test_get_db_clears_tenant_and_closes_session(monkeypatch):
    class FakeDB:
        closed = False

        def close(self):
            self.closed = True

    fake_db = FakeDB()
    monkeypatch.setattr(session_scope, "SessionLocal", lambda: fake_db)

    set_current_company_id(uuid4())
    generator = session_scope.get_db()

    yielded = next(generator)
    assert yielded is fake_db

    try:
        next(generator)
    except StopIteration:
        pass

    assert fake_db.closed is True
