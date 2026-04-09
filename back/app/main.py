import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.connection import engine
from app.models.events import Event
from app.models.tasks import Task
from app.models.user import User
from app.routers.agenda import events as agenda_events
from app.routers.agenda import tasks as agenda_tasks
from app.routers.auth import login as auth_login
from app.routers.auth import register


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

    app.include_router(auth_login.router)
    app.include_router(register.router)
    app.include_router(agenda_tasks.router)
    app.include_router(agenda_events.router)

    @app.get("/")
    def read_root():
        return {"message": "Backend funcionando!"}

    return app


app = create_app()
