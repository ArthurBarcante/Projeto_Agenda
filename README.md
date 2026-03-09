# AIgenda

Plataforma de agendamento inteligente para equipes e empresas, com foco em confiabilidade, isolamento por tenant e escalabilidade.

## Descricao

O **AIgenda** e um sistema de gestao de compromissos para times que precisam organizar agendas com seguranca e previsibilidade.

O projeto resolve problemas comuns de operacao em ambientes corporativos:

- conflitos de horario entre participantes;
- duplicidade de requisicoes em operacoes criticas;
- isolamento de dados entre empresas (multi-tenant);
- controle de acesso por papeis e permissoes;
- rastreabilidade de eventos e acoes no sistema.

## Funcionalidades / Features

- Cadastro, atualizacao e cancelamento de compromissos.
- Prevencao automatica de conflitos de horario.
- Suporte a multiplos participantes por compromisso.
- Autenticacao via JWT.
- Controle de acesso com RBAC (roles e permissions).
- Isolamento multi-tenant por empresa.
- Idempotencia para evitar criacao duplicada em requests repetidos.
- Middleware de rate limit com suporte a Redis.
- Auditoria de eventos e padrao outbox para integracoes.
- Testes organizados em camadas (`unit`, `integration`, `e2e`).

## Tecnologias

### Backend

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Pydantic
- Uvicorn

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Qualidade

- Pytest
- ESLint

## Instalacao / Setup

### 1) Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd aigenda
```

### 2) Configurar variaveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com os valores do seu ambiente local (principalmente `DATABASE_URL`, `SECRET_KEY` e `REDIS_URL`).

### 3) Subir dependencias externas

Garanta que voce possui:

- PostgreSQL em execucao
- Redis em execucao

### 4) Setup do backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic -c alembic.ini upgrade head
uvicorn backend.main:app --reload
```

API disponivel em `http://127.0.0.1:8000`.

### 5) Setup do frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend disponivel em `http://localhost:3000`.

## Uso / Exemplos

### Endpoints principais

- `POST /auth/login`
- `POST /appointments`
- `PUT /appointments/{appointment_id}`
- `PATCH /appointments/{appointment_id}/cancel`
- `GET /me`

### Exemplo: login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
	-H "Content-Type: application/json" \
	-d '{
		"company_identifier": "acme",
		"email": "user@acme.com",
		"senha": "123456"
	}'
```

### Exemplo: criar compromisso com idempotencia

```bash
curl -X POST http://127.0.0.1:8000/appointments \
	-H "Authorization: Bearer <seu_token>" \
	-H "Content-Type: application/json" \
	-H "Idempotency-Key: 7f005748-8c8e-4f89-92ea-9d4aa5e6b220" \
	-d '{
		"titulo": "Reuniao de planejamento",
		"descricao": "Sprint semanal",
		"inicio": "2026-03-10T10:00:00Z",
		"fim": "2026-03-10T11:00:00Z",
		"participantes_ids": []
	}'
```

### Rodando testes

```bash
pytest
```

## Contribuicao

Contribuicoes sao bem-vindas.

Fluxo recomendado:

1. Crie uma branch a partir da `main`:

```bash
git checkout -b feat/minha-feature
```

2. Implemente sua alteracao com testes.
3. Execute validacoes locais (`pytest` e lint do frontend quando aplicavel).
4. Abra um Pull Request descrevendo contexto, solucao e impacto.

## Licenca

Este projeto esta sob a licenca **Apache License 2.0**. Consulte o arquivo `LICENSE` para detalhes.
