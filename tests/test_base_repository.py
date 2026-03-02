from types import SimpleNamespace

import pytest

from app.repositories import BaseRepository


class FakeColumn:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return ("eq", self.name, other)


class TenantModel:
    company_id = FakeColumn("company_id")


class NonTenantModel:
    pass


class FakeQuery:
    def __init__(self, model):
        self.model = model
        self.filters = []

    def filter(self, *conditions):
        self.filters.extend(conditions)
        return self


class FakeSession:
    def __init__(self):
        self.last_query = None

    def query(self, model):
        self.last_query = FakeQuery(model)
        return self.last_query


def test_query_starts_with_tenant_filter():
    db = FakeSession()
    company = SimpleNamespace(id="company-123")

    repository = BaseRepository(db=db, model=TenantModel, current_company=company)
    query = repository.query()

    assert query is db.last_query
    assert query.model is TenantModel
    assert query.filters == [("eq", "company_id", "company-123")]


def test_query_raises_for_model_without_company_id():
    db = FakeSession()
    company = SimpleNamespace(id="company-123")

    repository = BaseRepository(db=db, model=NonTenantModel, current_company=company)

    with pytest.raises(AttributeError, match="does not define company_id"):
        repository.query()
