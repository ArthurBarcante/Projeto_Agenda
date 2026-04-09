# Projeto Agenda

Projeto de organizacao pessoal com frontend em HTML, CSS e JavaScript puro e backend em FastAPI.

Hoje o projeto esta dividido em duas camadas com niveis diferentes de maturidade:

- o backend ja possui autenticacao, tarefas e eventos com persistencia real
- o frontend ja possui fluxo visual de autenticacao e area autenticada inicial
- a interface da agenda ainda nao consome as APIs de tarefas e eventos

## Geral do projeto

O objetivo do Projeto Agenda e evoluir para uma aplicacao que ajude o usuario a organizar rotina, tarefas e compromissos em um unico lugar.

No estado atual, o sistema ja entrega:

- cadastro de usuario com persistencia em PostgreSQL
- login com JWT
- rota protegida para identificar o usuario autenticado
- CRUD de tarefas por usuario no backend
- CRUD de eventos por usuario no backend
- frontend com login, cadastro, dashboard e navegacao autenticada

Ainda estao em construcao:

- interface visual da agenda conectada ao backend
- interface visual de perfil
- telas para criar, listar, editar e excluir tarefas e eventos no frontend
- recursos mais avancados de acompanhamento de rotina

## Estrutura resumida

```text
Projeto_Agenda/
├── back/app/
│   ├── core/        # autenticacao, token e seguranca
│   ├── database/    # conexao e sessao do banco
│   ├── models/      # tabelas ORM
│   ├── routers/     # endpoints da API
│   ├── schemas/     # validacao dos dados
│   └── tests/       # testes automatizados do backend
├── back/mock/       # base mock para uso opcional no frontend
├── configs/         # dependencias do backend
├── docs/            # documentacao beginner e developer
└── front/           # interface web em HTML, CSS e JS puro
```

## Configuracoes principais

### 1. Ambiente Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r configs/requirements.txt
```

Dependencias principais:

- fastapi
- uvicorn[standard]
- sqlalchemy
- psycopg2-binary
- pydantic[email]
- bcrypt
- python-jose
- pytest

### 2. Banco de dados

O backend usa PostgreSQL por padrao. A conexao fica em `back/app/database/connection.py`.

Valor padrao atual:

```python
DEFAULT_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/aigenda"
```

Para sobrescrever no seu ambiente:

```bash
export DATABASE_URL="postgresql://usuario:senha@localhost:5432/aigenda"
```

### 3. Token JWT

O segredo usado no token pode ser configurado pela variavel abaixo:

```bash
export JWT_SECRET_KEY="um-segredo-forte-para-desenvolvimento"
```

Se nada for definido, o projeto usa um valor padrao de desenvolvimento em `back/app/core/security.py`.

### 4. Criacao automatica das tabelas

Ao subir a API, o projeto pode inicializar as tabelas automaticamente.

Comportamento atual:

- `APP_INIT_DB_ON_STARTUP=1`: inicializa tabelas no startup
- `APP_INIT_DB_ON_STARTUP=0`: nao inicializa tabelas no startup

### 5. Modo de autenticacao no frontend

O frontend consegue alternar entre API real e mock local em `front/js/core/configs/config.js`.

Opcoes:

- `real`: usa FastAPI em `http://127.0.0.1:8000`
- `mock`: usa JSON Server em `http://127.0.0.1:3002`

## Como executar

### Backend

```bash
uvicorn app.main:app --reload --app-dir back
```

URLs uteis:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

### Frontend

Abra `front/index.html` com Live Server ou qualquer servidor estatico local.

### Mock opcional do frontend

Use apenas se quiser testar o modo mock.

```bash
npx json-server --watch back/mock/db.json --port 3002
```

## Testes automatizados

Os testes atuais ficam em `back/app/tests` e cobrem o fluxo de autenticacao.

```bash
pytest back/app/tests -q
```

Cobertura atual:

- cadastro
- login
- rota `/auth/me`

## Endpoints implementados hoje

### Autenticacao

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Tarefas

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

### Eventos

- `POST /events`
- `GET /events`
- `GET /events/{event_id}`
- `PUT /events/{event_id}`
- `DELETE /events/{event_id}`

## Proximos passos sugeridos

1. Integrar no frontend as APIs reais de tarefas e eventos, porque o backend dessa parte ja esta pronto.
2. Criar interface visual para agenda e perfil, hoje ainda vazias ou iniciais.
3. Expandir os testes automatizados para CRUD de tarefas e eventos.
4. Centralizar configuracoes sensiveis em variaveis de ambiente e, se desejar, em um arquivo `.env` de desenvolvimento.
5. Definir a proxima camada funcional do produto, por exemplo progresso, rotina ou acompanhamento por usuario.

## Navegacao da documentacao

### Beginner

- `docs/beginner/what-is-the-project.md`
- `docs/beginner/what-functions-it-has.md`
- `docs/beginner/user-interface.md`

### Developer Back-end

- `docs/developer/back-end/auth.md`
- `docs/developer/back-end/tasks.md`
- `docs/developer/back-end/events.md`

### Developer Front-end

- `docs/developer/front-end/login.md`
- `docs/developer/front-end/register.md`
- `docs/developer/front-end/dashboard.md`
- `docs/developer/front-end/routing-and-session.md`
- `docs/developer/front-end/agenda.md`
- `docs/developer/front-end/profile.md`

