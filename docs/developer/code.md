# Estrutura de Codigo e Responsabilidades

## 1. Mapa de modulos

```text
backend/
  main.py
  app/
    api/routers/
      auth.py
      schedule.py
      tests.py
    middleware/
      tenant_middleware.py
      rate_limit_middleware.py
    dependencies/
      fastapi.py
    core/
      db/
      tenant/
      security/
      errors/
      events/
      rate_limit/
      settings/
    modules/
      schedule/
      users/
      permissions/
      idempotency/
      outbox/
      audit/
      notifications/
  tests/
    unit/
    integration/
    e2e/
```

## 2. Entry point e composicao
- `backend/main.py`:
  - instancia `FastAPI`;
  - registra middlewares globais;
  - registra error handlers;
  - registra handlers de eventos (`schedule` e `notifications`);
  - inclui roteadores principais e legados.

## 3. API Routers
### `auth.py`
- `POST /auth/login` e alias legado `/authentication/login`.
- valida company por slug + credenciais de usuario.
- emite JWT com `sub`, `company_id`, `company_slug`.

### `schedule.py`
- `POST /appointments` (com permissao `agenda.criar` e suporte idempotencia).
- `PUT /appointments/{id}` (atualizacao por autor).
- `PATCH /appointments/{id}/cancel` (cancelamento por autor).

### `tests.py`
- endpoint `GET /me` para diagnostico de autenticacao/contexto.

## 4. Dominio de Agenda
### Entidades
- `Appointment`:
  - campos principais: `title`, `description`, `start_time`, `end_time`, `status`.
  - estado: `scheduled`, `cancelled`, `completed`.
  - regras: `can_be_updated`, `can_be_cancelled`, `cancel(current_user)`.
- `AppointmentParticipant`:
  - associacao N:N entre appointments e users.
  - PK composta (`appointment_id`, `user_id`) + constraint de unicidade.

### Service
`AppointmentService` centraliza:
- checagem de conflito temporal para criador e participantes;
- controle de autoria para update/cancel;
- auditoria antes/depois;
- publicacao de evento em outbox;
- controle de transacao (`commit`, `rollback`, `refresh`).

### Repository
`AppointmentRepositoryAlias`:
- leitura por tenant;
- consulta de conflito com intervalo sobreposto (`start < end_novo` e `end > start_novo`);
- uso de `with_for_update()` na deteccao de conflito.

## 5. Seguranca e autorizacao
### Autenticacao
- JWT assinado com `HS256`.
- dependencia `get_current_user` valida token e carrega usuario no tenant correto.

### Autorizacao RBAC
- `require_permission("agenda.criar")` no endpoint de criacao.
- `PermissionService` consulta join entre `permissions`, `roles`, `role_permissions`, `user_roles`.

## 6. Multi-tenancy no codigo
- `TenantContextMiddleware` seta tenant por request autenticada.
- `TenantModel` marca entidades tenant-scoped.
- Enforcement de escopo em `core/db/session.py` para queries `SELECT` de entidades tenant-scoped.
- Repositorios de agenda exigem tenant no contexto para funcionar.

## 7. Confiabilidade
### Idempotencia
- `IdempotencyService`:
  - extrai header `Idempotency-Key`;
  - calcula hash canonico do corpo;
  - retorna resposta anterior se chave+hash coincidirem;
  - bloqueia reuse com payload diferente (409).

### Outbox
- `OutboxService` persiste evento transacional.
- `outbox_worker.processar_eventos` faz polling, dispatch e retentativa.

### Auditoria
- `AuditService` registra `dados_antes` e `dados_depois` por acao.

## 8. Sistema de eventos interno
- `EventBus` faz dispatch por `event_type`.
- registro de handlers em startup:
  - handlers de `schedule` (log de evento);
  - handlers de `notifications` (envio de webhook).

## 9. Convencoes de modelagem
- IDs UUID (geracao UUID7 no base model).
- `created_at`/`updated_at` em `BaseModel`.
- tabelas de dominio herdam `TenantModel` quando tenant-scoped.
- schemas Pydantic usam aliases para compatibilidade de payloads.

## 10. Testes e cobertura estrutural
- Unit tests: modelos, repositorio base, event bus, ambiente.
- Integration tests: conflitos, idempotencia, outbox, permissao, rate limit, tenant scope.
- E2E: estrutura preparada para cenarios completos.

## 11. Pontos de atencao para estudo
- Nomenclatura mista (pt/en) em campos e mensagens.
- Rotas legadas coexistem com rotas novas.
- Ha trechos com duplicacao aparente (bom exercicio para refatoracao guiada por testes).
