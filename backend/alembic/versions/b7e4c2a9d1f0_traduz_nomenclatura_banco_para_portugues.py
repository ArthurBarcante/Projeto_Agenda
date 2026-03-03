"""traduz nomenclatura banco para portugues

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
    _rename_table_if_exists("companies", "empresas")
    _rename_table_if_exists("users", "usuarios")
    _rename_table_if_exists("appointments", "compromissos")
    _rename_table_if_exists("appointment_participants", "participantes_compromissos")

    _rename_column_if_exists("empresas", "name", "nome")
    _rename_column_if_exists("empresas", "slug", "identificador")
    _rename_column_if_exists("empresas", "plan", "plano")
    _rename_column_if_exists("empresas", "is_active", "ativo")

    _rename_column_if_exists("usuarios", "company_id", "empresa_id")
    _rename_column_if_exists("usuarios", "name", "nome")
    _rename_column_if_exists("usuarios", "password_hash", "hash_senha")
    _rename_column_if_exists("usuarios", "is_active", "ativo")

    _rename_column_if_exists("compromissos", "company_id", "empresa_id")
    _rename_column_if_exists("compromissos", "creator_id", "criador_id")
    _rename_column_if_exists("compromissos", "title", "titulo")
    _rename_column_if_exists("compromissos", "description", "descricao")
    _rename_column_if_exists("compromissos", "starts_at", "inicio_em")
    _rename_column_if_exists("compromissos", "ends_at", "fim_em")
    _rename_column_if_exists("compromissos", "status", "estado")

    _rename_column_if_exists("participantes_compromissos", "company_id", "empresa_id")
    _rename_column_if_exists("participantes_compromissos", "appointment_id", "compromisso_id")
    _rename_column_if_exists("participantes_compromissos", "user_id", "usuario_id")

    _rename_constraint_if_exists(
        "usuarios",
        "uq_user_company_email",
        "uq_usuario_empresa_email",
    )
    _rename_constraint_if_exists(
        "participantes_compromissos",
        "uq_appointment_user",
        "uq_participante_compromisso_usuario",
    )

    _rename_index_if_exists(
        "compromissos",
        "ix_appointments_company_starts_ends_status",
        "ix_compromissos_empresa_inicio_fim_status",
    )
    _rename_index_if_exists(
        "participantes_compromissos",
        "ix_appointment_participants_user_appointment",
        "ix_participantes_compromissos_usuario_compromisso",
    )


def downgrade() -> None:
    _rename_index_if_exists(
        "compromissos",
        "ix_compromissos_empresa_inicio_fim_status",
        "ix_appointments_company_starts_ends_status",
    )
    _rename_index_if_exists(
        "participantes_compromissos",
        "ix_participantes_compromissos_usuario_compromisso",
        "ix_appointment_participants_user_appointment",
    )

    _rename_constraint_if_exists(
        "usuarios",
        "uq_usuario_empresa_email",
        "uq_user_company_email",
    )
    _rename_constraint_if_exists(
        "participantes_compromissos",
        "uq_participante_compromisso_usuario",
        "uq_appointment_user",
    )

    _rename_column_if_exists("empresas", "nome", "name")
    _rename_column_if_exists("empresas", "identificador", "slug")
    _rename_column_if_exists("empresas", "plano", "plan")
    _rename_column_if_exists("empresas", "ativo", "is_active")

    _rename_column_if_exists("usuarios", "empresa_id", "company_id")
    _rename_column_if_exists("usuarios", "nome", "name")
    _rename_column_if_exists("usuarios", "hash_senha", "password_hash")
    _rename_column_if_exists("usuarios", "ativo", "is_active")

    _rename_column_if_exists("compromissos", "empresa_id", "company_id")
    _rename_column_if_exists("compromissos", "criador_id", "creator_id")
    _rename_column_if_exists("compromissos", "titulo", "title")
    _rename_column_if_exists("compromissos", "descricao", "description")
    _rename_column_if_exists("compromissos", "inicio_em", "starts_at")
    _rename_column_if_exists("compromissos", "fim_em", "ends_at")
    _rename_column_if_exists("compromissos", "estado", "status")

    _rename_column_if_exists("participantes_compromissos", "empresa_id", "company_id")
    _rename_column_if_exists("participantes_compromissos", "compromisso_id", "appointment_id")
    _rename_column_if_exists("participantes_compromissos", "usuario_id", "user_id")

    _rename_table_if_exists("participantes_compromissos", "appointment_participants")
    _rename_table_if_exists("compromissos", "appointments")
    _rename_table_if_exists("usuarios", "users")
    _rename_table_if_exists("empresas", "companies")
