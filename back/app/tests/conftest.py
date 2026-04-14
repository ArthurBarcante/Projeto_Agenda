from __future__ import annotations

import sys
from datetime import date
from itertools import count
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[3]
BACK_DIR = ROOT_DIR / "back"

if str(BACK_DIR) not in sys.path:
    sys.path.insert(0, str(BACK_DIR))

from app.core.security import hash_password
from app.core.security import create_access_token
from app.database.base import Base
from app.database.deps import get_db
from app.main import create_app
from app.modules.events.model import Event
from app.modules.tasks.model import Task
from app.modules.users.model import User


@pytest.fixture(scope="session")
def db_engine(tmp_path_factory: pytest.TempPathFactory):
    db_file = tmp_path_factory.mktemp("database") / "test.sqlite3"
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )
    session = testing_session_local()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def app(db_session: Session):
    application = create_app(init_database_on_startup=False)

    def override_get_db():
        yield db_session

    application.dependency_overrides[get_db] = override_get_db
    yield application
    application.dependency_overrides.clear()


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def make_user_payload():
    sequence = count(1)

    def _make_user_payload(**overrides):
        index = next(sequence)
        payload = {
            "name": f"Usuario {index}",
            "email": f"usuario{index}@example.com",
            "password": "SenhaSegura123",
            "confirm_password": "SenhaSegura123",
            "phone": f"1199999{index:04d}",
            "cpf": f"{index:011d}",
            "birthdate": "2000-01-01",
            "role": "user",
        }
        payload.update(overrides)
        return payload

    return _make_user_payload


@pytest.fixture
def valid_user_payload(make_user_payload):
    return make_user_payload()


@pytest.fixture
def create_user(db_session: Session, make_user_payload):
    def _create_user(**overrides):
        payload = make_user_payload(**overrides)
        user = User(
            name=payload["name"],
            email=payload["email"],
            password=hash_password(payload["password"]),
            phone=payload["phone"],
            cpf=payload["cpf"],
            birthdate=date.fromisoformat(payload["birthdate"]),
            role=payload["role"],
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user, payload

    return _create_user


@pytest.fixture
def auth_headers(create_user):
    def _auth_headers(**overrides):
        user, _ = create_user(**overrides)
        token = create_access_token(data={"sub": str(user.id)})
        return {"Authorization": f"Bearer {token}"}, user

    return _auth_headers