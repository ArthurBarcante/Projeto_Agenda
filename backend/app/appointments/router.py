from fastapi import APIRouter


router = APIRouter(prefix="/appointments", tags=["appointments"])


__all__ = ["router"]