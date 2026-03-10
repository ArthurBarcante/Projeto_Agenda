from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.errors.error_handlers import register_error_handlers
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.core.rate_limit import rate_limit_service
from app.middleware.tenant_middleware import TenantContextMiddleware


class _RedisFalso:
    def __init__(self):
        self._store: dict[str, int] = {}

    async def incr(self, key: str) -> int:
        valor = self._store.get(key, 0) + 1
        self._store[key] = valor
        return valor

    async def expire(self, key: str, _: int) -> bool:
        return key in self._store


def _criar_app_teste() -> FastAPI:
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(TenantContextMiddleware)
    register_error_handlers(app)

    @app.get("/ok")
    def ok():
        return {"ok": True}

    return app


def test_rate_limit_por_tenant_retorna_429_apos_exceder_limite(monkeypatch):
    company_id = uuid4()
    limite = 3

    monkeypatch.setattr(
        "app.middleware.tenant_middleware.decode_token",
        lambda _token: {"tenant_id": str(company_id)},
    )
    monkeypatch.setattr(
        rate_limit_service.settings,
        "RATE_LIMIT_REQUESTS_PER_MINUTE",
        limite,
    )

    redis_falso = _RedisFalso()
    monkeypatch.setattr(rate_limit_service, "_obter_redis_client", lambda: redis_falso)

    app = _criar_app_teste()
    client = TestClient(app, raise_server_exceptions=False)
    headers = {"Authorization": "Bearer token-valido"}

    for _ in range(limite):
        resposta = client.get("/ok", headers=headers)
        assert resposta.status_code == 200

    resposta_limite = client.get("/ok", headers=headers)

    assert resposta_limite.status_code == 429
    corpo = resposta_limite.json()
    assert corpo["erro"]["codigo"] == "RATE_LIMIT_EXCEEDED"
    assert corpo["erro"]["mensagem"] == "Limite de requests por minuto excedido."
