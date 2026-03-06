# Estrutura do Projeto — AIgenda

Este documento foi atualizado para refletir a árvore atual do projeto e resumir a função de cada pasta e arquivo.

## 1) Árvore completa do projeto (código e configuração)

> Observação: a árvore abaixo exclui apenas conteúdo pesado/gerado (`.venv`, `.pytest_cache`, `frontend/node_modules`, `frontend/.next`, e `__pycache__`) para manter legibilidade.

```text
aigenda/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   │   ├── 06b0bc232d22_criar_tabela_empresas.py
│   │   │   ├── 37a5ff5ebbbb_standardize_database_english.py
│   │   │   ├── 3afa394c9de8_criar_tabela_usuarios.py
│   │   │   ├── 3da7143a0b78_criar_tabela_audit_logs.py
│   │   │   ├── 8f2c7a1b90d4_adicionar_indices_conflito_compromissos.py
│   │   │   ├── 9f31c9af0e1a_criar_tabela_idempotency_keys.py
│   │   │   ├── a0abcfefcde4_adicionar_exclusion_constraint_.py
│   │   │   ├── b7e4c2a9d1f0_traduz_nomenclatura_banco_para_portugues.py
│   │   │   ├── c4d8a1f2e7b9_criar_tabela_outbox_events.py
│   │   │   ├── d2e6f9a4b1c3_criar_tabelas_rbac.py
│   │   │   ├── e1a9d4b7c2f6_criar_tabela_webhook_subscriptions.py
│   │   │   └── f3b1c9e4a2d7_standardize_database_english.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/
│   │   │   ├── agenda/
│   │   │   │   ├── __init__.py
│   │   │   │   └── compromissos.py
│   │   │   ├── autenticacao/
│   │   │   │   ├── __init__.py
│   │   │   │   └── autenticacao.py
│   │   │   ├── compromissos/
│   │   │   │   ├── __init__.py
│   │   │   │   └── compromissos.py
│   │   │   ├── testes/
│   │   │   │   └── testes.py
│   │   │   └── dependencias.py
│   │   ├── core/
│   │   │   ├── autenticacao/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── seguranca.py
│   │   │   │   └── token_jwt.py
│   │   │   ├── config/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── configuracoes.py
│   │   │   │   └── uuid7.py
│   │   │   ├── errors/
│   │   │   │   ├── api_error.py
│   │   │   │   ├── error_codes.py
│   │   │   │   └── error_handlers.py
│   │   │   ├── events/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── event_bus.py
│   │   │   │   ├── event_handler_registry.py
│   │   │   │   └── event_types.py
│   │   │   ├── rate_limit/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── rate_limit_middleware.py
│   │   │   │   └── rate_limit_service.py
│   │   │   ├── tenant/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── tenant_context.py
│   │   │   │   └── tenant_middleware.py
│   │   │   ├── __init__.py
│   │   │   └── inquilino.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── sessao.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── appointment.py
│   │   │   ├── appointment_participant.py
│   │   │   ├── audit_log.py
│   │   │   ├── base.py
│   │   │   ├── base_model.py
│   │   │   ├── company.py
│   │   │   ├── compromisso.py
│   │   │   ├── empresa.py
│   │   │   ├── idempotency_key.py
│   │   │   ├── mixins.py
│   │   │   ├── participante_compromisso.py
│   │   │   ├── tenant_model.py
│   │   │   ├── user.py
│   │   │   └── usuario.py
│   │   ├── modules/
│   │   │   ├── agenda/
│   │   │   │   ├── api/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── compromissos.py
│   │   │   │   ├── events/
│   │   │   │   │   ├── handlers/
│   │   │   │   │   │   ├── compromisso_cancelado_handler.py
│   │   │   │   │   │   └── compromisso_criado_handler.py
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── compromisso_repository.py
│   │   │   │   ├── schemas/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── compromisso.py
│   │   │   │   │   └── compromisso_legado.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── compromisso_service.py
│   │   │   │   │   └── servico_compromisso.py
│   │   │   │   └── __init__.py
│   │   │   ├── auditoria/
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── audit_repository.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── audit_service.py
│   │   │   │   └── __init__.py
│   │   │   ├── auth/
│   │   │   │   ├── api/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── autenticacao.py
│   │   │   │   ├── repositories/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── schemas/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   ├── companies/
│   │   │   ├── compromissos/
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── compromisso_service.py
│   │   │   │   └── __init__.py
│   │   │   ├── empresas/
│   │   │   │   ├── api/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── repositories/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── schemas/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   ├── idempotency/
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── idempotency_repository.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── idempotency_service.py
│   │   │   │   └── __init__.py
│   │   │   ├── outbox/
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── outbox_event.py
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── outbox_repository.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── outbox_service.py
│   │   │   │   ├── workers/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── outbox_worker.py
│   │   │   │   └── __init__.py
│   │   │   ├── permissoes/
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── permission.py
│   │   │   │   │   ├── role.py
│   │   │   │   │   ├── role_permission.py
│   │   │   │   │   └── user_role.py
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── role_repository.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── permission_service.py
│   │   │   │   └── __init__.py
│   │   │   ├── schedule/
│   │   │   │   ├── schemas/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── appointment.py
│   │   │   │   └── services/
│   │   │   │       ├── __init__.py
│   │   │   │       └── appointment_service.py
│   │   │   ├── testes/
│   │   │   │   ├── api/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── testes.py
│   │   │   │   └── __init__.py
│   │   │   ├── users/
│   │   │   ├── usuarios/
│   │   │   │   ├── api/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── repositories/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── schemas/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   └── webhooks/
│   │   │       ├── events/
│   │   │       │   ├── __init__.py
│   │   │       │   └── webhook_event_handler.py
│   │   │       ├── models/
│   │   │       │   ├── __init__.py
│   │   │       │   └── webhook_subscription.py
│   │   │       ├── repositories/
│   │   │       │   ├── __init__.py
│   │   │       │   └── webhook_repository.py
│   │   │       └── services/
│   │   │           ├── __init__.py
│   │   │           └── webhook_service.py
│   │   ├── repositories/
│   │   │   └── __init__.py
│   │   ├── repositorios/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── base_repository.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── appointment.py
│   │   │   ├── compromisso.py
│   │   │   └── compromisso_legado.py
│   │   ├── services/
│   │   ├── utils/
│   │   ├── __init__.py
│   │   └── principal.py
│   └── aigenda.db
├── config/
│   ├── .env
│   ├── .gitignore
│   ├── alembic.ini
│   └── requirements.txt
├── docs/
│   ├── estrutura-do-projeto.md
│   ├── fase-1-frontend.md
│   ├── fase-1.md
│   └── funcionalidades-futuras.md
├── frontend/
│   ├── public/
│   │   ├── file.svg
│   │   ├── globe.svg
│   │   ├── next.svg
│   │   ├── vercel.svg
│   │   └── window.svg
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   └── entrar/
│   │   │   │       └── page.tsx
│   │   │   ├── (dashboard)/
│   │   │   │   ├── compromissos/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── painel/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── perfil/
│   │   │   │       └── page.tsx
│   │   │   ├── favicon.ico
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── features/
│   │   │   ├── autenticacao/
│   │   │   │   ├── services/
│   │   │   │   │   └── autenticacaoService.ts
│   │   │   │   ├── types/
│   │   │   │   │   └── autenticacao.ts
│   │   │   │   └── ui/
│   │   │   │       └── EntrarView.tsx
│   │   │   ├── compromissos/
│   │   │   │   ├── hooks/
│   │   │   │   │   └── useCompromissos.ts
│   │   │   │   ├── services/
│   │   │   │   │   └── compromissosService.ts
│   │   │   │   ├── types/
│   │   │   │   │   └── compromisso.ts
│   │   │   │   └── ui/
│   │   │   │       ├── CompromissosView.tsx
│   │   │   │       └── PainelView.tsx
│   │   │   └── usuarios/
│   │   │       └── ui/
│   │   │           └── PerfilView.tsx
│   │   ├── shared/
│   │   │   ├── api/
│   │   │   │   ├── endpoints.ts
│   │   │   │   └── httpClient.ts
│   │   │   ├── components/
│   │   │   │   └── PaginaBase.tsx
│   │   │   ├── lib/
│   │   │   │   └── formatarDataHora.ts
│   │   │   └── types/
│   │   │       └── compromisso.ts
│   │   ├── store/
│   │   │   └── README.md
│   │   └── styles/
│   │       └── README.md
│   ├── .gitignore
│   ├── eslint.config.mjs
│   ├── next-env.d.ts
│   ├── next.config.ts
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── tests/
│   ├── conftest.py
│   ├── test_appointment_cancel_service.py
│   ├── test_appointment_model.py
│   ├── test_appointment_time_conflict_service.py
│   ├── test_base_repository.py
│   ├── test_company_model.py
│   ├── test_env.py
│   ├── test_event_bus.py
│   ├── test_idempotency_appointments.py
│   ├── test_outbox_events.py
│   ├── test_permissions.py
│   ├── test_rate_limit.py
│   ├── test_tenant_scope_enforcement.py
│   └── test_webhooks.py
├── .gitignore
└── README.md
```

## 2) Pastas/arquivos gerados localmente (fora da árvore acima)

- `.venv/`: ambiente virtual Python local (dependências instaladas).
- `.pytest_cache/`: cache de execução do pytest.
- `frontend/node_modules/`: dependências npm instaladas localmente.
- `frontend/.next/`: artefatos de build e cache do Next.js.
- `**/__pycache__/`: bytecode Python gerado automaticamente.

## 3) Função resumida de cada pasta e arquivo

### Raiz

- `backend/`: backend FastAPI, domínio, modelos e migrações.
- `config/`: configuração de ambiente e dependências Python.
- `docs/`: documentação funcional e técnica.
- `frontend/`: aplicação web Next.js.
- `tests/`: suíte de testes automatizados do backend.
- `.gitignore`: regras globais de ignorados do repositório.
- `README.md`: visão geral do projeto e instruções de uso.

### backend/

- `backend/aigenda.db`: banco SQLite local de desenvolvimento.

#### backend/alembic/

- `backend/alembic/`: infraestrutura de migrações de banco.
- `backend/alembic/env.py`: contexto e configuração do Alembic.
- `backend/alembic/script.py.mako`: template padrão para novas migrações.
- `backend/alembic/versions/`: histórico de versões de schema.
- `backend/alembic/versions/06b0bc232d22_criar_tabela_empresas.py`: cria tabela de empresas.
- `backend/alembic/versions/37a5ff5ebbbb_standardize_database_english.py`: padroniza nomes de schema para inglês.
- `backend/alembic/versions/3afa394c9de8_criar_tabela_usuarios.py`: cria tabela de usuários.
- `backend/alembic/versions/3da7143a0b78_criar_tabela_audit_logs.py`: cria tabela de auditoria.
- `backend/alembic/versions/8f2c7a1b90d4_adicionar_indices_conflito_compromissos.py`: adiciona índices para conflitos de agenda.
- `backend/alembic/versions/9f31c9af0e1a_criar_tabela_idempotency_keys.py`: cria tabela de chaves de idempotência.
- `backend/alembic/versions/a0abcfefcde4_adicionar_exclusion_constraint_.py`: adiciona constraint de exclusão para conflitos temporais.
- `backend/alembic/versions/b7e4c2a9d1f0_traduz_nomenclatura_banco_para_portugues.py`: migração de nomenclatura para português.
- `backend/alembic/versions/c4d8a1f2e7b9_criar_tabela_outbox_events.py`: cria tabela de eventos de outbox.
- `backend/alembic/versions/d2e6f9a4b1c3_criar_tabelas_rbac.py`: cria tabelas de RBAC (papéis e permissões).
- `backend/alembic/versions/e1a9d4b7c2f6_criar_tabela_webhook_subscriptions.py`: cria tabela de inscrições de webhook.
- `backend/alembic/versions/f3b1c9e4a2d7_standardize_database_english.py`: padronização adicional de schema em inglês.

#### backend/app/

- `backend/app/`: pacote principal da aplicação FastAPI.
- `backend/app/__init__.py`: inicialização do pacote `app`.
- `backend/app/principal.py`: bootstrap da aplicação e registro de rotas.

##### backend/app/api/

- `backend/app/api/`: camada HTTP (endpoints e dependências).
- `backend/app/api/dependencias.py`: dependências compartilhadas das rotas.
- `backend/app/api/agenda/`: endpoints de agenda.
- `backend/app/api/agenda/__init__.py`: inicialização do submódulo de agenda.
- `backend/app/api/agenda/compromissos.py`: rotas de compromissos da agenda.
- `backend/app/api/autenticacao/`: endpoints de autenticação.
- `backend/app/api/autenticacao/__init__.py`: inicialização do submódulo de autenticação.
- `backend/app/api/autenticacao/autenticacao.py`: rotas de login/autorização.
- `backend/app/api/compromissos/`: endpoints dedicados de compromissos.
- `backend/app/api/compromissos/__init__.py`: inicialização do submódulo.
- `backend/app/api/compromissos/compromissos.py`: rotas CRUD de compromissos.
- `backend/app/api/testes/`: endpoints utilitários de teste.
- `backend/app/api/testes/testes.py`: rotas de verificação e diagnóstico.

##### backend/app/core/

- `backend/app/core/`: componentes centrais transversais (segurança, config, eventos, erros, tenant).
- `backend/app/core/__init__.py`: inicialização do pacote core.
- `backend/app/core/inquilino.py`: utilitários de contexto de inquilino/tenant.
- `backend/app/core/autenticacao/`: núcleo de autenticação.
- `backend/app/core/autenticacao/__init__.py`: inicialização do subpacote.
- `backend/app/core/autenticacao/seguranca.py`: regras de segurança e autorização.
- `backend/app/core/autenticacao/token_jwt.py`: criação/validação de tokens JWT.
- `backend/app/core/config/`: configurações globais da aplicação.
- `backend/app/core/config/__init__.py`: inicialização de configuração.
- `backend/app/core/config/configuracoes.py`: leitura e validação de settings.
- `backend/app/core/config/uuid7.py`: utilitários para UUIDv7.
- `backend/app/core/errors/`: tratamento padronizado de erros da API.
- `backend/app/core/errors/api_error.py`: exceções de domínio/API.
- `backend/app/core/errors/error_codes.py`: catálogo de códigos de erro.
- `backend/app/core/errors/error_handlers.py`: handlers de exceções para respostas HTTP.
- `backend/app/core/events/`: infraestrutura de eventos internos.
- `backend/app/core/events/__init__.py`: inicialização do subpacote de eventos.
- `backend/app/core/events/event_bus.py`: barramento de publicação/assinatura de eventos.
- `backend/app/core/events/event_handler_registry.py`: registro de handlers por tipo de evento.
- `backend/app/core/events/event_types.py`: definição de tipos/contratos de eventos.
- `backend/app/core/rate_limit/`: componentes de limitação de taxa.
- `backend/app/core/rate_limit/__init__.py`: inicialização do subpacote.
- `backend/app/core/rate_limit/rate_limit_middleware.py`: middleware de rate limiting.
- `backend/app/core/rate_limit/rate_limit_service.py`: serviço de cálculo e validação de limite.
- `backend/app/core/tenant/`: componentes formais de multi-tenant.
- `backend/app/core/tenant/__init__.py`: inicialização do subpacote.
- `backend/app/core/tenant/tenant_context.py`: contexto ativo de tenant por requisição.
- `backend/app/core/tenant/tenant_middleware.py`: middleware de resolução/aplicação de tenant.

##### backend/app/db/

- `backend/app/db/`: acesso a banco e sessão ORM.
- `backend/app/db/__init__.py`: inicialização do pacote db.
- `backend/app/db/sessao.py`: configuração de sessão/engine (nomenclatura PT).
- `backend/app/db/session.py`: configuração de sessão/engine (nomenclatura EN).

##### backend/app/models/

- `backend/app/models/`: modelos ORM de persistência.
- `backend/app/models/appointment.py`: entidade de compromisso (EN).
- `backend/app/models/appointment_participant.py`: vínculo compromisso-participante (EN).
- `backend/app/models/audit_log.py`: entidade de logs de auditoria.
- `backend/app/models/base.py`: base declarativa ORM.
- `backend/app/models/base_model.py`: classe base comum de modelos.
- `backend/app/models/company.py`: entidade de empresa (EN).
- `backend/app/models/compromisso.py`: entidade de compromisso (PT).
- `backend/app/models/empresa.py`: entidade de empresa (PT).
- `backend/app/models/idempotency_key.py`: entidade de chave de idempotência.
- `backend/app/models/mixins.py`: mixins reutilizáveis para modelos.
- `backend/app/models/participante_compromisso.py`: vínculo compromisso-participante (PT).
- `backend/app/models/tenant_model.py`: base de modelo com escopo de tenant.
- `backend/app/models/user.py`: entidade de usuário (EN).
- `backend/app/models/usuario.py`: entidade de usuário (PT).

##### backend/app/modules/

- `backend/app/modules/`: módulos de domínio por contexto de negócio.
- `backend/app/modules/agenda/`: domínio de agenda/compromissos.
- `backend/app/modules/agenda/__init__.py`: inicialização do módulo.
- `backend/app/modules/agenda/api/`: rotas do módulo agenda.
- `backend/app/modules/agenda/api/__init__.py`: inicialização do subpacote API.
- `backend/app/modules/agenda/api/compromissos.py`: endpoints do módulo agenda.
- `backend/app/modules/agenda/events/`: eventos do módulo agenda.
- `backend/app/modules/agenda/events/__init__.py`: inicialização de eventos.
- `backend/app/modules/agenda/events/handlers/`: handlers de eventos da agenda.
- `backend/app/modules/agenda/events/handlers/compromisso_cancelado_handler.py`: handler de cancelamento de compromisso.
- `backend/app/modules/agenda/events/handlers/compromisso_criado_handler.py`: handler de criação de compromisso.
- `backend/app/modules/agenda/repositories/`: persistência da agenda.
- `backend/app/modules/agenda/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/agenda/repositories/compromisso_repository.py`: repositório de compromissos.
- `backend/app/modules/agenda/schemas/`: contratos de entrada/saída da agenda.
- `backend/app/modules/agenda/schemas/__init__.py`: inicialização do subpacote.
- `backend/app/modules/agenda/schemas/compromisso.py`: schema principal de compromisso.
- `backend/app/modules/agenda/schemas/compromisso_legado.py`: schema legado de compromisso.
- `backend/app/modules/agenda/services/`: serviços de negócio da agenda.
- `backend/app/modules/agenda/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/agenda/services/compromisso_service.py`: serviço de compromisso.
- `backend/app/modules/agenda/services/servico_compromisso.py`: serviço legado/alternativo de compromisso.
- `backend/app/modules/auditoria/`: domínio de auditoria.
- `backend/app/modules/auditoria/__init__.py`: inicialização do módulo.
- `backend/app/modules/auditoria/repositories/`: persistência de logs.
- `backend/app/modules/auditoria/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/auditoria/repositories/audit_repository.py`: repositório de auditoria.
- `backend/app/modules/auditoria/services/`: regras de auditoria.
- `backend/app/modules/auditoria/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/auditoria/services/audit_service.py`: serviço de auditoria.
- `backend/app/modules/auth/`: domínio de autenticação modular.
- `backend/app/modules/auth/__init__.py`: inicialização do módulo.
- `backend/app/modules/auth/api/`: API do módulo auth.
- `backend/app/modules/auth/api/__init__.py`: inicialização do subpacote.
- `backend/app/modules/auth/api/autenticacao.py`: endpoints de autenticação no módulo.
- `backend/app/modules/auth/repositories/`: repositórios do módulo auth.
- `backend/app/modules/auth/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/auth/schemas/`: schemas do módulo auth.
- `backend/app/modules/auth/schemas/__init__.py`: inicialização do subpacote.
- `backend/app/modules/auth/services/`: serviços do módulo auth.
- `backend/app/modules/auth/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/companies/`: pasta reservada para módulo em inglês (estrutura em evolução).
- `backend/app/modules/compromissos/`: domínio de compromissos (estrutura paralela).
- `backend/app/modules/compromissos/__init__.py`: inicialização do módulo.
- `backend/app/modules/compromissos/services/`: serviços deste domínio.
- `backend/app/modules/compromissos/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/compromissos/services/compromisso_service.py`: serviço de compromissos.
- `backend/app/modules/empresas/`: domínio de empresas (PT).
- `backend/app/modules/empresas/__init__.py`: inicialização do módulo.
- `backend/app/modules/empresas/api/`: endpoints de empresas.
- `backend/app/modules/empresas/api/__init__.py`: inicialização do subpacote.
- `backend/app/modules/empresas/repositories/`: repositórios de empresas.
- `backend/app/modules/empresas/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/empresas/schemas/`: schemas de empresas.
- `backend/app/modules/empresas/schemas/__init__.py`: inicialização do subpacote.
- `backend/app/modules/empresas/services/`: serviços de empresas.
- `backend/app/modules/empresas/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/idempotency/`: domínio de idempotência.
- `backend/app/modules/idempotency/__init__.py`: inicialização do módulo.
- `backend/app/modules/idempotency/repositories/`: persistência de chaves idempotentes.
- `backend/app/modules/idempotency/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/idempotency/repositories/idempotency_repository.py`: repositório de idempotência.
- `backend/app/modules/idempotency/services/`: serviços de idempotência.
- `backend/app/modules/idempotency/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/idempotency/services/idempotency_service.py`: lógica de idempotência de requisições.
- `backend/app/modules/outbox/`: domínio de outbox/eventos assíncronos.
- `backend/app/modules/outbox/__init__.py`: inicialização do módulo.
- `backend/app/modules/outbox/models/`: modelos do outbox.
- `backend/app/modules/outbox/models/__init__.py`: inicialização do subpacote.
- `backend/app/modules/outbox/models/outbox_event.py`: entidade de evento pendente/publicável.
- `backend/app/modules/outbox/repositories/`: persistência de eventos de outbox.
- `backend/app/modules/outbox/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/outbox/repositories/outbox_repository.py`: repositório de outbox.
- `backend/app/modules/outbox/services/`: regras de outbox.
- `backend/app/modules/outbox/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/outbox/services/outbox_service.py`: serviço para registrar/publicar eventos.
- `backend/app/modules/outbox/workers/`: processamento assíncrono de outbox.
- `backend/app/modules/outbox/workers/__init__.py`: inicialização do subpacote.
- `backend/app/modules/outbox/workers/outbox_worker.py`: worker de leitura/publicação do outbox.
- `backend/app/modules/permissoes/`: domínio de RBAC/permissões.
- `backend/app/modules/permissoes/__init__.py`: inicialização do módulo.
- `backend/app/modules/permissoes/models/`: modelos de papéis/permissões.
- `backend/app/modules/permissoes/models/__init__.py`: inicialização do subpacote.
- `backend/app/modules/permissoes/models/permission.py`: entidade de permissão.
- `backend/app/modules/permissoes/models/role.py`: entidade de papel.
- `backend/app/modules/permissoes/models/role_permission.py`: associação papel-permissão.
- `backend/app/modules/permissoes/models/user_role.py`: associação usuário-papel.
- `backend/app/modules/permissoes/repositories/`: acesso a dados de RBAC.
- `backend/app/modules/permissoes/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/permissoes/repositories/role_repository.py`: repositório de papéis.
- `backend/app/modules/permissoes/services/`: serviços de autorização.
- `backend/app/modules/permissoes/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/permissoes/services/permission_service.py`: regras de validação/concessão de permissões.
- `backend/app/modules/schedule/`: domínio de agenda em nomenclatura inglesa.
- `backend/app/modules/schedule/schemas/`: schemas do domínio schedule.
- `backend/app/modules/schedule/schemas/__init__.py`: inicialização do subpacote.
- `backend/app/modules/schedule/schemas/appointment.py`: schema de appointment.
- `backend/app/modules/schedule/services/`: serviços do domínio schedule.
- `backend/app/modules/schedule/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/schedule/services/appointment_service.py`: serviço de appointment.
- `backend/app/modules/testes/`: módulo de endpoints de teste.
- `backend/app/modules/testes/__init__.py`: inicialização do módulo.
- `backend/app/modules/testes/api/`: API do módulo de testes.
- `backend/app/modules/testes/api/__init__.py`: inicialização do subpacote.
- `backend/app/modules/testes/api/testes.py`: rotas de checagem/diagnóstico.
- `backend/app/modules/users/`: pasta reservada para módulo em inglês (estrutura em evolução).
- `backend/app/modules/usuarios/`: domínio de usuários (PT).
- `backend/app/modules/usuarios/__init__.py`: inicialização do módulo.
- `backend/app/modules/usuarios/api/`: API de usuários.
- `backend/app/modules/usuarios/api/__init__.py`: inicialização do subpacote.
- `backend/app/modules/usuarios/repositories/`: repositórios de usuários.
- `backend/app/modules/usuarios/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/usuarios/schemas/`: schemas de usuários.
- `backend/app/modules/usuarios/schemas/__init__.py`: inicialização do subpacote.
- `backend/app/modules/usuarios/services/`: serviços de usuários.
- `backend/app/modules/usuarios/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/webhooks/`: domínio de assinatura/disparo de webhooks.
- `backend/app/modules/webhooks/events/`: eventos de webhook.
- `backend/app/modules/webhooks/events/__init__.py`: inicialização do subpacote.
- `backend/app/modules/webhooks/events/webhook_event_handler.py`: handler para eventos que disparam webhooks.
- `backend/app/modules/webhooks/models/`: modelos de webhook.
- `backend/app/modules/webhooks/models/__init__.py`: inicialização do subpacote.
- `backend/app/modules/webhooks/models/webhook_subscription.py`: entidade de assinatura de webhook.
- `backend/app/modules/webhooks/repositories/`: acesso a dados de webhooks.
- `backend/app/modules/webhooks/repositories/__init__.py`: inicialização do subpacote.
- `backend/app/modules/webhooks/repositories/webhook_repository.py`: repositório de assinaturas/webhooks.
- `backend/app/modules/webhooks/services/`: serviços de webhook.
- `backend/app/modules/webhooks/services/__init__.py`: inicialização do subpacote.
- `backend/app/modules/webhooks/services/webhook_service.py`: lógica de entrega e gerenciamento de webhooks.

##### backend/app/repositories e backend/app/repositorios/

- `backend/app/repositories/`: namespace para repositórios (EN).
- `backend/app/repositories/__init__.py`: inicialização do namespace.
- `backend/app/repositorios/`: repositórios em nomenclatura PT.
- `backend/app/repositorios/__init__.py`: inicialização do pacote.
- `backend/app/repositorios/base.py`: classe/base utilitária de repositório.
- `backend/app/repositorios/base_repository.py`: implementação base de repositório para CRUD.

##### backend/app/schemas, services e utils

- `backend/app/schemas/`: schemas compartilhados de API/domínio.
- `backend/app/schemas/__init__.py`: inicialização do pacote de schemas.
- `backend/app/schemas/appointment.py`: contrato de appointment.
- `backend/app/schemas/compromisso.py`: contrato principal de compromisso.
- `backend/app/schemas/compromisso_legado.py`: contrato legado de compromisso.
- `backend/app/services/`: pasta reservada para serviços compartilhados.
- `backend/app/utils/`: pasta reservada para utilitários compartilhados.

### config/

- `config/`: configurações do ambiente backend.
- `config/.env`: variáveis de ambiente locais (segredos/configurações).
- `config/.gitignore`: regras de ignorados específicas da pasta de config.
- `config/alembic.ini`: configuração do Alembic (paths e conexão).
- `config/requirements.txt`: dependências Python do backend.

### docs/

- `docs/`: documentação oficial do projeto.
- `docs/estrutura-do-projeto.md`: este documento (estrutura técnica).
- `docs/fase-1.md`: escopo e entregáveis da Fase 1.
- `docs/fase-1-frontend.md`: recorte do frontend na Fase 1.
- `docs/funcionalidades-futuras.md`: roadmap de fases futuras.

### frontend/

- `frontend/`: app web em Next.js + React + TypeScript.
- `frontend/.gitignore`: ignorados específicos do frontend.
- `frontend/eslint.config.mjs`: regras de lint JS/TS.
- `frontend/next-env.d.ts`: tipos automáticos do Next.js para TS.
- `frontend/next.config.ts`: configuração do framework Next.js.
- `frontend/package.json`: scripts e dependências npm.
- `frontend/package-lock.json`: lock de versões npm.
- `frontend/postcss.config.mjs`: configuração PostCSS.
- `frontend/tailwind.config.ts`: configuração do Tailwind.
- `frontend/tsconfig.json`: configuração TypeScript.

#### frontend/public/

- `frontend/public/`: assets estáticos públicos.
- `frontend/public/file.svg`: ícone/asset SVG auxiliar.
- `frontend/public/globe.svg`: ícone de globo.
- `frontend/public/next.svg`: ícone da marca Next.
- `frontend/public/vercel.svg`: ícone da Vercel.
- `frontend/public/window.svg`: ícone/asset de janela.

#### frontend/src/app/

- `frontend/src/`: código-fonte do frontend.
- `frontend/src/app/`: rotas e layout do App Router.
- `frontend/src/app/(auth)/`: grupo de rotas de autenticação.
- `frontend/src/app/(auth)/entrar/`: rota de login.
- `frontend/src/app/(auth)/entrar/page.tsx`: página de entrada/autenticação.
- `frontend/src/app/(dashboard)/`: grupo de rotas autenticadas.
- `frontend/src/app/(dashboard)/compromissos/`: rota de compromissos no painel.
- `frontend/src/app/(dashboard)/compromissos/page.tsx`: página de compromissos.
- `frontend/src/app/(dashboard)/painel/`: rota principal do painel.
- `frontend/src/app/(dashboard)/painel/page.tsx`: página inicial do dashboard.
- `frontend/src/app/(dashboard)/perfil/`: rota de perfil.
- `frontend/src/app/(dashboard)/perfil/page.tsx`: página de perfil do usuário.
- `frontend/src/app/favicon.ico`: ícone da aplicação.
- `frontend/src/app/globals.css`: estilos globais.
- `frontend/src/app/layout.tsx`: layout raiz e composição de providers.
- `frontend/src/app/page.tsx`: página raiz pública.

#### frontend/src/features/

- `frontend/src/features/`: organização por funcionalidades.
- `frontend/src/features/autenticacao/`: feature de login/sessão.
- `frontend/src/features/autenticacao/services/`: integração HTTP da autenticação.
- `frontend/src/features/autenticacao/services/autenticacaoService.ts`: serviço de autenticação.
- `frontend/src/features/autenticacao/types/`: tipos do domínio de autenticação.
- `frontend/src/features/autenticacao/types/autenticacao.ts`: tipagens de autenticação.
- `frontend/src/features/autenticacao/ui/`: componentes visuais da feature.
- `frontend/src/features/autenticacao/ui/EntrarView.tsx`: tela/componente de login.
- `frontend/src/features/compromissos/`: feature de compromissos.
- `frontend/src/features/compromissos/hooks/`: hooks da feature.
- `frontend/src/features/compromissos/hooks/useCompromissos.ts`: hook de leitura/manutenção de compromissos.
- `frontend/src/features/compromissos/services/`: serviços HTTP da feature.
- `frontend/src/features/compromissos/services/compromissosService.ts`: chamadas de API de compromissos.
- `frontend/src/features/compromissos/types/`: tipos da feature.
- `frontend/src/features/compromissos/types/compromisso.ts`: tipagens de compromisso.
- `frontend/src/features/compromissos/ui/`: componentes de interface da feature.
- `frontend/src/features/compromissos/ui/CompromissosView.tsx`: view/lista de compromissos.
- `frontend/src/features/compromissos/ui/PainelView.tsx`: view-resumo do painel.
- `frontend/src/features/usuarios/`: feature de usuários/perfil.
- `frontend/src/features/usuarios/ui/`: camada visual da feature.
- `frontend/src/features/usuarios/ui/PerfilView.tsx`: view de perfil do usuário.

#### frontend/src/shared/, store e styles

- `frontend/src/shared/`: recursos compartilhados entre features.
- `frontend/src/shared/api/`: infraestrutura HTTP compartilhada.
- `frontend/src/shared/api/endpoints.ts`: catálogo central de endpoints.
- `frontend/src/shared/api/httpClient.ts`: cliente HTTP base.
- `frontend/src/shared/components/`: componentes reutilizáveis.
- `frontend/src/shared/components/PaginaBase.tsx`: layout base de páginas.
- `frontend/src/shared/lib/`: utilitários puros reutilizáveis.
- `frontend/src/shared/lib/formatarDataHora.ts`: formatação de data/hora.
- `frontend/src/shared/types/`: tipos compartilhados.
- `frontend/src/shared/types/compromisso.ts`: tipo compartilhado de compromisso.
- `frontend/src/store/`: documentação/estrutura de estado global.
- `frontend/src/store/README.md`: guia do padrão de store.
- `frontend/src/styles/`: documentação/estrutura de estilos.
- `frontend/src/styles/README.md`: guia de organização de estilos.

### tests/

- `tests/`: suíte automatizada do backend.
- `tests/conftest.py`: fixtures e configuração de testes.
- `tests/test_appointment_cancel_service.py`: testes de cancelamento de appointment.
- `tests/test_appointment_model.py`: testes do modelo appointment.
- `tests/test_appointment_time_conflict_service.py`: testes de conflito de horários.
- `tests/test_base_repository.py`: testes da base de repositórios.
- `tests/test_company_model.py`: testes do modelo de empresa.
- `tests/test_env.py`: testes de ambiente/configuração.
- `tests/test_event_bus.py`: testes de barramento de eventos.
- `tests/test_idempotency_appointments.py`: testes de idempotência em appointments.
- `tests/test_outbox_events.py`: testes de outbox/events.
- `tests/test_permissions.py`: testes de permissões/RBAC.
- `tests/test_rate_limit.py`: testes de limitação de taxa.
- `tests/test_tenant_scope_enforcement.py`: testes de isolamento por tenant.
- `tests/test_webhooks.py`: testes de fluxo de webhooks.

## 4) Convenções rápidas

- Pastas com `api/`: superfície HTTP (rotas/controladores).
- Pastas com `services/`: regras de negócio/casos de uso.
- Pastas com `repositories/` ou `repositorios/`: acesso a dados.
- Pastas com `models/`: entidades ORM/persistência.
- Pastas com `schemas/` e `types/`: contratos de entrada/saída.
- Arquivos `__init__.py`: inicialização de pacote Python.
