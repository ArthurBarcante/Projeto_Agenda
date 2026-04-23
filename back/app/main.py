import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from app.core.config import ALLOWED_ORIGINS
from app.core.logging_config import get_logger, setup_logging
from app.database.base import Base
from app.database.connection import engine
from app.modules.auth import router as auth_router
from app.modules.badges.model import Badge
from app.modules.badges.user_badge_model import UserBadge
from app.modules.events import router as events_router
from app.modules.events.model import Event
from app.modules.progress import router as progress_router
from app.modules.progress.model import Progress
from app.modules.tasks import router as tasks_router
from app.modules.tasks.model import Task
from app.modules.users import router as users_router
from app.modules.users.model import User


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    apply_sqlite_compat_migrations()


def apply_sqlite_compat_migrations() -> None:
    """Aplicar ajustes mínimos de schema para bancos SQLite legados.

    Evita falha em runtime quando o arquivo SQLite já existia e um campo novo
    foi adicionado no modelo sem ferramenta formal de migration.
    """
    if engine.dialect.name != "sqlite":
        return

    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "progress" not in table_names:
        return

    progress_columns = {column["name"] for column in inspector.get_columns("progress")}
    if "last_completed_at" in progress_columns:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE progress ADD COLUMN last_completed_at DATETIME"))


def should_init_database() -> bool:
    return os.getenv("APP_INIT_DB_ON_STARTUP", "1").lower() not in {"0", "false", "no"}


def create_app(init_database_on_startup: bool | None = None) -> FastAPI:
    if init_database_on_startup is None:
        init_database_on_startup = should_init_database()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        setup_logging()
        logger = get_logger(__name__)
        logger.info("Aplicação iniciando")
        if init_database_on_startup:
            init_database()
            logger.info("Banco de dados inicializado")
        yield
        logger.info("Aplicação encerrando")

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _request_logger = get_logger("app.requests")

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.monotonic()
        response = await call_next(request)
        duration_ms = round((time.monotonic() - start) * 1000)
        _request_logger.info(
            "%s %s -> %d (%dms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response

    app.include_router(auth_router.router)
    app.include_router(users_router.router)
    app.include_router(tasks_router.router)
    app.include_router(events_router.router)
    app.include_router(progress_router.router)

    @app.get("/")
    def read_root():
        return {"message": "Backend funcionando!"}

    return app


app = create_app()
