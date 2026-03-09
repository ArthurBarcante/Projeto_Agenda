from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.security.token_jwt import decode_token
from app.core.errors.api_error import APIError
from app.core.errors.error_codes import ErrorCode
from app.core.tenant_scope import set_current_company_id
from app.core.db.session_scope import get_db
from app.modules.users.models.user import User
from app.modules.users.models.company import Company
from app.modules.permissions.services.permission_service import PermissionService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        company_id: str = payload.get("company_id")

        if user_id is None or company_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    set_current_company_id(company_id)

    user = db.query(User).filter(
        User.id == user_id,
        User.company_id == company_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def get_current_company(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Company:

    company = db.query(Company).filter(
        Company.id == current_user.company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CompanyAlias not found"
        )

    return company


def require_permission(permission_code: str):
    def guard(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        permission_service = PermissionService(db)
        if not permission_service.user_has_permission(
            user_id=current_user.id,
            permission_code=permission_code,
        ):
            raise APIError(
                codigo=ErrorCode.USER_NOT_AUTHORIZED,
                mensagem="User does not have permission for this action",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        return current_user

    return guard