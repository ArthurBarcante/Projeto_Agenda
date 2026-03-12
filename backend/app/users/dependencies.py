from sqlalchemy.orm import Session

from app.users.repository import UserRepository
from app.users.service import UserService


def get_user_repository(db: Session) -> UserRepository:
    return UserRepository(db)


def get_user_service(db: Session) -> UserService:
    return UserService(db)


__all__ = ["get_user_repository", "get_user_service"]