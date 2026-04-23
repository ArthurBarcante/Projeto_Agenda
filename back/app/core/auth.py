from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.core.security import decode_access_token
from app.database.deps import get_db
from app.modules.users.model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_logger = get_logger(__name__)

credentials_exception = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Token invalido",
	headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
):
	payload = decode_access_token(token)
	if payload is None:
		_logger.warning("invalid_token")
		raise credentials_exception

	user_id = payload.get("sub")
	if user_id is None:
		_logger.warning("token_missing_sub")
		raise credentials_exception

	try:
		parsed_user_id = int(user_id)
	except (TypeError, ValueError):
		_logger.warning("token_invalid_sub sub=%s", user_id)
		raise credentials_exception

	user = db.query(User).filter(User.id == parsed_user_id).first()
	if user is None:
		_logger.warning("token_user_not_found user_id=%d", parsed_user_id)
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuario nao encontrado",
			headers={"WWW-Authenticate": "Bearer"},
		)

	return user
