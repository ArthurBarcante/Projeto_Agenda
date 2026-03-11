from fastapi import FastAPI
from . import __version__
from .core.errors.error_handlers import register_error_handlers
from .middleware.rate_limit_middleware import RateLimitMiddleware
from .middleware.tenant_middleware import TenantContextMiddleware
from .modules.schedule.events import register_schedule_handlers
from .modules.notifications.events import register_webhook_handlers
from .api.routers.schedule import legacy_router as legacy_appointments_router
from .api.routers.schedule import router as appointments_router
from .api.routers.auth import legacy_router as legacy_auth_router
from .api.routers.auth import router as auth_router
from .api.routers.tests import router as test_router


def register_middlewares(app: FastAPI) -> None:
    """Register application middlewares."""
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(TenantContextMiddleware)


def register_routers(app: FastAPI) -> None:
    """Register API routers."""
    app.include_router(auth_router)
    app.include_router(appointments_router)
    app.include_router(legacy_auth_router)
    app.include_router(legacy_appointments_router)
    app.include_router(test_router)


def register_events() -> None:
    """Register event handlers."""
    register_schedule_handlers()
    register_webhook_handlers()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Agenda API",
        description="Multi-tenant scheduling API",
        version=__version__,
    )

    register_error_handlers(app)
    register_middlewares(app)
    register_events()
    register_routers(app)

    return app


app = create_app()
