# Página do Backend

Esta página descreve a estrutura do backend e a função principal de cada arquivo relevante.

## Estrutura do backend

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── deps.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── deps.py
│   │   ├── schedule/
│   │   │   ├── __init__.py
│   │   │   └── appointments.py
│   │   └── test/
│   │       └── tests.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── tenant.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py
│   │   │   └── security.py
│   │   └── config/
│   │       ├── __init__.py
│   │       ├── config.py
│   │       └── uuid7.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   ├── appointment.py
│   │   ├── appointment_participant.py
│   │   ├── base.py
│   │   ├── company.py
│   │   ├── mixins.py
│   │   └── user.py
│   ├── modules/schedule/services/
│   │   └── appointment_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base.py
│   └── schemas/
│       ├── __init__.py
│       └── appointment.py
└── alembic/
	├── env.py
	├── script.py.mako
	└── versions/
```

## Explicação breve por arquivo

### Entrada da aplicação

- `app/main.py`: inicializa FastAPI e registra as rotas.
- `app/__init__.py`: metadados do pacote backend.

### API (camada HTTP)

- `app/api/deps.py`: dependências globais da API (ex.: usuário autenticado).
- `app/api/auth/auth.py`: endpoint de login e geração de token.
- `app/api/auth/deps.py`: dependências específicas da autenticação.
- `app/api/schedule/appointments.py`: endpoints de criação/edição/cancelamento de compromissos.
- `app/api/test/tests.py`: endpoints utilitários de verificação.

### Core (regras transversais)

- `app/core/config/config.py`: leitura de variáveis de ambiente e settings.
- `app/core/config/uuid7.py`: geração de UUID v7.
- `app/core/auth/security.py`: hash e verificação de senha.
- `app/core/auth/jwt.py`: criação e decodificação de JWT.
- `app/core/tenant.py`: controle de contexto de tenant (empresa ativa).

### Persistência

- `app/db/session.py`: engine, sessão do SQLAlchemy e enforcement de tenant em queries.

### Domínio (modelos)

- `app/models/base.py`: classes base ORM e campos comuns.
- `app/models/mixins.py`: mixins compartilhados (ex.: escopo de tenant).
- `app/models/company.py`: entidade de empresa e plano.
- `app/models/user.py`: entidade de usuário.
- `app/models/appointment.py`: entidade de compromisso e máquina de estado.
- `app/models/appointment_participant.py`: relação compromisso-participante.

### Aplicação (regras de negócio)

- `app/modules/schedule/services/appointment_service.py`: orquestra regras de agendamento (conflito, permissão, atualização e cancelamento).

### Repositórios e schemas

- `app/repositories/base.py`: base de acesso a dados com recorte por tenant.
- `app/schemas/appointment.py`: contratos de entrada/saída dos endpoints de compromisso.

### Migrações

- `alembic/env.py`: configuração do Alembic.
- `alembic/script.py.mako`: template de migração.
- `alembic/versions/*.py`: histórico versionado de migrações do banco.
