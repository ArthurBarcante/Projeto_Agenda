from app.api.routers.auth import legacy_router as auth_legacy_router
from app.api.routers.auth import router as auth_router
from app.api.routers.schedule import legacy_router as schedule_legacy_router
from app.api.routers.schedule import router as schedule_router
from app.api.routers.tests import router as tests_router

__all__ = [
	"auth_router",
	"auth_legacy_router",
	"schedule_router",
	"schedule_legacy_router",
	"tests_router",
]
