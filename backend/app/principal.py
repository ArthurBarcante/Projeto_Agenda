from fastapi import FastAPI
from app import __version__
from app.core.errors.error_handlers import register_error_handlers
from app.core.rate_limit.rate_limit_middleware import RateLimitMiddleware
from app.core.tenant.tenant_middleware import TenantContextMiddleware
from app.modules.agenda.events import registrar_handlers_agenda
from app.modules.webhooks.events import registrar_handlers_webhooks
from app.modules.agenda.api import legacy_router as legacy_appointments_router
from app.modules.agenda.api import router as appointments_router
from app.modules.auth.api import legacy_router as legacy_auth_router
from app.modules.auth.api import router as auth_router
from app.modules.testes.api import router as test_router

app = FastAPI(version=__version__)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TenantContextMiddleware)
register_error_handlers(app)
registrar_handlers_agenda()
registrar_handlers_webhooks()

app.include_router(auth_router)
app.include_router(appointments_router)
app.include_router(legacy_auth_router)
app.include_router(legacy_appointments_router)
app.include_router(test_router)
