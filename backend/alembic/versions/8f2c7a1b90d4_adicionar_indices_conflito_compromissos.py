"""adicionar indices de conflito de compromissos

Revision ID: 8f2c7a1b90d4
Revises: 3afa394c9de8
Create Date: 2026-03-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8f2c7a1b90d4"
down_revision: Union[str, Sequence[str], None] = "3afa394c9de8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conexao = op.get_bind()
    inspetor = sa.inspect(conexao)
    tabelas = set(inspetor.get_table_names())

    if "appointments" in tabelas:
        op.create_index(
            "ix_appointments_company_starts_ends_status",
            "appointments",
            ["company_id", "starts_at", "ends_at", "status"],
            unique=False,
        )

    if "compromissos" in tabelas:
        op.create_index(
            "ix_compromissos_empresa_inicio_fim_status",
            "compromissos",
            ["empresa_id", "inicio_em", "fim_em", "estado"],
            unique=False,
        )

    if "appointment_participants" in tabelas:
        op.create_index(
            "ix_appointment_participants_user_appointment",
            "appointment_participants",
            ["user_id", "appointment_id"],
            unique=False,
        )

    if "participantes_compromissos" in tabelas:
        op.create_index(
            "ix_participantes_compromissos_usuario_compromisso",
            "participantes_compromissos",
            ["usuario_id", "compromisso_id"],
            unique=False,
        )


def downgrade() -> None:
    conexao = op.get_bind()
    inspetor = sa.inspect(conexao)
    tabelas = set(inspetor.get_table_names())

    if "appointment_participants" in tabelas:
        indices_participantes = {
            index["name"]
            for index in inspetor.get_indexes("appointment_participants")
        }
        if "ix_appointment_participants_user_appointment" in indices_participantes:
            op.drop_index(
                "ix_appointment_participants_user_appointment",
                table_name="appointment_participants",
            )

    if "participantes_compromissos" in tabelas:
        indices_participantes = {
            index["name"]
            for index in inspetor.get_indexes("participantes_compromissos")
        }
        if "ix_participantes_compromissos_usuario_compromisso" in indices_participantes:
            op.drop_index(
                "ix_participantes_compromissos_usuario_compromisso",
                table_name="participantes_compromissos",
            )

    if "appointments" in tabelas:
        indices_compromissos = {
            index["name"]
            for index in inspetor.get_indexes("appointments")
        }
        if "ix_appointments_company_starts_ends_status" in indices_compromissos:
            op.drop_index(
                "ix_appointments_company_starts_ends_status",
                table_name="appointments",
            )

    if "compromissos" in tabelas:
        indices_compromissos = {
            index["name"]
            for index in inspetor.get_indexes("compromissos")
        }
        if "ix_compromissos_empresa_inicio_fim_status" in indices_compromissos:
            op.drop_index(
                "ix_compromissos_empresa_inicio_fim_status",
                table_name="compromissos",
            )
