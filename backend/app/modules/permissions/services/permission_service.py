from uuid import UUID

from sqlalchemy.orm import Session

from app.core.tenant.tenant_context import get_tenant
from app.modules.permissions.models.permission import Permission
from app.modules.permissions.models.role import Role
from app.modules.permissions.models.role_permission import RolePermission
from app.modules.permissions.models.user_role import UserRole


class PermissionService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def user_has_permission(
        self,
        user_id: UUID,
        permission_code: str,
    ) -> bool:
        tenant_id = get_tenant()

        consulta = (
            self.db.query(Permission.id)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(UserRole.user_id == user_id)
            .filter(Permission.code == permission_code)
        )

        if tenant_id is not None:
            consulta = consulta.filter(Role.company_id == tenant_id)

        return consulta.first() is not None

    def user_has_permission(
        self,
        user_id: UUID,
        permission_code: str,
    ) -> bool:
        return self.user_has_permission(
            user_id=user_id,
            permission_code=permission_code,
        )
