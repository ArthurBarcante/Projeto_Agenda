from app.core.security import create_access_token, verify_password
from app.modules.users.model import User


def test_register_creates_user_with_hashed_password(client, db_session, valid_user_payload):
    response = client.post("/auth/register", json=valid_user_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Usuário criado com sucesso"
    assert body["user"]["email"] == valid_user_payload["email"]

    created_user = db_session.query(User).filter(User.email == valid_user_payload["email"]).first()
    assert created_user is not None
    assert created_user.password != valid_user_payload["password"]
    assert verify_password(valid_user_payload["password"], str(created_user.password))
    assert "confirm_password" not in User.__table__.columns.keys()
    assert not hasattr(created_user, "confirm_password")


def test_register_rejects_duplicate_email(client, create_user, make_user_payload):
    existing_user, _ = create_user()
    payload = make_user_payload(email=existing_user.email)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "Email já cadastrado"}


def test_register_rejects_duplicate_cpf(client, create_user, make_user_payload):
    existing_user, _ = create_user()
    payload = make_user_payload(cpf=existing_user.cpf)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "CPF já cadastrado"}


def test_register_rejects_password_confirmation_mismatch(client, make_user_payload):
    payload = make_user_payload(confirm_password="SenhaDiferente123")

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("As senhas não coincidem" in error["msg"] for error in errors)


def test_login_returns_bearer_token_for_valid_credentials(client, create_user):
    user, payload = create_user()

    response = client.post(
        "/auth/login",
        json={"email": user.email, "password": payload["password"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]


def test_login_rejects_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={"email": "inexistente@example.com", "password": "SenhaSegura123"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Email ou senha inválidos"}


def test_login_rejects_wrong_password(client, create_user):
    user, _ = create_user()

    response = client.post(
        "/auth/login",
        json={"email": user.email, "password": "SenhaErrada123"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Email ou senha inválidos"}


def test_auth_me_returns_authenticated_user(client, create_user):
    user, _ = create_user()
    token = create_access_token(data={"sub": str(user.id)})

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"id": user.id, "email": user.email}


def test_auth_me_requires_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_auth_me_rejects_invalid_token(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer token-invalido"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Token invalido"}


def test_auth_me_rejects_token_for_missing_user(client):
    token = create_access_token(data={"sub": "999999"})

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Usuario nao encontrado"}
