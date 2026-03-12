"""traduz naming banco para portuguese

Revision ID: b7e4c2a9d1f0
Revises: 8f2c7a1b90d4
Create Date: 2026-03-03 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7e4c2a9d1f0"
down_revision: Union[str, Sequence[str], None] = "8f2c7a1b90d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _rename_table_if_exists(old_name: str, new_name: str) -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if old_name in tables and new_name not in tables:
        op.rename_table(old_name, new_name)


def _rename_column_if_exists(table_name: str, old_name: str, new_name: str) -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if table_name not in tables:
        return

    columns = {column["name"] for column in inspector.get_columns(table_name)}
    if old_name in columns and new_name not in columns:
        op.alter_column(table_name, old_name, new_column_name=new_name)


def _rename_constraint_if_exists(table_name: str, old_name: str, new_name: str) -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if table_name not in tables:
        return

    unique_constraints = {
        constraint["name"]
        for constraint in inspector.get_unique_constraints(table_name)
        if constraint.get("name")
    }

    if old_name in unique_constraints and new_name not in unique_constraints:
        op.execute(
            sa.text(
                f'ALTER TABLE "{table_name}" RENAME CONSTRAINT "{old_name}" TO "{new_name}"'
            )
        )


def _rename_index_if_exists(table_name: str, old_name: str, new_name: str) -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if table_name not in tables:
        return

    indexes = {
        index["name"]
        for index in inspector.get_indexes(table_name)
        if index.get("name")
    }

    if old_name in indexes and new_name not in indexes:
        op.execute(sa.text(f'ALTER INDEX "{old_name}" RENAME TO "{new_name}"'))


def upgrade() -> None:
    _rename_table_if_exists("companies", "companies")
    _rename_table_if_exists("users", "users")
    _rename_table_if_exists("appointments", "appointments")
    _rename_table_if_exists("appointment_participants", "appointment_participants")

    _rename_column_if_exists("companies", "name", "nome")
    _rename_column_if_exists("companies", "slug", "identificador")
    _rename_column_if_exists("companies", "plan", "plano")
    _rename_column_if_exists("companies", "is_active", "is_active")

    _rename_column_if_exists("users", "company_id", "company_id")
    _rename_column_if_exists("users", "name", "nome")
    _rename_column_if_exists("users", "password_hash", "hash_senha")
    _rename_column_if_exists("users", "is_active", "is_active")

    _rename_column_if_exists("appointments", "company_id", "company_id")
    _rename_column_if_exists("appointments", "creator_id", "creator_id")
    _rename_column_if_exists("appointments", "title", "title")
    _rename_column_if_exists("appointments", "description", "description")
    _rename_column_if_exists("appointments", "start_time", "start_time")
    _rename_column_if_exists("appointments", "end_time", "end_time")
    _rename_column_if_exists("appointments", "status", "estado")

    _rename_column_if_exists("appointment_participants", "company_id", "company_id")
    _rename_column_if_exists("appointment_participants", "appointment_id", "appointment_id")
    _rename_column_if_exists("appointment_participants", "user_id", "user_id")

    _rename_constraint_if_exists(
        "users",
        "uq_user_company_email",
        "uq_user_company_email",
    )
    _rename_constraint_if_exists(
        "appointment_participants",
        "uq_appointment_user",
        "uq_appointment_participant_user",
    )

    _rename_index_if_exists(
        "appointments",
        "ix_appointments_company_starts_ends_status",
        "ix_appointments_company_start_end_status",
    )
    _rename_index_if_exists(
        "appointment_participants",
        "ix_appointment_participants_user_appointment",
        "ix_appointment_participants_user_appointment",
    )


def downgrade() -> None:
    _rename_index_if_exists(
        "appointments",
        "ix_appointments_company_start_end_status",
        "ix_appointments_company_starts_ends_status",
    )
    _rename_index_if_exists(
        "appointment_participants",
        "ix_appointment_participants_user_appointment",
        "ix_appointment_participants_user_appointment",
    )

    _rename_constraint_if_exists(
        "users",
        "uq_user_company_email",
        "uq_user_company_email",
    )
    _rename_constraint_if_exists(
        "appointment_participants",
        "uq_appointment_participant_user",
        "uq_appointment_user",
    )

    _rename_column_if_exists("companies", "nome", "name")
    _rename_column_if_exists("companies", "identificador", "slug")
    _rename_column_if_exists("companies", "plano", "plan")
    _rename_column_if_exists("companies", "is_active", "is_active")

    _rename_column_if_exists("users", "company_id", "company_id")
    _rename_column_if_exists("users", "nome", "name")
    _rename_column_if_exists("users", "hash_senha", "password_hash")
    _rename_column_if_exists("users", "is_active", "is_active")

    _rename_column_if_exists("appointments", "company_id", "company_id")
    _rename_column_if_exists("appointments", "creator_id", "creator_id")
    _rename_column_if_exists("appointments", "title", "title")
    _rename_column_if_exists("appointments", "description", "description")
    _rename_column_if_exists("appointments", "start_time", "start_time")
    _rename_column_if_exists("appointments", "end_time", "end_time")
    _rename_column_if_exists("appointments", "estado", "status")

    _rename_column_if_exists("appointment_participants", "company_id", "company_id")
    _rename_column_if_exists("appointment_participants", "appointment_id", "appointment_id")
    _rename_column_if_exists("appointment_participants", "user_id", "user_id")

    _rename_table_if_exists("appointment_participants", "appointment_participants")
    _rename_table_if_exists("appointments", "appointments")
    _rename_table_if_exists("users", "users")
    _rename_table_if_exists("companies", "companies")
