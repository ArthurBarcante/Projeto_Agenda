import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.connection import engine
from app.modules.auth import router as auth_router
from app.modules.badges.model import Badge
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


def should_init_database() -> bool:
    return os.getenv("APP_INIT_DB_ON_STARTUP", "1").lower() not in {"0", "false", "no"}


def create_app(init_database_on_startup: bool | None = None) -> FastAPI:
    if init_database_on_startup is None:
        init_database_on_startup = should_init_database()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        if init_database_on_startup:
            init_database()
        yield

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
