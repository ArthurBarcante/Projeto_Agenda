from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.company import Company
from app.models.user import User
from app.core.auth.security import verify_password
from app.core.auth.jwt import create_access_token
from app.core.tenant import set_current_company_id
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
  company_slug: str
  email: EmailStr
  password: str


class TokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
  
    company = db.query(Company).filter(
      Company.slug == data.company_slug
      ).first()
    
    if not company:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid credentials"
          )

    set_current_company_id(company.id)
    
    user = db.query(User).filter(
      User.email == data.email, 
      User.company_id == company.id
      ).first()
    
    if not user:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED, 
          detail="Invalid credentials"
          )
    
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED, 
          detail="Invalid credentials"
          )
        
    token = create_access_token(
      {
        "sub": str(user.id),
        "company_id": str(company.id),
        "company_slug": company.slug
        }
      )
    
    return TokenResponse(access_token=token)