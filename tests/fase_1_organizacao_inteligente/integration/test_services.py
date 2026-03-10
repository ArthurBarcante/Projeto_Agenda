import json
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import HTTPException
from starlette.requests import Request
from unittest.mock import MagicMock

from app.modules.idempotency.services.idempotency_service import IdempotencyService
from app.modules.permissions.services.permission_service import PermissionService


def _request_from_body(body: bytes, headers: list[tuple[bytes, bytes]] | None = None) -> Request:
    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    scope = {
        "type": "http",
        "method": "POST",
        "path": "/appointments",
        "headers": headers or [],
    }
    return Request(scope, receive=receive)


def test_permission_service_user_has_permission_returns_true_without_recursion(monkeypatch):
    service = PermissionService(MagicMock())
    monkeypatch.setattr(service, "_query_user_has_permission", lambda **kwargs: True)

    result = service.user_has_permission(user_id=uuid4(), permission_code="agenda.criar")

    assert result is True


@pytest.mark.anyio
async def test_idempotency_hash_is_stable_for_same_json_with_different_key_order():
    service = IdempotencyService(MagicMock())

    request_a = _request_from_body(json.dumps({"a": 1, "b": 2}).encode("utf-8"))
    request_b = _request_from_body(json.dumps({"b": 2, "a": 1}).encode("utf-8"))

    hash_a = await service._calcular_request_hash(request_a)
    hash_b = await service._calcular_request_hash(request_b)

    assert hash_a == hash_b


@pytest.mark.anyio
async def test_idempotency_detects_payload_mismatch_for_same_key():
    db = MagicMock()
    service = IdempotencyService(db)

    existing = SimpleNamespace(request_hash="stored-hash", response_body={"ok": True}, status_code=201)
    service.repository = MagicMock()
    service.repository.buscar_por_chave.return_value = existing

    request = _request_from_body(
        body=b'{"x":1}',
        headers=[(b"idempotency-key", b"same-key")],
    )

    with pytest.raises(HTTPException) as exc:
        await service.verificar_idempotencia(request=request, company_id=uuid4())

    assert exc.value.status_code == 409
