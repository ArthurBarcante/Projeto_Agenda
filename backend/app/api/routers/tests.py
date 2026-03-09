from fastapi import APIRouter, Depends

from app.dependencies.fastapi import get_current_user


router = APIRouter()


@router.get("/me")
def ler_me(current_user=Depends(get_current_user)):
    return {
        "user_id": str(current_user.id),
        "company_id": str(current_user.company_id),
    }
