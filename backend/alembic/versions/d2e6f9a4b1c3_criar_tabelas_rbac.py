"""criar tabelas rbac

Revision ID: d2e6f9a4b1c3
Revises: c4d8a1f2e7b9
Create Date: 2026-03-06 12:00:00.000000

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d2e6f9a4b1c3"
down_revision: Union[str, Sequence[str], None] = "c4d8a1f2e7b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("empresa_id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "permissions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("codigo", sa.String(length=120), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo", name="uq_permissions_codigo"),
    )

    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column("permission_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )

    op.create_table(
        "user_roles",
        sa.Column("usuario_id", sa.UUID(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("usuario_id", "role_id"),
    )

    op.create_index("ix_roles_empresa_id", "roles", ["empresa_id"])
    op.create_index("ix_permissions_codigo", "permissions", ["codigo"])
    op.create_index("ix_user_roles_usuario_id", "user_roles", ["usuario_id"])

    permissions_table = sa.table(
        "permissions",
        sa.column("id", sa.UUID()),
        sa.column("codigo", sa.String(length=120)),
        sa.column("descricao", sa.Text()),
    )
    op.bulk_insert(
        permissions_table,
        [
            {
                "id": uuid4(),
                "codigo": "agenda.criar",
                "descricao": "Permite criar compromissos",
            },
            {
                "id": uuid4(),
                "codigo": "agenda.editar",
                "descricao": "Permite editar compromissos",
            },
            {
                "id": uuid4(),
                "codigo": "agenda.cancelar",
                "descricao": "Permite cancelar compromissos",
            },
            {
                "id": uuid4(),
                "codigo": "usuarios.criar",
                "descricao": "Permite criar usuários",
            },
            {
                "id": uuid4(),
                "codigo": "usuarios.editar",
                "descricao": "Permite editar usuários",
            },
            {
                "id": uuid4(),
                "codigo": "dashboard.visualizar",
                "descricao": "Permite visualizar dashboard",
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_user_roles_usuario_id", table_name="user_roles")
    op.drop_index("ix_permissions_codigo", table_name="permissions")
    op.drop_index("ix_roles_empresa_id", table_name="roles")
    op.drop_table("user_roles")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")
