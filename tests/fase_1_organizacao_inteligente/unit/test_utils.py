from app.core.errors.api_error import APIError
from app.core.errors.error_codes import ErrorCode
from app.core.security import token_jwt


def test_api_error_to_dict_has_expected_shape():
    error = APIError(
        codigo=ErrorCode.VALIDATION_FAILED,
        mensagem="Invalid payload",
        status_code=422,
    )

    payload = error.to_dict()

    assert payload["erro"]["codigo"] == "VALIDATION_FAILED"
    assert payload["erro"]["mensagem"] == "Invalid payload"
    assert payload["erro"]["timestamp"].endswith("Z")


def test_token_create_and_decode_round_trip(monkeypatch):
    monkeypatch.setattr(token_jwt.settings, "SECRET_KEY", "test-secret")
    monkeypatch.setattr(token_jwt.settings, "ALGORITHM", "HS256")
    monkeypatch.setattr(token_jwt.settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 5)

    token = token_jwt.criar_token_acesso({"sub": "user-1", "company_id": "tenant-1"})
    payload = token_jwt.decode_token(token)

    assert payload["sub"] == "user-1"
    assert payload["company_id"] == "tenant-1"
    assert "exp" in payload
