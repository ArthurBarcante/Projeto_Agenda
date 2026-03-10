# Escopo do Projeto

## Objetivo funcional

AIgenda e uma plataforma de agendamento corporativo com foco em seguranca e consistencia.

Escopo implementado hoje:

- autenticacao de usuarios por empresa;
- agenda com criacao, atualizacao e cancelamento;
- controle de permissao;
- isolamento multi-tenant;
- idempotencia em escrita critica;
- auditoria e outbox para eventos.

## Escopo tecnico

- backend em FastAPI + SQLAlchemy + Alembic;
- frontend em Next.js/React/TypeScript;
- Redis para rate limit;
- testes organizados por fase de produto.

## Pontos de entrada

## Backend

- `backend/main.py`
- rotas principais:
	- `POST /auth/login`
	- `POST /appointments`
	- `PUT /appointments/{id}`
	- `PATCH /appointments/{id}/cancel`
	- `GET /me`

## Frontend

- entrada app router em `frontend/src/intelligent_organization/app/`
- paginas: home, signin, dashboard, appointments e profile.

## Estrutura de alto nivel

```text
backend/   -> API, dominio, persistencia e infraestrutura
frontend/  -> interface principal e modulo de engajamento
tests/     -> suites por fase (fase_1 e fase_2)
docs/      -> documentacao para iniciantes e devs
```

## Limites atuais e roadmap

## Fase 1 (ativo)

Nucleo robusto de agenda e seguranca.

## Fase 2 (em evolucao)

Engajamento no frontend (metas, XP, consistencia).

## Fases 3 e 4 (planejadas)

Personalizacao progressiva e camada adaptativa.
frontend/src/intelligent_organization/features/authentication/ui/SignInView.tsx
frontend/src/intelligent_organization/features/users/ui/ProfileView.tsx
frontend/src/intelligent_organization/shared/api/endpoints.ts
frontend/src/intelligent_organization/shared/api/httpClient.ts
frontend/src/intelligent_organization/shared/components/PaginaBase.tsx
frontend/src/intelligent_organization/shared/lib/formatarDataHora.ts
frontend/src/intelligent_organization/shared/types/appointment.ts
frontend/src/intelligent_organization/store/README.md
frontend/src/intelligent_organization/styles/README.md
frontend/tailwind.config.ts
frontend/tsconfig.json
frontend/vitest.config.js
.gitignore
LICENSE
pyproject.toml
README.md
requirements.txt
tests/conftest.py
tests/fase_1_organizacao_inteligente/e2e/.gitkeep
tests/fase_1_organizacao_inteligente/integration/test_api_module_legacy.py
tests/fase_1_organizacao_inteligente/integration/test_appointment_cancel_service.py
tests/fase_1_organizacao_inteligente/integration/test_appointment_time_conflict_service.py
tests/fase_1_organizacao_inteligente/integration/test_database.py
tests/fase_1_organizacao_inteligente/integration/test_idempotency_appointments.py
tests/fase_1_organizacao_inteligente/integration/test_outbox_events.py
tests/fase_1_organizacao_inteligente/integration/test_permissions.py
tests/fase_1_organizacao_inteligente/integration/test_rate_limit.py
tests/fase_1_organizacao_inteligente/integration/test_routes.py
tests/fase_1_organizacao_inteligente/integration/test_services.py
tests/fase_1_organizacao_inteligente/integration/test_tenant_scope_enforcement.py
tests/fase_1_organizacao_inteligente/integration/test_webhooks.py
tests/fase_1_organizacao_inteligente/unit/test_appointment_model.py
tests/fase_1_organizacao_inteligente/unit/test_base_repository.py
tests/fase_1_organizacao_inteligente/unit/test_company_model.py
tests/fase_1_organizacao_inteligente/unit/test_env.py
tests/fase_1_organizacao_inteligente/unit/test_event_bus.py
tests/fase_1_organizacao_inteligente/unit/test_models.py
tests/fase_1_organizacao_inteligente/unit/test_utils.py
tests/fase_2_engajamento/e2e/.gitkeep
tests/fase_2_engajamento/integration/.gitkeep
tests/fase_2_engajamento/unit/agendaService.test.js
tests/fase_2_engajamento/unit/calculateStreak.test.js
tests/fase_2_engajamento/unit/calculateXP.test.js
tests/fase_2_engajamento/unit/.gitkeep
tests/fixtures.py
tests/__init__.py
tests/README.md
```

## 5. Funcao objetiva de cada arquivo (por area)

### 5.1 Raiz do projeto
- `README.md`: visao geral do sistema e instrucoes de uso.
- `LICENSE`: licenca do projeto.
- `.gitignore`: regras de arquivos ignorados pelo Git.
- `.env`: variaveis de ambiente locais (desenvolvimento).
- `.env.example`: exemplo de variaveis de ambiente.
- `requirements.txt`: dependencias Python para install rapido.
- `pyproject.toml`: configuracao principal do projeto Python (build/deps/tools).
- `alembic.ini`: configuracao do Alembic para migracoes.
- `.coverage`: artefato local com cobertura de testes.

### 5.2 CI e automacao
- `.github/workflows/`: pipelines de automacao (CI/CD).

### 5.3 Backend - bootstrap e migracoes
- `backend/main.py`: ponto de entrada da API FastAPI e composicao da aplicacao.
- `backend/alembic/env.py`: contexto Alembic para execucao de migracoes.
- `backend/alembic/script.py.mako`: template de novos arquivos de migracao.
- `backend/alembic/versions/06b0bc232d22_create_companies_table.py`: cria tabela de empresas/tenants.
- `backend/alembic/versions/37a5ff5ebbbb_standardize_database_english.py`: padroniza nomenclatura do schema para ingles.
- `backend/alembic/versions/3afa394c9de8_create_users_table.py`: cria tabela de usuarios.
- `backend/alembic/versions/3da7143a0b78_create_audit_logs_table.py`: cria tabela de trilha de auditoria.
- `backend/alembic/versions/8f2c7a1b90d4_add_appointment_conflict_indexes.py`: adiciona indices para checagem de conflito de horario.
- `backend/alembic/versions/9f31c9af0e1a_create_idempotency_keys_table.py`: cria tabela de chaves de idempotencia.
- `backend/alembic/versions/a0abcfefcde4_add_exclusion_constraint_appointments.py`: adiciona constraint de exclusao para conflitos de agenda.
- `backend/alembic/versions/b7e4c2a9d1f0_translate_database_naming_to_portuguese.py`: migra nomes do schema para portugues.
- `backend/alembic/versions/c4d8a1f2e7b9_create_outbox_events_table.py`: cria tabela de eventos outbox.
- `backend/alembic/versions/d2e6f9a4b1c3_create_rbac_tables.py`: cria tabelas de RBAC (roles/permissoes/vinculos).
- `backend/alembic/versions/e1a9d4b7c2f6_create_webhook_subscriptions_table.py`: cria tabela de assinaturas de webhook.
- `backend/alembic/versions/f3b1c9e4a2d7_standardize_database_english.py`: outra etapa de padronizacao de nomenclatura em ingles.

### 5.4 Backend - API
- `backend/app/__init__.py`: marca pacote raiz da aplicacao backend.
- `backend/app/api/routers/__init__.py`: agrega exportacoes dos roteadores.
- `backend/app/api/routers/auth.py`: endpoints de autenticacao/login.
- `backend/app/api/routers/schedule.py`: endpoints de agenda/appointments.
- `backend/app/api/routers/tests.py`: endpoints auxiliares para validacao/testes.
- `backend/app/api/versioning/__init__.py`: pacote de versionamento da API.
- `backend/app/api/versioning/v1.py`: registro da versao `v1` da API.

### 5.5 Backend - Core
- `backend/app/core/__init__.py`: pacote central de infraestrutura.
- `backend/app/core/config/__init__.py`: pacote de configuracoes auxiliares.
- `backend/app/core/config/uuid7.py`: utilitario de geracao/uso de UUIDv7.
- `backend/app/core/db/__init__.py`: pacote de infraestrutura de banco.
- `backend/app/core/db/models/__init__.py`: agregador dos modelos base.
- `backend/app/core/db/models/base.py`: base declarativa do SQLAlchemy.
- `backend/app/core/db/models/base_model.py`: modelo base com campos comuns.
- `backend/app/core/db/models/mixins.py`: mixins reutilizaveis para entidades.
- `backend/app/core/db/models/tenant_model.py`: base para entidades tenant-scoped.
- `backend/app/core/db/repositories/__init__.py`: pacote de repositorios base.
- `backend/app/core/db/repositories/base_repository.py`: CRUD/regras comuns de repositorio.
- `backend/app/core/db/session.py`: criacao e configuracao da sessao de banco.
- `backend/app/core/db/session_scope.py`: controle de escopo transacional da sessao.
- `backend/app/core/errors/api_error.py`: excecao padrao de API.
- `backend/app/core/errors/error_codes.py`: catalogo de codigos de erro.
- `backend/app/core/errors/error_handlers.py`: handlers globais de excecao.
- `backend/app/core/events/__init__.py`: pacote de eventos internos.
- `backend/app/core/events/event_bus.py`: barramento de eventos interno.
- `backend/app/core/events/event_handler_registry.py`: registro de handlers por tipo de evento.
- `backend/app/core/events/event_types.py`: definicao dos tipos de evento.
- `backend/app/core/rate_limit/__init__.py`: pacote de rate limit.
- `backend/app/core/rate_limit/rate_limit_service.py`: servico de controle de taxa.
- `backend/app/core/security/__init__.py`: pacote de seguranca.
- `backend/app/core/security/security.py`: regras utilitarias de autenticacao/autorizacao.
- `backend/app/core/security/token_jwt.py`: emissao e validacao de JWT.
- `backend/app/core/settings/__init__.py`: pacote de configuracoes aplicacionais.
- `backend/app/core/settings/settings.py`: carregamento de settings/env.
- `backend/app/core/tenant/__init__.py`: pacote de contexto multi-tenant.
- `backend/app/core/tenant/tenant_context.py`: contexto atual de tenant por request.
- `backend/app/core/tenant_scope.py`: enforcement de escopo tenant em consultas.

### 5.6 Backend - Dependencias e middleware
- `backend/app/dependencies/__init__.py`: pacote de dependencias FastAPI.
- `backend/app/dependencies/fastapi.py`: providers para DB, usuario atual, permissoes etc.
- `backend/app/middleware/__init__.py`: pacote de middlewares.
- `backend/app/middleware/rate_limit_middleware.py`: middleware global de rate limiting.
- `backend/app/middleware/tenant_middleware.py`: middleware de resolucao/propagacao de tenant.

### 5.7 Backend - Modulos de negocio
- `backend/app/modules/audit/__init__.py`: pacote do modulo de auditoria.
- `backend/app/modules/audit/repositories/__init__.py`: pacote de repositorio de auditoria.
- `backend/app/modules/audit/repositories/audit_repository.py`: persistencia dos registros de auditoria.
- `backend/app/modules/audit/services/__init__.py`: pacote de servico de auditoria.
- `backend/app/modules/audit/services/audit_service.py`: orquestra criacao de trilha de auditoria.
- `backend/app/modules/idempotency/__init__.py`: pacote de idempotencia.
- `backend/app/modules/idempotency/repositories/__init__.py`: pacote de repositorio de idempotencia.
- `backend/app/modules/idempotency/repositories/idempotency_repository.py`: acesso a chaves/respostas idempotentes.
- `backend/app/modules/idempotency/services/__init__.py`: pacote de servico de idempotencia.
- `backend/app/modules/idempotency/services/idempotency_service.py`: valida/reaproveita requests idempotentes.
- `backend/app/modules/notifications/events/__init__.py`: pacote de eventos de notificacao.
- `backend/app/modules/notifications/events/webhook_event_handler.py`: handler de evento para disparo de webhook.
- `backend/app/modules/notifications/models/__init__.py`: pacote de modelos de notificacao.
- `backend/app/modules/notifications/models/audit_log.py`: modelo de log de auditoria no contexto de notificacoes.
- `backend/app/modules/notifications/models/webhook_subscription.py`: modelo de assinatura de webhook.
- `backend/app/modules/notifications/repositories/__init__.py`: pacote de repositorio de notificacoes.
- `backend/app/modules/notifications/repositories/webhook_repository.py`: acesso a assinaturas de webhook.
- `backend/app/modules/notifications/services/__init__.py`: pacote de servico de notificacoes.
- `backend/app/modules/notifications/services/webhook_service.py`: envio/gestao de webhooks.
- `backend/app/modules/outbox/__init__.py`: pacote do modulo outbox.
- `backend/app/modules/outbox/models/__init__.py`: pacote de modelos de outbox.
- `backend/app/modules/outbox/models/idempotency_key.py`: modelo de chave idempotente.
- `backend/app/modules/outbox/models/outbox_event.py`: modelo do evento persistido em outbox.
- `backend/app/modules/outbox/repositories/__init__.py`: pacote de repositorio de outbox.
- `backend/app/modules/outbox/repositories/outbox_repository.py`: acesso/leitura/escrita de eventos outbox.
- `backend/app/modules/outbox/services/__init__.py`: pacote de servico de outbox.
- `backend/app/modules/outbox/services/outbox_service.py`: grava eventos transacionais no outbox.
- `backend/app/modules/outbox/workers/__init__.py`: pacote de workers de outbox.
- `backend/app/modules/outbox/workers/outbox_worker.py`: worker de processamento/publicacao de eventos pendentes.
- `backend/app/modules/permissions/__init__.py`: pacote de autorizacao RBAC.
- `backend/app/modules/permissions/models/__init__.py`: pacote de modelos RBAC.
- `backend/app/modules/permissions/models/permission.py`: modelo de permissao.
- `backend/app/modules/permissions/models/role.py`: modelo de papel (role).
- `backend/app/modules/permissions/models/role_permission.py`: modelo de relacao role-permission.
- `backend/app/modules/permissions/models/user_role.py`: modelo de relacao user-role.
- `backend/app/modules/permissions/repositories/__init__.py`: pacote de repositorio RBAC.
- `backend/app/modules/permissions/repositories/role_repository.py`: consulta de roles/permissoes.
- `backend/app/modules/permissions/services/__init__.py`: pacote de servico RBAC.
- `backend/app/modules/permissions/services/permission_service.py`: validacao de permissao por usuario.
- `backend/app/modules/schedule/events/__init__.py`: pacote de eventos do dominio agenda.
- `backend/app/modules/schedule/events/handlers/appointment_cancelled_handler.py`: handler para evento de cancelamento.
- `backend/app/modules/schedule/events/handlers/appointment_created_handler.py`: handler para evento de criacao.
- `backend/app/modules/schedule/models/appointment.py`: entidade principal de compromisso.
- `backend/app/modules/schedule/models/appointment_participant.py`: entidade de participantes do compromisso.
- `backend/app/modules/schedule/repositories/appointment_repository.py`: consultas/regras de persistencia de agenda.
- `backend/app/modules/schedule/schemas/__init__.py`: pacote de schemas do modulo agenda.
- `backend/app/modules/schedule/schemas/appointment.py`: DTOs de request/response de appointments.
- `backend/app/modules/schedule/services/__init__.py`: pacote de servicos do modulo agenda.
- `backend/app/modules/schedule/services/appointment_service.py`: regras de negocio de criacao/edicao/cancelamento.
- `backend/app/modules/users/models/company.py`: modelo de empresa/tenant.
- `backend/app/modules/users/models/user.py`: modelo de usuario.

### 5.8 Dados locais e migracoes auxiliares
- `dev_data/aigenda.db`: banco local (SQLite) para execucao em dev.
- `dev_data/migrations/README.md`: orientacoes para dados/migracoes locais.

### 5.9 Documentacao
- `docs/beginner/overview.md`: visao inicial para novos colaboradores.
- `docs/beginner/features.md`: resumo das funcionalidades.
- `docs/beginner/workflow.md`: fluxo de trabalho para iniciantes.
- `docs/beginner/architecture.md`: arquitetura explicada em nivel introdutorio.
- `docs/beginner/glossary.md`: glossario de termos do projeto.
- `docs/developer/setup.md`: setup tecnico de ambiente.
- `docs/developer/architecture.md`: arquitetura tecnica detalhada.
- `docs/developer/api.md`: contratos/endpoints de API.
- `docs/developer/code.md`: organizacao do codigo e responsabilidades.
- `docs/developer/performance.md`: consideracoes de performance.
- `docs/developer/workflow.md`: fluxo de desenvolvimento para equipe tecnica.

### 5.10 Frontend - configuracao e assets
- `frontend/.gitignore`: regras locais de ignorados do frontend.
- `frontend/package.json`: scripts e dependencias NPM.
- `frontend/package-lock.json`: lockfile das dependencias.
- `frontend/tsconfig.json`: configuracao TypeScript.
- `frontend/next.config.ts`: configuracao do Next.js.
- `frontend/next-env.d.ts`: tipos gerados para ambiente Next.
- `frontend/tailwind.config.ts`: configuracao do Tailwind.
- `frontend/postcss.config.mjs`: plugins PostCSS.
- `frontend/eslint.config.mjs`: regras de lint JS/TS.
- `frontend/vitest.config.js`: configuracao de testes front com Vitest.
- `frontend/public/file.svg`: asset estatico SVG.
- `frontend/public/globe.svg`: asset estatico SVG.
- `frontend/public/next.svg`: asset estatico SVG.
- `frontend/public/vercel.svg`: asset estatico SVG.
- `frontend/public/window.svg`: asset estatico SVG.

### 5.11 Frontend - modulo engagement (fase 2)
- `frontend/src/engagement/data/mockData.js`: dados mock para telas de engajamento.
- `frontend/src/engagement/services/agendaService.js`: servico de dados da agenda no modulo engagement.
- `frontend/src/engagement/hooks/useConsistence.js`: hook de consistencia.
- `frontend/src/engagement/hooks/useMetas.js`: hook de metas.
- `frontend/src/engagement/hooks/usePerformance.js`: hook de performance.
- `frontend/src/engagement/hooks/useXP.js`: hook de pontuacao XP.
- `frontend/src/engagement/utils/calculateMetrics.js`: calculo de metricas agregadas.
- `frontend/src/engagement/utils/calculateStreak.js`: calculo de streak/consistencia.
- `frontend/src/engagement/utils/calculateXP.js`: calculo de pontuacao XP.
- `frontend/src/engagement/components/cards/MetaCard.jsx`: card de meta.
- `frontend/src/engagement/components/cards/MetricCard.jsx`: card de metrica.
- `frontend/src/engagement/components/cards/XPCard.jsx`: card de XP.
- `frontend/src/engagement/components/feedback/XpToast.jsx`: feedback visual de ganho XP.
- `frontend/src/engagement/components/progress/ProgressBar.jsx`: barra de progresso.
- `frontend/src/engagement/pages/Agenda/index.jsx`: pagina de agenda do modulo.
- `frontend/src/engagement/pages/Consistence/index.jsx`: pagina de consistencia.
- `frontend/src/engagement/pages/Metas/index.jsx`: pagina de metas.
- `frontend/src/engagement/pages/Perfomance/index.jsx`: pagina de performance.

### 5.12 Frontend - modulo intelligent_organization
- `frontend/src/intelligent_organization/app/layout.tsx`: layout raiz do app router.
- `frontend/src/intelligent_organization/app/page.tsx`: pagina inicial.
- `frontend/src/intelligent_organization/app/globals.css`: estilos globais.
- `frontend/src/intelligent_organization/app/favicon.ico`: icone do app.
- `frontend/src/intelligent_organization/app/(auth)/signin/page.tsx`: rota de login.
- `frontend/src/intelligent_organization/app/(dashboard)/dashboard/page.tsx`: rota de dashboard.
- `frontend/src/intelligent_organization/app/(dashboard)/appointments/page.tsx`: rota de appointments.
- `frontend/src/intelligent_organization/app/(dashboard)/profile/page.tsx`: rota de perfil.
- `frontend/src/intelligent_organization/features/appointments/hooks/use_appointments.ts`: hook de appointments.
- `frontend/src/intelligent_organization/features/appointments/services/appointments_service.ts`: client de servico de appointments.
- `frontend/src/intelligent_organization/features/appointments/types/appointment.ts`: tipos de appointments.
- `frontend/src/intelligent_organization/features/appointments/ui/AppointmentsView.tsx`: view de listagem/gestao de appointments.
- `frontend/src/intelligent_organization/features/appointments/ui/DashboardView.tsx`: view de dashboard de appointments.
- `frontend/src/intelligent_organization/features/authentication/services/authentication_service.ts`: servico de autenticacao.
- `frontend/src/intelligent_organization/features/authentication/types/authentication.ts`: tipos de autenticacao.
- `frontend/src/intelligent_organization/features/authentication/ui/SignInView.tsx`: tela/componente de login.
- `frontend/src/intelligent_organization/features/users/ui/ProfileView.tsx`: tela/componente de perfil do usuario.
- `frontend/src/intelligent_organization/shared/api/endpoints.ts`: mapa central de endpoints.
- `frontend/src/intelligent_organization/shared/api/httpClient.ts`: cliente HTTP compartilhado.
- `frontend/src/intelligent_organization/shared/components/PaginaBase.tsx`: componente base de pagina.
- `frontend/src/intelligent_organization/shared/lib/formatarDataHora.ts`: utilitario de formatacao de data/hora.
- `frontend/src/intelligent_organization/shared/types/appointment.ts`: tipos compartilhados de appointment.
- `frontend/src/intelligent_organization/store/README.md`: orientacoes da camada de estado/store.
- `frontend/src/intelligent_organization/styles/README.md`: orientacoes para organizacao de estilos.

### 5.13 Testes
- `tests/__init__.py`: marca pacote de testes.
- `tests/conftest.py`: fixtures e setup global do pytest.
- `tests/fixtures.py`: fixtures reutilizaveis entre suites.
- `tests/README.md`: guia de execucao e organizacao dos testes.
- `tests/fase_1_organizacao_inteligente/e2e/.gitkeep`: mantem pasta E2E no controle de versao.
- `tests/fase_1_organizacao_inteligente/integration/test_api_module_legacy.py`: integra API/modulo legado.
- `tests/fase_1_organizacao_inteligente/integration/test_appointment_cancel_service.py`: integra regra de cancelamento de appointment.
- `tests/fase_1_organizacao_inteligente/integration/test_appointment_time_conflict_service.py`: integra regra de conflito de horario.
- `tests/fase_1_organizacao_inteligente/integration/test_database.py`: validacoes de banco e integridade.
- `tests/fase_1_organizacao_inteligente/integration/test_idempotency_appointments.py`: integra idempotencia em appointments.
- `tests/fase_1_organizacao_inteligente/integration/test_outbox_events.py`: integra fluxo de eventos outbox.
- `tests/fase_1_organizacao_inteligente/integration/test_permissions.py`: integra regras de permissao RBAC.
- `tests/fase_1_organizacao_inteligente/integration/test_rate_limit.py`: integra limitacao de taxa.
- `tests/fase_1_organizacao_inteligente/integration/test_routes.py`: integra contratos de rotas.
- `tests/fase_1_organizacao_inteligente/integration/test_services.py`: integra servicos principais.
- `tests/fase_1_organizacao_inteligente/integration/test_tenant_scope_enforcement.py`: integra isolamento multi-tenant.
- `tests/fase_1_organizacao_inteligente/integration/test_webhooks.py`: integra envio/disparo de webhooks.
- `tests/fase_1_organizacao_inteligente/unit/test_appointment_model.py`: unidade da entidade appointment.
- `tests/fase_1_organizacao_inteligente/unit/test_base_repository.py`: unidade do repositorio base.
- `tests/fase_1_organizacao_inteligente/unit/test_company_model.py`: unidade do modelo de company.
- `tests/fase_1_organizacao_inteligente/unit/test_env.py`: unidade de carregamento de ambiente/config.
- `tests/fase_1_organizacao_inteligente/unit/test_event_bus.py`: unidade do barramento de eventos.
- `tests/fase_1_organizacao_inteligente/unit/test_models.py`: unidade de modelos gerais.
- `tests/fase_1_organizacao_inteligente/unit/test_utils.py`: unidade de utilitarios.
- `tests/fase_2_engajamento/e2e/.gitkeep`: mantem pasta E2E da fase 2.
- `tests/fase_2_engajamento/integration/.gitkeep`: mantem pasta de integracao da fase 2.
- `tests/fase_2_engajamento/unit/.gitkeep`: mantem pasta unit da fase 2.
- `tests/fase_2_engajamento/unit/agendaService.test.js`: unidade do servico de agenda (frontend engagement).
- `tests/fase_2_engajamento/unit/calculateStreak.test.js`: unidade do calculo de streak.
- `tests/fase_2_engajamento/unit/calculateXP.test.js`: unidade do calculo de XP.

## 6. Observacao de manutencao
- Arquivos `__init__.py` listados no projeto marcam pacotes Python e, em alguns casos, centralizam exportacoes.
- Arquivos `.gitkeep` existem apenas para manter pastas vazias versionadas.
