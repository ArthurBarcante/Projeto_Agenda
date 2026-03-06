"""criar tabela webhook_subscriptions

Revision ID: e1a9d4b7c2f6
Revises: d2e6f9a4b1c3
Create Date: 2026-03-06 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e1a9d4b7c2f6"
down_revision: Union[str, Sequence[str], None] = "d2e6f9a4b1c3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "webhook_subscriptions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("empresa_id", sa.UUID(), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("secret", sa.Text(), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_webhook_subscriptions_empresa_evento_ativo",
        "webhook_subscriptions",
        ["empresa_id", "event_type", "ativo"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_webhook_subscriptions_empresa_evento_ativo",
        table_name="webhook_subscriptions",
    )
    op.drop_table("webhook_subscriptions")
