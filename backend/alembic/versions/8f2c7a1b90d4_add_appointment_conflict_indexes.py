"""add appointment conflict indexes

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
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    if "appointments" in tables:
        op.create_index(
            "ix_appointments_company_starts_ends_status",
            "appointments",
            ["company_id", "starts_at", "ends_at", "status"],
            unique=False,
        )

    if "appointment_participants" in tables:
        op.create_index(
            "ix_appointment_participants_user_appointment",
            "appointment_participants",
            ["user_id", "appointment_id"],
            unique=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    if "appointment_participants" in tables:
        participant_indexes = {
            index["name"]
            for index in inspector.get_indexes("appointment_participants")
        }
        if "ix_appointment_participants_user_appointment" in participant_indexes:
            op.drop_index(
                "ix_appointment_participants_user_appointment",
                table_name="appointment_participants",
            )

    if "appointments" in tables:
        appointment_indexes = {
            index["name"]
            for index in inspector.get_indexes("appointments")
        }
        if "ix_appointments_company_starts_ends_status" in appointment_indexes:
            op.drop_index(
                "ix_appointments_company_starts_ends_status",
                table_name="appointments",
            )
