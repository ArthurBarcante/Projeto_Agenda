from sqlalchemy.orm import Session

from app.users.repository import UserRepository


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = UserRepository(db)


__all__ = ["UserService"]