# AIGENDA

Sistema inteligente de organização e evolução pessoal com foco em agenda estruturada, prevenção de conflitos, isolamento multi-tenant e evolução por fases.

## Estrutura principal do projeto

```text
aigenda/
├── backend/        # Código backend (FastAPI, domínio, serviços, ORM, migrações)
├── frontend/       # Código frontend (Next.js)
├── config/         # Configurações e dependências do projeto
├── tests/          # Testes automatizados
├── documentation/  # Documentação de apoio
└── virtualenv/     # Ambientes virtuais Python
```

## Navegação do projeto no GitHub

- [Visão geral do projeto (página inicial)](README.md)
- [Backend: estrutura e arquivos](documentation/docs/backend.md)
- [Frontend: estrutura e arquivos](documentation/docs/frontend.md)
- [Configurações e tecnologias](documentation/docs/config.md)
- [Virtualenv (ambiente Python)](documentation/docs/virtualenv.md)
- [Documentação de fases e roadmap](documentation/docs/documentation.md)
- [Testes automatizados](documentation/docs/tests.md)

## Visão geral do sistema

- **Fase atual:** Fase 1 (Organização Inteligente) implementada.
- **Objetivo atual:** organizar compromissos com integridade e sem sobreposição.
- **Base técnica:** FastAPI + SQLAlchemy + Alembic + PostgreSQL + Next.js.
- **Diretriz do produto:** autonomia permanente do usuário; evolução amplia a experiência sem bloquear funcionalidades base.
