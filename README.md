# Projeto Agenda (AIGenda)

## Escopo do projeto

O **AIGenda** é uma API backend em FastAPI para agenda multiempresa (multi-tenant), com foco em:

- Isolamento de dados por empresa (`tenant`) em nível de consulta.
- Gestão de empresas e usuários com PostgreSQL + SQLAlchemy.
- Autenticação com login por empresa e geração de JWT.
- Base técnica para evoluir módulos de agenda, contatos e compromissos.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pytest

## Estrutura principal

- `app/main.py`: inicialização da aplicação e roteadores.
- `app/api/auth/auth.py`: endpoint de login.
- `app/db/session.py`: sessão do banco e enforcement automático de tenant.
- `app/models/`: modelos ORM (`Company`, `User`, base e mixins).
- `app/repositories/base.py`: repositório base com filtro por empresa.
- `alembic/versions/`: migrations de esquema.

## Documentação adicional

- [O que foi feito até agora](docs/o-que-foi-feito-ate-agora.md)

## Execução local (resumo)

1. Criar/ativar ambiente virtual.
2. Instalar dependências com `requirements.txt`.
3. Configurar variáveis de ambiente (ex.: `DATABASE_URL`).
4. Executar migrations com Alembic.
5. Iniciar API FastAPI.

