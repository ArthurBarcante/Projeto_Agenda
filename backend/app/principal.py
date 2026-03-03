from fastapi import FastAPI
from app import __version__
from app.api.autenticacao import router as rota_autenticacao
from app.api.compromissos import router as compromissos_router
from app.api.testes.testes import router as rota_testes

app = FastAPI(version=__version__)

app.include_router(rota_autenticacao)
app.include_router(compromissos_router)
app.include_router(rota_testes)
