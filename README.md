# AIgenda

O AIgenda é um sistema de organização inteligente de compromissos, pensado para equipes e empresas que precisam de agendamento confiável, seguro e escalável.

O projeto já nasce com fundamentos de arquitetura profissional: separação por camadas, isolamento multi-tenant, controle de autoria, prevenção automática de conflitos de agenda e testes estruturais.

## Objetivo do sistema

- Organizar compromissos de forma centralizada
- Permitir múltiplos participantes por compromisso
- Evitar conflitos de horário automaticamente
- Manter rastreabilidade de autoria e histórico
- Preparar base técnica para evolução em fases (engajamento, personalização e inteligência adaptativa)

## Stack do projeto

- Backend: FastAPI + SQLAlchemy + Alembic
- Banco de dados: PostgreSQL (via Docker Compose)
- Frontend: Next.js + React + TypeScript + Tailwind CSS
- Testes: Pytest

## Estrutura principal

```text
aigenda/
├── backend/
├── frontend/
├── docs/
├── config/
├── tests/
├── docker-compose.yml
└── Makefile
```

## Como executar

1. Criar e ativar ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências do backend:

```bash
pip install -r config/requirements.txt
```

3. Subir infraestrutura (PostgreSQL):

```bash
docker compose up -d
```

4. Rodar migrações:

```bash
alembic -c config/alembic.ini upgrade head
```

5. Executar API (entrypoint atual):

```bash
PYTHONPATH=backend uvicorn app.principal:app --reload
```

6. Executar frontend:

```bash
cd frontend
npm install
npm run dev
```

## Documentação funcional por fase

- Fase 1 (Organização Inteligente): `docs/fase-1.md`
- Frontend da Fase 1: `docs/fase-1-frontend.md`
- Roadmap de funcionalidades futuras: `docs/funcionalidades-futuras.md`
- Guia detalhado da estrutura de pastas e arquivos: `docs/estrutura-do-projeto.md`

## Qualidade e validação

- Testes automatizados no diretório `tests/`
- Migrações versionadas em `backend/alembic/versions/`
- Organização por domínio no backend (`api`, `models`, `repositorios`, `modules`)

## Visão de evolução

O AIgenda segue uma estratégia em fases: primeiro garantir uma base robusta de organização (Fase 1), depois evoluir para engajamento e gamificação (Fase 2), personalização progressiva (Fase 3) e inteligência adaptativa (Fase 4).
