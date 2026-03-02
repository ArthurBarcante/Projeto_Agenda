# O que foi feito até agora

Esta página registra o estado atual de implementação do projeto.

## Banco de dados e migrations

- Estrutura de migrations com Alembic configurada.
- Migration `06b0bc232d22` criada para tabela `companies`.
- Migration `3afa394c9de8` criada para tabela `users` com relação para `companies`.
- Constraint de unicidade por tenant em usuário: `uq_user_company_email` (`company_id + email`).

## Modelagem de domínio

- Modelo `Company` com:
	- `name`, `slug`, `plan`, `is_active`.
	- Enum de plano (`FREE`, `PRO`, `ENTERPRISE`).
	- Relação ORM com usuários.
- Modelo `User` com:
	- `id` (UUIDv7), `company_id`, `name`, `email`, `password_hash`, `is_active`.
	- Relação com `Company`.
	- Marcação de escopo de tenant (`__tenant_scoped__ = True`).

## Multi-tenant

- Contexto de tenant implementado em `app/core/tenant.py`.
- Enforcement automático de escopo em consultas `SELECT` no `SessionLocal`:
	- Se a entidade é tenant-scoped, aplica filtro por `company_id`.
	- Se não houver contexto de tenant, lança erro para evitar vazamento de dados.
- `BaseRepository` já inicia queries com filtro da empresa atual.

## Autenticação

- Endpoint de login em `POST /auth/login`.
- Fluxo implementado:
	- Busca empresa por `company_slug`.
	- Busca usuário por `email` + `company_id`.
	- Valida senha.
	- Emite JWT com `sub`, `company_id` e `company_slug`.

## Identificadores UUIDv7

- Utilitário central em `app/core/config/uuid7.py`.
- Estratégia híbrida:
	- Usa `uuid.uuid7()` quando disponível.
	- Fallback para pacote `uuid6` quando necessário.

## Testes existentes

- `tests/test_company_model.py`
	- Valida enum de planos e colunas/constraints do modelo `Company`.
- `tests/test_base_repository.py`
	- Garante filtro por tenant no repositório base.
	- Garante erro para modelos sem `company_id`.
- `tests/test_tenant_scope_enforcement.py`
	- Garante erro sem contexto de tenant em entidades tenant-scoped.
	- Garante injeção automática de filtro por `company_id`.
	- Garante que entidades não tenant-scoped não exigem contexto.

## Próximos passos sugeridos

- Criar endpoints CRUD de empresas e usuários (com autorização).
- Adicionar testes de integração para fluxo de login/JWT.
- Iniciar módulo principal de agenda (eventos, contatos e compromissos).
- Definir papéis/perfis de acesso por tenant.
