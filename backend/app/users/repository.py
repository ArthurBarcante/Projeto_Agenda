from sqlalchemy.orm import Session

from app.users.model import User


class UserRepository:
    model = User

    def __init__(self, db: Session) -> None:
        self.db = db


__all__ = ["UserRepository"]