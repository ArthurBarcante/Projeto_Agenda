# Projeto Agenda

Projeto de agenda com frontend em HTML, CSS e JavaScript puro e backend em FastAPI.

Hoje o backend ja possui autenticacao real com persistencia de usuarios em PostgreSQL, usando SQLAlchemy para ORM, bcrypt para hash de senha e JWT para autenticacao stateless.

## Estado Atual

- Cadastro de usuario com persistencia real no PostgreSQL
- Validacao de email e CPF duplicados
- Validacao de confirmacao de senha via schema Pydantic
- Senha salva com hash bcrypt
- Login real com email e senha
- Retorno de token JWT no login
- Rota protegida para identificar o usuario autenticado
- Frontend ainda pode alternar entre mock local e API real

## Tecnologias

- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI
- ORM: SQLAlchemy
- Banco de dados: PostgreSQL
- Driver PostgreSQL: psycopg2-binary
- Validacao: Pydantic
- Hash de senha: bcrypt
- Autenticacao: JWT com python-jose
- Mock local: JSON Server

## Estrutura Resumida

```text
Projeto_Agenda/
├── README.md
├── back/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routers/
│   │   └── schemas/
│   └── mock/
├── configs/
│   └── requirements.txt
├── docs/
│   ├── beginner/
│   └── developer/
├── front/
└── tests/
```

## Fluxo Implementado Hoje

### Cadastro

1. A API recebe os dados pelo schema de entrada.
2. Valida email, CPF e confirmacao de senha.
3. Gera hash bcrypt da senha.
4. Salva o usuario na tabela `users` do PostgreSQL.

### Login

1. Busca o usuario pelo email.
2. Compara a senha com o hash salvo no banco.
3. Gera um token JWT com o `sub` do usuario.
4. Retorna `access_token` e `token_type`.

### Autenticacao

1. O cliente envia `Authorization: Bearer TOKEN`.
2. O backend decodifica o JWT.
3. Busca o usuario no banco.
4. Libera acesso a rotas protegidas.

## Como Rodar o Projeto

### 1. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependencias do backend

```bash
pip install -r configs/requirements.txt
```

Dependencias atuais em `configs/requirements.txt`:

- fastapi
- uvicorn[standard]
- pydantic[email]
- sqlalchemy
- psycopg2-binary
- bcrypt
- python-jose

### 3. Configurar o PostgreSQL

O backend usa a conexao definida em `back/app/database/connection.py`.

Exemplo atual:

```python
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/aigenda"
```

Ajuste conforme o seu ambiente:

- usuario
- senha
- host
- porta
- nome do banco

Ao iniciar a API, a tabela `users` e criada automaticamente se ainda nao existir.

### 4. Rodar o backend FastAPI

```bash
uvicorn app.main:app --reload --app-dir back
```

URLs:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

### 5. Rodar o mock local opcional

```bash
npx json-server --watch back/mock/db.json
```

URL do mock:

- http://localhost:3000

### 6. Abrir o frontend

Abra `front/index.html` com Live Server ou outro servidor estatico local.

## Alternancia do Frontend Entre Mock e API Real

O frontend usa a chave definida em `front/js/core/api.js`:

```js
const USE_REAL_API = false;
```

Valores:

- `false`: usa JSON Server
- `true`: usa FastAPI

Observacao: o backend ja esta com persistencia real de usuario, mas o frontend ainda pode ser alternado manualmente entre mock e API real.

## Endpoints Atuais da API

### GET /

Resposta:

```json
{
	"message": "Backend funcionando!"
}
```

### POST /auth/register

Payload:

```json
{
	"name": "Arthur",
	"email": "arthur@email.com",
	"password": "123456",
	"confirm_password": "123456",
	"phone": "86999999999",
	"cpf": "12345678900",
	"birthdate": "2000-05-10",
	"role": "user"
}
```

Resposta de sucesso:

```json
{
	"message": "Usuario criado com sucesso",
	"user": {
		"id": 1,
		"name": "Arthur",
		"email": "arthur@email.com"
	}
}
```

### POST /auth/login

Payload:

```json
{
	"email": "arthur@email.com",
	"password": "123456"
}
```

Resposta de sucesso:

```json
{
	"access_token": "jwt-token-aqui",
	"token_type": "bearer"
}
```

### GET /auth/me

Header:

```http
Authorization: Bearer SEU_TOKEN
```

Resposta de sucesso:

```json
{
	"id": 1,
	"email": "arthur@email.com"
}
```

## Arquivos Principais do Backend

- `back/app/main.py`: inicializacao da API, CORS, inclusao de routers e criacao automatica das tabelas
- `back/app/database/connection.py`: engine e sessao do SQLAlchemy
- `back/app/database/deps.py`: dependencia `get_db`
- `back/app/models/user.py`: modelo ORM da tabela `users`
- `back/app/schemas/auth/user.py`: schema de cadastro
- `back/app/schemas/auth/login.py`: schema de login
- `back/app/core/security.py`: hash de senha e JWT
- `back/app/core/auth.py`: identificacao do usuario autenticado via token
- `back/app/routers/auth/register.py`: endpoint de cadastro
- `back/app/routers/auth/login.py`: endpoints de login e `/me`

## Navegacao da Documentacao

### Beginner

- [O que e o projeto](docs/beginner/what-is-the-project.md)
- [O que o projeto faz](docs/beginner/what-functions-it-has.md)
- [Estado atual](docs/beginner/current-state.md)
- [Futuras evolucoes](docs/beginner/future-evolutions.md)

### Developer

- [Estrutura do projeto](docs/developer/project-structure.md)
- [Requisitos futuros](docs/developer/future-requirements.md)

### Developer Back-end

- [App](docs/developer/back-end/app.md)
- [Models](docs/developer/back-end/models.md)
- [Routers](docs/developer/back-end/routers.md)
- [Schemas](docs/developer/back-end/schemas.md)
- [Security](docs/developer/back-end/security.md)

### Developer Front-end

- [CSS](docs/developer/front-end/css.md)
- [JavaScript](docs/developer/front-end/js.md)
- [Login](docs/developer/front-end/login.md)
- [Register](docs/developer/front-end/register.md)
- [UI](docs/developer/front-end/ui.md)

## Observacoes

- `confirm_password` existe apenas no schema de entrada e nao deve ser persistido.
- O token JWT usa uma chave padrao local, mas o ideal e configurar `JWT_SECRET_KEY` no ambiente.
- A configuracao de banco ainda esta fixa no codigo e pode evoluir para `.env` depois.

## Proximos Passos Sugeridos

- integrar o frontend ao fluxo JWT completo
- proteger futuras rotas de tarefas e eventos com `get_current_user`
- adicionar testes automatizados para cadastro, login e rota protegida