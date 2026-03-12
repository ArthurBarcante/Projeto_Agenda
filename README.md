# AIgenda

Plataforma de agenda digital para organizacao de compromissos, com base arquitetural preparada para crescimento por modulos.

## Descricao

O **AIgenda** e um projeto de organizacao de agenda para pessoas, equipes e empresas.

O repositorio atual combina duas frentes:

- uma visao de produto orientada a organizacao inteligente e evolucao futura;
- uma base tecnica em consolidacao, com backend, frontend, testes e documentacao separados.

Hoje, o projeto ja possui estrutura para autenticacao, usuarios, compromissos, persistencia com SQLAlchemy, interface web com Next.js e suites de testes organizadas por contexto.

## Estado atual do repositorio

O repositrio esta em fase de consolidacao da base.

Isso significa que a arquitetura esta mais avancada do que a quantidade de fluxos completos expostos na interface e na API.

Em termos práticos, o codigo atual entrega:

- aplicacao FastAPI com registro de routers de `auth`, `users` e `appointments`;
- models ORM para usuarios e compromissos;
- camada de banco separada em `backend/db/`;
- frontend com rotas de `signin`, `dashboard`, `appointments` e `profile`;
- cliente HTTP compartilhado no frontend;
- testes de backend e frontend organizados por feature.

## Documentacao

A documentacao do projeto esta organizada por publico.

### Beginner

- [docs/beginner/what_is_the_project.md](docs/beginner/what_is_the_project.md)
- [docs/beginner/what_the_project_does.md](docs/beginner/what_the_project_does.md)
- [docs/beginner/how_the_project_works.md](docs/beginner/how_the_project_works.md)

### Developer

- [docs/developer/project_structure.md](docs/developer/project_structure.md)
- [docs/developer/backend.md](docs/developer/backend.md)
- [docs/developer/frontend.md](docs/developer/frontend.md)
- [docs/developer/tests.md](docs/developer/tests.md)
- [docs/developer/architecture.md](docs/developer/architecture.md)
- [docs/developer/project_planning.md](docs/developer/project_planning.md)
- [docs/developer/future_improvements.md](docs/developer/future_improvements.md)

## Estrutura principal

- `backend/`: API, modelos, servicos e infraestrutura de banco.
- `frontend/`: interface web com Next.js, React e TypeScript.
- `tests/`: testes de backend e frontend.
- `docs/`: documentacao para iniciantes e desenvolvedores.

## Tecnologias

### Backend

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- Uvicorn

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Qualidade

- Pytest
- Vitest
- ESLint

## Setup

### 1. Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd aigenda
```

### 2. Configurar ambiente Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar banco de dados

Defina a variavel `DATABASE_URL` no seu ambiente ou no arquivo `.env`, conforme sua configuracao local.

Depois execute as migracoes:

```bash
alembic -c backend/db/alembic.ini upgrade head
```

### 4. Subir o backend

```bash
uvicorn backend.app.main:app --reload
```

API disponivel em `http://127.0.0.1:8000`.

### 5. Subir o frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend disponivel em `http://localhost:3000`.

## Endpoints e rotas relevantes no estado atual

### Backend

- `POST /auth/login`
- prefixo `/users`
- prefixo `/appointments`

Observacao: os routers ja estao registrados, mas parte do comportamento ainda esta em implementacao.

### Frontend

- `/signin`
- `/dashboard`
- `/appointments`
- `/profile`

## Testes

```bash
pytest -c tests/config/pytest.ini --rootdir=.
pytest -c tests/config/pytest.ini --rootdir=. tests/backend/
pytest -c tests/config/pytest.ini --rootdir=. tests/frontend/
```

No frontend:

```bash
cd frontend
npm test
```

## Terminologia adotada

Para manter consistencia entre codigo e documentacao:

- o dominio de negocio e descrito em portugues como `compromissos`;
- o nome tecnico do modulo e da rota continua `appointments`;
- o fluxo de acesso do usuario e descrito como `login` ou `autenticacao`;
- a rota web correspondente no frontend continua `signin`;
- o modulo tecnico do backend continua `auth`.

## Licenca

Este projeto esta sob a licenca **Apache License 2.0**. Consulte o arquivo `LICENSE` para detalhes.
