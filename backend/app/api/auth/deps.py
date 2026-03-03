from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.auth.jwt import decode_token
from app.db.session import get_db
from app.models.user import User
from app.models.company import Company

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
              detail="Invalid authentication credentials"
              )
            
    except JWTError:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid authentication credentials"
          )
        
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
          detail="Company not found"
          )
        
    return company