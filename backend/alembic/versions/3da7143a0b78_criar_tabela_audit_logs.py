"""criar tabela audit_logs

Revision ID: 3da7143a0b78
Revises: a0abcfefcde4
Create Date: 2026-03-05 11:53:20.341082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '3da7143a0b78'
down_revision: Union[str, Sequence[str], None] = 'a0abcfefcde4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("empresa_id", sa.UUID(), nullable=False),
        sa.Column("usuario_id", sa.UUID(), nullable=True),
        sa.Column("acao", sa.String(length=120), nullable=False),
        sa.Column("entidade", sa.String(length=120), nullable=False),
        sa.Column("entidade_id", sa.UUID(), nullable=False),
        sa.Column("dados_antes", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("dados_depois", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_audit_logs_usuario_id", "audit_logs", ["usuario_id"], unique=False)
    op.create_index(
        "ix_audit_logs_empresa_entidade_criado",
        "audit_logs",
        ["empresa_id", "entidade", "criado_em"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_audit_logs_empresa_entidade_criado", table_name="audit_logs")
    op.drop_index("ix_audit_logs_usuario_id", table_name="audit_logs")
    op.drop_table("audit_logs")
