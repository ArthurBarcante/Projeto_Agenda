from fastapi import FastAPI
from app import __version__
from app.core.errors.error_handlers import register_error_handlers
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.middleware.tenant_middleware import TenantContextMiddleware
from app.modules.schedule.events import register_schedule_handlers
from app.modules.notifications.events import register_webhook_handlers
from app.api.routers.schedule import legacy_router as legacy_appointments_router
from app.api.routers.schedule import router as appointments_router
from app.api.routers.auth import legacy_router as legacy_auth_router
from app.api.routers.auth import router as auth_router
from app.api.routers.tests import router as test_router

app = FastAPI(version=__version__)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TenantContextMiddleware)
register_error_handlers(app)
register_schedule_handlers()
register_webhook_handlers()

app.include_router(auth_router)
app.include_router(appointments_router)
app.include_router(legacy_auth_router)
app.include_router(legacy_appointments_router)
app.include_router(test_router)
