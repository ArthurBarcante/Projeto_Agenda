# Estrutura do Projeto — Guia Detalhado

Este documento descreve, de forma objetiva, o papel de cada pasta e dos principais arquivos do AIgenda.

## Raiz do projeto (`aigenda/`)

- `README.md`: visão geral do sistema, execução local e links para documentação.
- `docker-compose.yml`: sobe infraestrutura de apoio (ex.: PostgreSQL).
- `Makefile`: atalhos de comandos de desenvolvimento e automação.
- `.gitignore`: arquivos/pastas ignorados no versionamento.

## Backend (`backend/`)

### `backend/app/`

Contém o código principal da API FastAPI.

- `main.py`: inicialização da aplicação e registro de rotas.

#### `backend/app/core/`

Configurações transversais da aplicação.

- `config.py`: leitura de variáveis de ambiente e configurações globais.
- `database.py`: engine/sessão do banco e utilitários de acesso.
- `dependencies.py`: dependências reutilizáveis (injeção em rotas/serviços).
- `exceptions.py`: exceções de domínio e tratamento padronizado.
- `security.py`: utilitários de autenticação e segurança.

#### `backend/app/modules/`

Módulos de domínio, organizados por contexto de negócio.

##### `auth/`

- `routes.py`: endpoints de autenticação.
- `schemas.py`: contratos de entrada/saída da autenticação.

##### `users/`

- `models.py`: entidades de usuário no banco.
- `schemas.py`: validação e serialização de dados de usuário.
- `services.py`: regras de negócio de usuários.
- `routes.py`: endpoints de usuários.

##### `schedule/`

- `models.py`: entidades de compromissos e relações.
- `schemas.py`: contratos de criação/retorno de compromissos.
- `repository.py`: acesso estruturado a dados de agenda.
- `services.py`: regras de conflito, estado e autoria.
- `routes.py`: endpoints de agenda.

##### `companies/`

- `models.py`: entidades relacionadas a empresas/tenant.

#### `backend/app/services/`

Espaço para serviços compartilhados entre módulos.

#### `backend/app/utils/`

Utilitários genéricos para apoio às camadas da aplicação.

### `backend/alembic/`

Controle de migrações de banco de dados.

- `env.py`: configuração de execução das migrações.
- `script.py.mako`: template padrão para novos scripts de migração.
- `versions/`: histórico versionado de alterações de schema.

## Configuração (`config/`)

- `alembic.ini`: configuração do Alembic.
- `requirements.txt`: dependências de produção.
- `requirements-dev.txt`: dependências de desenvolvimento.
- `.env`: variáveis de ambiente locais (não deve ser exposto publicamente).

## Frontend (`frontend/`)

Aplicação cliente em React + TypeScript + Vite.

- `package.json`: scripts e dependências do frontend.
- `vite.config.ts`: configuração de build/dev server.
- `index.html`: página base.

### `frontend/src/`

- `main.tsx`: bootstrap do React.
- `App.tsx`: composição principal.
- `Login.tsx`: tela de login.
- `Dashboard.tsx`: painel inicial autenticado.

## Documentação (`docs/`)

- `FASE1_ARQUITETURA_OFICIAL.md`: diretriz arquitetural original da fase 1.
- `fase-1.md`: escopo funcional da Organização Inteligente.
- `fase-1-frontend.md`: recorte do frontend na fase 1.
- `funcionalidades-futuras.md`: roadmap das fases 2, 3 e 4.
- `estrutura-do-projeto.md`: este guia de estrutura.

## Testes (`tests/`)

- `test_schedule.py`: cenários de regras da agenda.
- `test_users.py`: cenários de regras de usuários.
- `test_real_conflict.py`: validação de conflito real de agenda.
- `test_real_concurrency_exclude.py`: cenário de concorrência e exclusão.

## Convenções adotadas

- `routes.py`: camada HTTP (entrada/saída da API).
- `services.py`: regras de negócio.
- `repository.py`: acesso persistente aos dados.
- `models.py`: entidades do banco.
- `schemas.py`: contratos de validação e serialização.
