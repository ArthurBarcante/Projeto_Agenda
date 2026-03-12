"""add_exclusion_constraint_appointments

Revision ID: a0abcfefcde4
Revises: b7e4c2a9d1f0
Create Date: 2026-03-05 11:33:17.199842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0abcfefcde4'
down_revision: Union[str, Sequence[str], None] = 'b7e4c2a9d1f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist;")
    op.execute(
        sa.text(
            """
            DO $$
            DECLARE
                appointments_regclass regclass;
            BEGIN
                SELECT to_regclass('public.appointments') INTO appointments_regclass;

                IF appointments_regclass IS NOT NULL
                AND NOT EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = 'ex_appointments_tenant_period_no_overlap'
                    AND conrelid = appointments_regclass
                ) THEN
                    ALTER TABLE public.appointments
                    ADD CONSTRAINT ex_appointments_tenant_period_no_overlap
                    EXCLUDE USING GIST (
                        company_id WITH =,
                        tstzrange(start_time, end_time, '[)') WITH &&
                    );
                END IF;
            END
            $$;
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            """
            DO $$
            DECLARE
                appointments_regclass regclass;
            BEGIN
                SELECT to_regclass('public.appointments') INTO appointments_regclass;

                IF appointments_regclass IS NOT NULL
                AND EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = 'ex_appointments_tenant_period_no_overlap'
                    AND conrelid = appointments_regclass
                ) THEN
                    ALTER TABLE public.appointments
                    DROP CONSTRAINT ex_appointments_tenant_period_no_overlap;
                END IF;
            END
            $$;
            """
        )
    )
