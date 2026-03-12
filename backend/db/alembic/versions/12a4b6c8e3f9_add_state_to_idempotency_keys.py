"""adicionar coluna state em idempotency_keys

Revision ID: 12a4b6c8e3f9
Revises: f3b1c9e4a2d7
Create Date: 2026-03-11 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "12a4b6c8e3f9"
down_revision: Union[str, Sequence[str], None] = "f3b1c9e4a2d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar o enum type
    sa.Enum("IN_PROGRESS", "COMPLETED", "FAILED", name="idempotency_state").create(
        op.get_bind(), checkfirst=True
    )
    
    # Adicionar coluna com valor default IN_PROGRESS para registros existentes
    op.add_column(
        "idempotency_keys",
        sa.Column(
            "state",
            sa.Enum("IN_PROGRESS", "COMPLETED", "FAILED", name="idempotency_state"),
            nullable=False,
            server_default="COMPLETED",  # Registros existentes são marcados como completos
        ),
    )
    
    # Adicionar coluna updated_at (caso não exista)
    op.add_column(
        "idempotency_keys",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
    
    # Adicionar índice para queries por estado
    op.create_index(
        "ix_idempotency_keys_state",
        "idempotency_keys",
        ["state"],
    )
    
    # Adicionar índice composto para leituras por company_id, key, estado
    op.create_index(
        "ix_idempotency_keys_company_key_state",
        "idempotency_keys",
        ["company_id", "key", "state"],
    )


def downgrade() -> None:
    op.drop_index("ix_idempotency_keys_company_key_state", table_name="idempotency_keys")
    op.drop_index("ix_idempotency_keys_state", table_name="idempotency_keys")
    op.drop_column("idempotency_keys", "updated_at")
    op.drop_column("idempotency_keys", "state")
    sa.Enum(name="idempotency_state").drop(op.get_bind(), checkfirst=True)
