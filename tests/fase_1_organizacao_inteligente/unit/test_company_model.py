from sqlalchemy import Boolean, Enum as SAEnum, String

from app.modules.users.models.company import Company, CompanyPlan


def test_company_plan_enum_values():
    assert [plan.value for plan in CompanyPlan] == ["free", "pro", "enterprise"]


def test_company_table_columns_and_constraints():
    columns = Company.__table__.c

    assert columns.name.nullable is False
    assert isinstance(columns.name.type, String)
    assert columns.name.type.length == 150

    assert columns.slug.nullable is False
    assert columns.slug.unique is True
    assert isinstance(columns.slug.type, String)
    assert columns.slug.type.length == 150

    assert columns.plan.nullable is False
    assert isinstance(columns.plan.type, SAEnum)
    assert columns.plan.type.name == "company_plan_enum"
    assert columns.plan.type.enums == [plan.name for plan in CompanyPlan]

    assert columns.is_active.nullable is False
    assert isinstance(columns.is_active.type, Boolean)


def test_company_is_active_default_is_true():
    default = Company.__table__.c.is_active.default

    assert default is not None
    assert default.arg is True
