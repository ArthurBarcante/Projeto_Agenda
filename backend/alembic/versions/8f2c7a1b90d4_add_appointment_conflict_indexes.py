"""adicionar indices de conflict de appointments

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
            ["company_id", "start_time", "end_time", "status"],
            unique=False,
        )

    if "appointments" in tabelas:
        op.create_index(
            "ix_appointments_company_start_end_status",
            "appointments",
            ["company_id", "start_time", "end_time", "estado"],
            unique=False,
        )

    if "appointment_participants" in tabelas:
        op.create_index(
            "ix_appointment_participants_user_appointment",
            "appointment_participants",
            ["user_id", "appointment_id"],
            unique=False,
        )

    if "appointment_participants" in tabelas:
        op.create_index(
            "ix_appointment_participants_user_appointment",
            "appointment_participants",
            ["user_id", "appointment_id"],
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

    if "appointments" in tabelas:
        appointment_indexes = {
            index["name"]
            for index in inspetor.get_indexes("appointments")
        }
        if "ix_appointments_company_starts_ends_status" in appointment_indexes:
            op.drop_index(
                "ix_appointments_company_starts_ends_status",
                table_name="appointments",
            )

    if "appointments" in tabelas:
        appointment_indexes = {
            index["name"]
            for index in inspetor.get_indexes("appointments")
        }
        if "ix_appointments_company_start_end_status" in appointment_indexes:
            op.drop_index(
                "ix_appointments_company_start_end_status",
                table_name="appointments",
            )
