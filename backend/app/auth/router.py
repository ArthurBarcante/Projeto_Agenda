"""Auth module router."""

from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags=["auth"])


__all__ = ["router"]
