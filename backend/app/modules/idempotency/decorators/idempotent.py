import inspect
import json
from collections.abc import Callable
from functools import wraps
from typing import Any

from fastapi import HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.modules.idempotency.services.idempotency_service import IdempotencyService


def _resolve_arguments(
    handler: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    bound_arguments = inspect.signature(handler).bind_partial(*args, **kwargs)
    return dict(bound_arguments.arguments)


def _get_by_path(arguments: dict[str, Any], path: str) -> Any:
    current: Any = arguments
    for part in path.split("."):
        if isinstance(current, dict):
            if part not in current:
                raise KeyError(part)
            current = current[part]
            continue

        if not hasattr(current, part):
            raise KeyError(part)
        current = getattr(current, part)

    return current


def _get_request(arguments: dict[str, Any], request_arg_name: str) -> Request:
    request = arguments.get(request_arg_name)
    if not isinstance(request, Request):
        raise RuntimeError(
            "Decorator @idempotent requer um parâmetro Request no handler "
            f"(nome esperado: '{request_arg_name}')."
        )
    return request


def _get_service(
    arguments: dict[str, Any],
    service_arg_name: str,
    db_arg_name: str,
) -> IdempotencyService:
    existing_service = arguments.get(service_arg_name)
    if isinstance(existing_service, IdempotencyService):
        return existing_service

    db = arguments.get(db_arg_name)
    if isinstance(db, Session):
        return IdempotencyService(db)

    for value in arguments.values():
        if isinstance(value, Session):
            return IdempotencyService(value)

    raise RuntimeError(
        "Decorator @idempotent não encontrou Session nem IdempotencyService no handler. "
        "Adicione `db: Session = Depends(get_db)` ou "
        "`idempotency_service: IdempotencyService = Depends(...)`."
    )


def _normalize_body_for_storage(content: Any) -> dict[str, Any]:
    encoded = jsonable_encoder(content)
    if isinstance(encoded, dict):
        return encoded
    return {"data": encoded}


def _extract_response_payload(response: Response) -> dict[str, Any]:
    body = response.body or b""
    if not body:
        return {}

    content_type = (response.headers.get("content-type") or "").lower()
    if "application/json" in content_type:
        try:
            decoded = json.loads(body.decode("utf-8"))
            return _normalize_body_for_storage(decoded)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    return {"raw": body.decode("utf-8", errors="replace")}


def _infer_status_code(request: Request) -> int:
    route = request.scope.get("route")
    route_status_code = getattr(route, "status_code", None)
    if isinstance(route_status_code, int):
        return route_status_code
    return 200


def _build_error_payload(exc: Exception) -> tuple[dict[str, Any] | None, int | None]:
    if isinstance(exc, HTTPException):
        return _normalize_body_for_storage({"detail": exc.detail}), exc.status_code

    return None, 500


def idempotent(
    *,
    company_id_path: str = "current_user.company_id",
    request_arg_name: str = "request",
    service_arg_name: str = "idempotency_service",
    db_arg_name: str = "db",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator para encapsular o fluxo de idempotência em handlers FastAPI.

    Requisitos esperados no handler:
    - Request disponível (default: parâmetro `request`)
    - company_id acessível via `company_id_path` (default: `current_user.company_id`)
    - Session SQLAlchemy (`db`) ou `idempotency_service`
    """

    def decorator(handler: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(handler)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            arguments = _resolve_arguments(handler, args, kwargs)
            request = _get_request(arguments, request_arg_name)
            service = _get_service(arguments, service_arg_name, db_arg_name)

            try:
                company_id = _get_by_path(arguments, company_id_path)
            except KeyError as exc:
                raise RuntimeError(
                    "Decorator @idempotent não conseguiu resolver company_id "
                    f"via '{company_id_path}'."
                ) from exc

            resposta_armazenada = await service.reivindicar_chave(
                request=request,
                company_id=company_id,
            )
            if resposta_armazenada is not None:
                return resposta_armazenada

            try:
                if inspect.iscoroutinefunction(handler):
                    result = await handler(*args, **kwargs)
                else:
                    result = await run_in_threadpool(handler, *args, **kwargs)
            except Exception as exc:
                error_body, error_status = _build_error_payload(exc)
                await service.marcar_como_falha(
                    request=request,
                    company_id=company_id,
                    error_body=error_body,
                    status_code=error_status,
                )
                raise

            if isinstance(result, Response):
                response_body = _extract_response_payload(result)
                status_code = result.status_code
            else:
                response_body = _normalize_body_for_storage(result)
                status_code = _infer_status_code(request)

            await service.finalizar_resposta(
                request=request,
                company_id=company_id,
                response_body=response_body,
                status_code=status_code,
            )
            return result

        wrapper.__signature__ = inspect.signature(handler)
        return wrapper

    return decorator
