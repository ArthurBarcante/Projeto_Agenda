"""FastAPI application factory."""

from fastapi import FastAPI

from app import __version__
from app.users.router import router as users_router
from app.appointments.router import router as appointments_router
from app.auth.router import router as auth_router


def register_middlewares(app: FastAPI) -> None:
    """Register application middlewares.
    
    Args:
        app: FastAPI application instance
    """
    pass


def register_routers(app: FastAPI) -> None:
    """Register application routers.
    
    Args:
        app: FastAPI application instance
    """
    app.include_router(users_router)
    app.include_router(appointments_router)
    app.include_router(auth_router)


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Agenda API",
        description="Multi-tenant scheduling API",
        version=__version__,
    )

    register_middlewares(app)
    register_routers(app)

    return app


app = create_app()

