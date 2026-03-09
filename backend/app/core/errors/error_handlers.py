from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.errors.api_error import APIError
from app.core.errors.error_codes import ErrorCode


def _utc_iso_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _payload(codigo: ErrorCode | str, mensagem: str) -> dict[str, dict[str, str]]:
    code_value = codigo.value if isinstance(codigo, ErrorCode) else codigo
    return {
        "erro": {
            "codigo": code_value,
            "mensagem": mensagem,
            "timestamp": _utc_iso_timestamp(),
        }
    }


def _mensagem_http_exception(exc: HTTPException) -> str:
    detalhe = exc.detail
    if isinstance(detalhe, str):
        return detalhe
    if detalhe is None:
        return "Erro na request"
    return str(detalhe)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(APIError)
    async def handle_api_error(_: Request, exc: APIError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
        codigo = ErrorCode.VALIDATION_FAILED if exc.status_code < 500 else ErrorCode.INTERNAL_ERROR
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload(codigo, _mensagem_http_exception(exc)),
        )

    @app.exception_handler(RequestValidationError)
    @app.exception_handler(ValidationError)
    async def handle_validation_error(_: Request, exc: Exception) -> JSONResponse:
        if isinstance(exc, RequestValidationError):
            mensagem = "Dados de entrada invalids"
        elif isinstance(exc, ValidationError):
            mensagem = "Falha de validation"
        else:
            mensagem = "Falha de validation"

        return JSONResponse(
            status_code=422,
            content=_payload(ErrorCode.VALIDATION_FAILED, mensagem),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=_payload(ErrorCode.INTERNAL_ERROR, "Erro interno no servidor"),
        )
