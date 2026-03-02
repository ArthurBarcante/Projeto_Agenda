from types import SimpleNamespace
from uuid import UUID

import pytest
from sqlalchemy import select

from app.core.tenant import clear_current_company_id, set_current_company_id
from app.db import session as session_module
from app.models.company import Company
from app.models.user import User


def test_tenant_scoped_query_requires_tenant_context():
    clear_current_company_id()
    execute_state = SimpleNamespace(is_select=True, statement=select(User))

    with pytest.raises(RuntimeError, match="Tenant context is required"):
        session_module._enforce_tenant_scope(execute_state)


def test_tenant_scoped_query_gets_automatic_company_filter():
    set_current_company_id(UUID("00000000-0000-0000-0000-000000000111"))
    execute_state = SimpleNamespace(is_select=True, statement=select(User))

    session_module._enforce_tenant_scope(execute_state)
    sql = str(execute_state.statement)

    assert "users.company_id" in sql
    clear_current_company_id()


def test_non_tenant_scoped_query_does_not_require_context():
    clear_current_company_id()
    execute_state = SimpleNamespace(is_select=True, statement=select(Company))

    session_module._enforce_tenant_scope(execute_state)
