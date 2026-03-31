# Projeto Agenda

Projeto de agenda com frontend em HTML, CSS e JavaScript puro, backend em FastAPI e suporte a dois modos de dados:

- mock com JSON Server
- API real com FastAPI

No estado atual, o projeto ja possui fluxo basico de autenticacao com:

- login
- cadastro
- validacao de email e CPF no backend
- alternancia simples entre mock e API real no frontend

## Tecnologias

- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI
- Mock API: JSON Server
- Validacao de dados: Pydantic

## Estrutura Basica

```text
Projeto_Agenda/
├── back/
│   └── app/
│       ├── main.py
│       ├── models/
│       ├── routers/
│       └── schemas/
├── back/mock/
│   └── db.json
├── configs/
│   └── requirements.txt
├── docs/
├── front/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── ui/
└── tests/
```

## Funcionalidades Atuais

- Tela de login
- Tela de cadastro
- Navegacao entre login e cadastro
- Login via mock ou FastAPI
- Cadastro via mock ou FastAPI
- Validacao de confirmacao de senha
- Validacao de email duplicado
- Validacao de CPF duplicado

## Como Rodar o Projeto

### 1. Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd Projeto_Agenda
```

### 2. Criar e ativar ambiente virtual

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias do backend

```bash
pip install fastapi uvicorn "pydantic[email]"
```

### 4. Rodar o backend FastAPI

```bash
uvicorn app.main:app --reload --app-dir back
```

Backend disponivel em:

- http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

### 5. Rodar o mock com JSON Server

```bash
npx json-server --watch back/mock/db.json
```

Mock disponivel em:

- http://localhost:3000

### 6. Abrir o frontend

Abra o arquivo [front/index.html](/home/arthur/Documentos/projetos/Projeto_Agenda/front/index.html) com Live Server no VS Code ou outro servidor local estatico.

Exemplo com Live Server:

- abrir [front/index.html](/home/arthur/Documentos/projetos/Projeto_Agenda/front/index.html)
- executar Open with Live Server

## Alternancia Entre Mock e API Real

O frontend usa uma chave simples no arquivo [front/js/core/api.js](/home/arthur/Documentos/projetos/Projeto_Agenda/front/js/core/api.js).

```js
const USE_REAL_API = false;
```

Valores:

- `false`: usa JSON Server
- `true`: usa FastAPI

Para trocar entre os dois modos, basta alterar essa linha.

## Endpoints Atuais da API Real

### GET /

Resposta:

```json
{
	"message": "Backend funcionando!"
}
```

### POST /auth/login

Payload:

```json
{
	"email": "admin@email.com",
	"password": "123456"
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
	"birth_date": "2000-05-10",
	"cpf": "12345678900",
	"phone": "86999999999"
}
```

## Observacoes

- O arquivo [configs/requirements.txt](/home/arthur/Documentos/projetos/Projeto_Agenda/configs/requirements.txt) ainda nao esta preenchido.
- O projeto ainda esta em fase inicial e pode receber novas rotas, persistencia real e dashboard.
- O campo `confirm_password` e usado apenas para validacao e nao deve ser persistido.

## Proximos Passos Sugeridos

- preencher o `requirements.txt`
- criar persistencia real para usuarios
- adicionar dashboard apos login
- criar testes automatizados de backend e frontend
- documentar melhor os fluxos em `docs/`
