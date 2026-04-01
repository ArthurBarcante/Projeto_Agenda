from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.connection import engine
from app.models.user import User
from app.routers.auth import login as auth_login
from app.routers.auth import register

app = FastAPI()

# Ensure SQLAlchemy models are loaded before table creation.
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_login.router)
app.include_router(register.router)

@app.get("/")
def read_root():
    return {"message": "Backend funcionando!"}
