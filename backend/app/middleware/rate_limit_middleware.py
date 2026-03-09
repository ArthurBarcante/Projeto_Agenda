from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.errors.api_error import APIError
from app.core.errors.error_codes import ErrorCode
from app.core.rate_limit.rate_limit_service import verificar_rate_limit
from app.core.tenant.tenant_context import get_tenant


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            company_id = get_tenant()

            if company_id is not None:
                limite_excedido = await verificar_rate_limit(company_id)
                if limite_excedido:
                    raise APIError(
                        codigo=ErrorCode.RATE_LIMIT_EXCEEDED,
                        mensagem="Limite de requests por minuto excedido.",
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    )

            return await call_next(request)
        except APIError as exc:
            return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
