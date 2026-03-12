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
        sa.Column("company_id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "permissions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("codigo", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
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
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )

    op.create_index("ix_roles_company_id", "roles", ["company_id"])
    op.create_index("ix_permissions_codigo", "permissions", ["codigo"])
    op.create_index("ix_user_roles_user_id", "user_roles", ["user_id"])

    permissions_table = sa.table(
        "permissions",
        sa.column("id", sa.UUID()),
        sa.column("codigo", sa.String(length=120)),
        sa.column("description", sa.Text()),
    )
    op.bulk_insert(
        permissions_table,
        [
            {
                "id": uuid4(),
                "codigo": "agenda.criar",
                "description": "Permite criar appointments",
            },
            {
                "id": uuid4(),
                "codigo": "agenda.editar",
                "description": "Permite editar appointments",
            },
            {
                "id": uuid4(),
                "codigo": "agenda.cancel",
                "description": "Permite cancel appointments",
            },
            {
                "id": uuid4(),
                "codigo": "users.criar",
                "description": "Permite criar users",
            },
            {
                "id": uuid4(),
                "codigo": "users.editar",
                "description": "Permite editar users",
            },
            {
                "id": uuid4(),
                "codigo": "dashboard.visualizar",
                "description": "Permite visualizar dashboard",
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_user_roles_user_id", table_name="user_roles")
    op.drop_index("ix_permissions_codigo", table_name="permissions")
    op.drop_index("ix_roles_company_id", table_name="roles")
    op.drop_table("user_roles")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")
