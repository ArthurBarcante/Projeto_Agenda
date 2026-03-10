# Setup de Ambiente

## Requisitos

- Python 3.11+
- Node.js 20+
- PostgreSQL 14+
- Redis 6+
- Git

## Variaveis de ambiente

```bash
cp .env.example .env
```

Campos minimos esperados:

- `DATABASE_URL`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REDIS_URL`
- `RATE_LIMIT_REQUESTS_PER_MINUTE`
- `ENVIRONMENT`

## Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic -c alembic.ini upgrade head
uvicorn backend.main:app --reload
```

API local: `http://127.0.0.1:8000`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

UI local: `http://localhost:3000`

## Testes

Backend:

```bash
source .venv/bin/activate
pytest
```

Frontend:

```bash
cd frontend
npm run test:fase2
```

## Troubleshooting rapido

- `Tenant context is required`: consulta tenant-scoped sem contexto definido.
- `Credentials invalids`: slug/email/senha invalidos no login.
- `RATE_LIMIT_EXCEEDED`: tenant ultrapassou limite por minuto.
- conflito em idempotencia: mesma chave com payload diferente (409).
