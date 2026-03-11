from types import SimpleNamespace
from uuid import uuid4

from app.api.routers import auth as auth_router
from app.core.db.session_scope import get_db
from app.dependencies import fastapi as dependencies
from app.modules.users.models.company import Company
from tests.fixtures import AuthDBStub


def _payload(company_identifier: str = "acme", email: str = "user@acme.com", senha: str = "123456"):
    return {
        "company_identifier": company_identifier,
        "email": email,
        "senha": senha,
    }


def test_auth_login_returns_token_when_credentials_are_valid(client, monkeypatch):
    company = SimpleNamespace(id=uuid4(), slug="acme")
    user = SimpleNamespace(id=uuid4(), company_id=company.id, email="user@acme.com", password_hash="hash")

    monkeypatch.setattr(auth_router, "verificar_senha", lambda plain, hashed: True)
    monkeypatch.setattr(auth_router, "criar_token_acesso", lambda dados: "fake-jwt")

    def override_db():
        yield AuthDBStub(company=company, user=user)

    from app.main import app

    app.dependency_overrides[get_db] = override_db

    response = client().post("/auth/login", json=_payload())

    assert response.status_code == 200
    assert response.json() == {"token_acesso": "fake-jwt", "tipo_token": "bearer"}


def test_auth_login_returns_401_when_company_does_not_exist(client):
    def override_db():
        yield AuthDBStub(company=None, user=None)

    from app.main import app

    app.dependency_overrides[get_db] = override_db

    response = client().post("/auth/login", json=_payload(company_identifier="missing"))

    assert response.status_code == 401
    assert response.json()["erro"]["mensagem"] == "Credentials invalids"


def test_auth_login_returns_401_when_password_is_invalid(client, monkeypatch):
    company = SimpleNamespace(id=uuid4(), slug="acme")
    user = SimpleNamespace(id=uuid4(), company_id=company.id, email="user@acme.com", password_hash="hash")

    monkeypatch.setattr(auth_router, "verificar_senha", lambda plain, hashed: False)

    def override_db():
        yield AuthDBStub(company=company, user=user)

    from app.main import app

    app.dependency_overrides[get_db] = override_db

    response = client().post("/auth/login", json=_payload())

    assert response.status_code == 401
    assert response.json()["erro"]["mensagem"] == "Credentials invalids"


def test_auth_login_returns_422_for_invalid_email(client):
    response = client().post(
        "/auth/login",
        json={"company_identifier": "acme", "email": "invalid", "senha": "123"},
    )

    assert response.status_code == 422
    assert response.json()["erro"]["codigo"] == "VALIDATION_FAILED"


def test_me_route_returns_current_user_identifiers(client, current_user_factory):
    current_user = current_user_factory()

    def override_current_user():
        return current_user

    from app.main import app

    app.dependency_overrides[dependencies.get_current_user] = override_current_user

    response = client().get("/me")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": str(current_user.id),
        "company_id": str(current_user.company_id),
    }
