# Como Rodar o Sistema (Passo a Passo)

Este guia mostra como iniciar o AIgenda em um computador local.

## O que voce precisa instalado

- Python 3.11 ou superior
- Node.js 20 ou superior
- PostgreSQL
- Redis
- Git

## Passo 1: abrir o projeto

```bash
git clone <url-do-repositorio>
cd aigenda
```

## Passo 2: criar configuracao local

```bash
cp .env.example .env
```

No arquivo `.env`, confira principalmente:

- `DATABASE_URL`
- `SECRET_KEY`
- `REDIS_URL`
- `RATE_LIMIT_REQUESTS_PER_MINUTE`

## Passo 3: iniciar banco e cache

Garanta que PostgreSQL e Redis estao ativos na sua maquina.

## Passo 4: iniciar backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic -c alembic.ini upgrade head
uvicorn backend.main:app --reload
```

Se tudo estiver certo, a API abre em `http://127.0.0.1:8000`.

## Passo 5: iniciar frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Se tudo estiver certo, a interface abre em `http://localhost:3000`.

## Passo 6: testar rapidamente

1. Abra `http://localhost:3000`.
2. Faca login com um usuario valido.
3. Tente criar um compromisso.
4. Confirme se ele aparece no fluxo esperado.

## Problemas comuns

- Erro de banco: revise `DATABASE_URL`.
- Erro de token: revise `SECRET_KEY`.
- Erro de limite de requisicao: ajuste `RATE_LIMIT_REQUESTS_PER_MINUTE`.
- Erro de conexao com cache: revise `REDIS_URL`.
