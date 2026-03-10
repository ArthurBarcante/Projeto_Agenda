# Estrutura de Pastas e Responsabilidades

## Mapa de alto nivel

```text
backend/     -> API, dominio e infraestrutura
frontend/    -> interface e experiencia do usuario
tests/       -> suites de validacao automatizada
docs/        -> documentacao funcional e tecnica
scripts/     -> automacoes auxiliares
dev_data/    -> dados locais de desenvolvimento
```

## Backend

## `backend/main.py`

Compoe a aplicacao FastAPI:

- registra middlewares globais;
- registra handlers de erro;
- registra handlers de eventos;
- inclui roteadores HTTP.

## `backend/app/api/`

Camada de entrada HTTP.

- `routers/auth.py`: login e rota legada.
- `routers/schedule.py`: criar, atualizar e cancelar compromissos.
- `routers/tests.py`: endpoint utilitario `/me`.

## `backend/app/core/`

Infraestrutura transversal.

- `db/`: sessao, base model e repositorio base.
- `security/`: hash de senha e JWT.
- `errors/`: erros customizados e serializacao de resposta de erro.
- `events/`: event bus e registro de handlers.
- `tenant/` e `tenant_scope.py`: contexto de tenant para isolamento.
- `rate_limit/`: servico de throttling com Redis.
- `settings/`: carregamento de configuracoes via ambiente.

## `backend/app/modules/`

Dominios de negocio.

- `schedule/`: appointment model, schemas, repositorio e service.
- `users/`: modelos Company e User.
- `permissions/`: RBAC (role, permission, user_role, role_permission).
- `idempotency/`: deduplicacao de requests.
- `outbox/`: eventos transacionais e worker.
- `audit/`: trilha de auditoria.
- `notifications/`: assinaturas e disparo de webhooks.

## Frontend

## `frontend/src/intelligent_organization/`

Aplicacao principal com Next App Router:

- `app/`: paginas (`/login`, `/dashboard`, `/appointments`, `/profile`).
- `features/`: organizacao por dominio de UI e servicos.
- `shared/`: cliente HTTP, endpoints, componentes e utilitarios comuns.

## `frontend/src/engagement/`

Modulo da fase 2, com componentes, hooks, paginas e servicos em JS.

## Testes

## `tests/fase_1_organizacao_inteligente/`

Cobertura da fase 1 (unit, integration e e2e).

## `tests/fase_2_engajamento/`

Cobertura da fase 2 (principalmente unit JS, com estrutura para integration/e2e).
