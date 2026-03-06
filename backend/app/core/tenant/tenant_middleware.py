from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.autenticacao.token_jwt import decodificar_token
from app.core.tenant.tenant_context import clear_tenant, set_tenant


class TenantContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        clear_tenant()
        try:
            authorization = request.headers.get("Authorization")
            if authorization:
                esquema, _, token = authorization.partition(" ")

                if esquema.lower() == "bearer" and token:
                    try:
                        payload = decodificar_token(token)
                    except JWTError:
                        return JSONResponse(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"detail": "Token inválido"},
                        )

                    tenant_id = (
                        payload.get("tenant_id")
                        or payload.get("empresa_id")
                        or payload.get("company_id")
                    )

                    if tenant_id:
                        set_tenant(tenant_id)

            response = await call_next(request)
            return response
        finally:
            clear_tenant()
