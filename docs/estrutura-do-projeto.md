# Estrutura do Projeto — Guia Completo

Este documento descreve o corpo atual de pastas e arquivos do AIgenda, com foco no papel de cada parte da aplicação.

## Estado estrutural consolidado

- `frontend/` é a pasta oficial do frontend.
- A pasta redundante `frontend/aigenda-frontend/` foi removida.
- A pasta redundante `documentation/` foi removida.
- Toda documentação oficial permanece em `docs/`.

## Raiz do projeto (`aigenda/`)

- `.gitignore`: regras de arquivos ignorados.
- `README.md`: visão geral, execução e links de documentação.
- `backend/`: API, domínio, modelos e migrações.
- `config/`: configurações e dependências Python.
- `docs/`: documentação funcional e técnica.
- `frontend/`: aplicação Next.js.
- `tests/`: testes automatizados do backend.

## Backend (`backend/`)

### Arquivos e pastas principais

- `backend/aigenda.db`: base SQLite local (ambiente de desenvolvimento).
- `backend/alembic/`: mecanismo de migração de schema.
- `backend/app/`: código principal da aplicação FastAPI.

### Migrações (`backend/alembic/`)

- `env.py`: configura contexto de execução do Alembic.
- `script.py.mako`: template para novas migrações.
- `versions/`: histórico de evolução do banco:
	- `06b0bc232d22_criar_tabela_empresas.py`
	- `3afa394c9de8_criar_tabela_usuarios.py`
	- `8f2c7a1b90d4_adicionar_indices_conflito_compromissos.py`
	- `b7e4c2a9d1f0_traduz_nomenclatura_banco_para_portugues.py`

### Aplicação (`backend/app/`)

- `__init__.py`: metadados do pacote backend.
- `principal.py`: ponto de entrada FastAPI e inclusão de rotas.

#### Camada de API (`backend/app/api/`)

- `dependencias.py`: dependências compartilhadas das rotas.
- `autenticacao/autenticacao.py`: endpoints de autenticação.
- `compromissos/compromissos.py`: endpoints de compromissos.
- `agenda/compromissos.py`: endpoints de agenda.
- `testes/testes.py`: endpoints auxiliares de teste/diagnóstico.

#### Núcleo (`backend/app/core/`)

- `inquilino.py`: controle de contexto multi-tenant.
- `autenticacao/seguranca.py`: utilitários de segurança/autorização.
- `autenticacao/token_jwt.py`: criação/validação de JWT.
- `config/configuracoes.py`: configurações globais da aplicação.
- `config/uuid7.py`: geração/manipulação de UUID7.

#### Banco e persistência

- `db/sessao.py`: sessão/engine de acesso ao banco.
- `repositorios/base.py`: padrão base de repositório.

#### Modelos (`backend/app/models/`)

- `base.py`: base ORM comum.
- `mixins.py`: comportamentos reutilizáveis para entidades.
- `empresa.py`: entidade Empresa (tenant).
- `usuario.py`: entidade Usuário.
- `compromisso.py`: entidade Compromisso.
- `participante_compromisso.py`: associação de participantes em compromissos.

#### Schemas (`backend/app/schemas/`)

- `compromisso.py`: contratos atuais de entrada/saída de compromisso.
- `compromisso_legado.py`: compatibilidade com formato legado.

#### Módulos de domínio (`backend/app/modules/`)

- `agenda/services/servico_compromisso.py`: regras de serviço da agenda.
- `compromissos/services/compromisso_service.py`: regras de negócio de compromissos.
- `auth/`, `companies/`, `schedule/`, `users/`: estrutura preparada para expansão por domínio.

#### Pastas de apoio

- `services/`: serviços compartilhados de aplicação.
- `utils/`: utilitários gerais.

## Frontend (`frontend/`)

Frontend oficial em Next.js (App Router) com React, TypeScript e Tailwind.

### Configuração da aplicação

- `.gitignore`: regras de ignorados do frontend.
- `package.json`: scripts e dependências.
- `package-lock.json`: lockfile das dependências.
- `next.config.ts`: configuração do Next.js.
- `tsconfig.json`: configuração TypeScript.
- `eslint.config.mjs`: configuração de lint.
- `postcss.config.mjs`: pipeline PostCSS.
- `tailwind.config.ts`: tokens e escopo Tailwind.

### Assets estáticos (`frontend/public/`)

- `file.svg`, `globe.svg`, `next.svg`, `vercel.svg`, `window.svg`.

### App Router (`frontend/src/app/`)

- `layout.tsx`: layout base da aplicação.
- `globals.css`: estilos globais.
- `page.tsx`: rota raiz.
- `favicon.ico`: ícone do app.
- `(auth)/entrar/page.tsx`: página de login.
- `(dashboard)/painel/page.tsx`: painel do usuário.
- `(dashboard)/compromissos/page.tsx`: página de compromissos.
- `(dashboard)/perfil/page.tsx`: página de perfil.

### Features (`frontend/src/features/`)

- `autenticacao/`
	- `services/autenticacaoService.ts`
	- `types/autenticacao.ts`
	- `ui/EntrarView.tsx`
- `compromissos/`
	- `hooks/useCompromissos.ts`
	- `services/compromissosService.ts`
	- `types/compromisso.ts`
	- `ui/CompromissosView.tsx`
	- `ui/PainelView.tsx`
- `usuarios/`
	- `ui/PerfilView.tsx`

### Compartilhado (`frontend/src/shared/`)

- `api/endpoints.ts`: catálogo de endpoints de integração.
- `api/httpClient.ts`: cliente HTTP centralizado.
- `components/PaginaBase.tsx`: componente base de página.
- `lib/formatarDataHora.ts`: utilitário de formatação de data/hora.
- `types/compromisso.ts`: tipos compartilhados de compromisso.

### Suporte interno (`frontend/src/`)

- `store/README.md`: documentação do padrão de estado global.
- `styles/README.md`: documentação de organização de estilos.

## Configuração (`config/`)

- `.env`: variáveis de ambiente locais.
- `.gitignore`: ignorados específicos da pasta.
- `alembic.ini`: configuração do Alembic.
- `requirements.txt`: dependências Python do backend.

## Documentação oficial (`docs/`)

- `fase-1.md`: escopo funcional da Fase 1 (Organização Inteligente).
- `fase-1-frontend.md`: recorte funcional do frontend na Fase 1.
- `funcionalidades-futuras.md`: roadmap das fases 2, 3 e 4.
- `estrutura-do-projeto.md`: este guia completo da estrutura.

## Testes (`tests/`)

- `test_appointment_cancel_service.py`: valida cancelamento de compromissos.
- `test_appointment_model.py`: valida regras do modelo de compromisso.
- `test_appointment_time_conflict_service.py`: valida conflitos de horário.
- `test_base_repository.py`: valida camada base de repositórios.
- `test_company_model.py`: valida entidade/consistência de empresa.
- `test_env.py`: valida ambiente/configurações.
- `test_tenant_scope_enforcement.py`: valida isolamento por tenant.

## Convenções adotadas

- `api/`: camada HTTP e contratos de acesso externo.
- `services/`: regras de negócio.
- `repositorios/`: acesso a dados/persistência.
- `models/`: entidades e mapeamento ORM.
- `schemas/`: validação e serialização de dados.
