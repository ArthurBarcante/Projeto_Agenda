# Dependencias e Bibliotecas

## Backend (Python)

Definidas em `pyproject.toml` e `requirements.txt`.

Principais:

- `fastapi`: framework HTTP.
- `SQLAlchemy`: ORM e camada de persistencia.
- `alembic`: migracoes de banco.
- `pydantic`: validacao de schemas.
- `python-jose`: JWT.
- `passlib` e `bcrypt`: hash e verificacao de senha.
- `redis`: rate limit e apoio a runtime.
- `psycopg2-binary`: driver PostgreSQL.
- `uvicorn`: servidor ASGI.
- `python-dotenv`: carregamento de `.env`.
- `requests`: cliente HTTP (webhooks/integracoes).
- `uuid6`: geracao de UUID com melhor ordenacao temporal.

## Frontend (Node)

Definidas em `frontend/package.json`.

- `next`, `react`, `react-dom`: base da aplicacao web.
- `typescript`: tipagem estatica.
- `tailwindcss`, `postcss`, `autoprefixer`: estilos.
- `eslint`, `eslint-config-next`: lint.
- `vitest`, `@vitest/coverage-v8`, `jsdom`: testes.

## Dependencias de ambiente

- PostgreSQL: banco principal.
- Redis: rate limiting.

## Variaveis de ambiente essenciais

Arquivo de referencia: `.env.example`.

- `DATABASE_URL`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REDIS_URL`
- `RATE_LIMIT_REQUESTS_PER_MINUTE`
- `ENVIRONMENT`
