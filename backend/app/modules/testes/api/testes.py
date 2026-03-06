from fastapi import APIRouter, Depends

from app.api.dependencias import obter_usuario_atual


router = APIRouter()


@router.get("/me")
def ler_me(usuario_atual=Depends(obter_usuario_atual)):
    return {
        "usuario_id": str(usuario_atual.id),
        "empresa_id": str(usuario_atual.company_id),
    }
