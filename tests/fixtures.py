from collections.abc import Callable
from dataclasses import dataclass
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app


class _QueryStub:
    def __init__(self, result):
        self._result = result

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self._result


@dataclass
class AuthDBStub:
    company: object | None
    user: object | None

    def query(self, model):
        model_name = getattr(model, "__name__", "")
        if model_name == "Company":
            return _QueryStub(self.company)
        return _QueryStub(self.user)


@pytest.fixture
def client() -> Callable[[], TestClient]:
    created_clients: list[TestClient] = []

    def _factory() -> TestClient:
        instance = TestClient(app)
        created_clients.append(instance)
        return instance

    yield _factory

    for instance in created_clients:
        instance.close()
    app.dependency_overrides.clear()


@pytest.fixture
def current_user_factory():
    def _factory():
        return SimpleNamespace(id=uuid4(), company_id=uuid4())

    return _factory
