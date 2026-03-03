from fastapi import FastAPI
from app import __version__
from app.api.auth import router as auth_router
from app.api.schedule import router as appointments_router
from app.api.test.tests import router as test_router

app = FastAPI(version=__version__)

app.include_router(auth_router)
app.include_router(appointments_router)

app.include_router(test_router)
