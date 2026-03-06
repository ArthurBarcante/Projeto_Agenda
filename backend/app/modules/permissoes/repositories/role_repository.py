from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.permissoes.models.role import Role
from app.modules.permissoes.models.user_role import UserRole
from app.repositorios.base_repository import BaseRepository


class RoleRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def create_role(
        self,
        company_id: UUID,
        name: str,
        description: str | None = None,
    ) -> Role:
        role = Role(
            company_id=company_id,
            name=name,
            description=description,
        )
        self.add(role)
        self.commit()
        self.refresh(role)
        return role

    def list_company_roles(self, company_id: UUID) -> list[Role]:
        return (
            self.query(Role)
            .filter(Role.company_id == company_id)
            .order_by(Role.name.asc())
            .all()
        )

    def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> UserRole:
        existente = (
            self.query(UserRole)
            .filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
            )
            .first()
        )
        if existente is not None:
            return existente

        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
        )
        self.add(user_role)
        self.commit()
        return user_role

    def list_user_roles(self, user_id: UUID) -> list[Role]:
        return (
            self.query(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(UserRole.user_id == user_id)
            .order_by(Role.name.asc())
            .all()
        )

    def criar_role(self, empresa_id: UUID, nome: str, descricao: str | None = None) -> Role:
        return self.create_role(company_id=empresa_id, name=nome, description=descricao)

    def buscar_roles_empresa(self, empresa_id: UUID) -> list[Role]:
        return self.list_company_roles(company_id=empresa_id)

    def atribuir_role_usuario(self, usuario_id: UUID, role_id: UUID) -> UserRole:
        return self.assign_role_to_user(user_id=usuario_id, role_id=role_id)

    def buscar_roles_usuario(self, usuario_id: UUID) -> list[Role]:
        return self.list_user_roles(user_id=usuario_id)
