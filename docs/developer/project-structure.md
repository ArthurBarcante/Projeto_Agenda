# Estrutura do Projeto (Developer)

Data da revisao: 1 de abril de 2026

## Objetivo deste documento

Este arquivo explica como o projeto esta organizado hoje, depois da implantacao de persistencia real de usuarios com PostgreSQL, autenticacao com JWT e rotas protegidas.

O foco aqui e ajudar quem esta estudando desenvolvimento a entender nao apenas "onde cada arquivo esta", mas tambem "por que ele existe".

---

## Visao geral da arquitetura

Hoje o projeto esta dividido em quatro blocos principais:

- `front/`: interface web em HTML, CSS e JavaScript
- `back/`: API em FastAPI com banco PostgreSQL
- `docs/`: documentacao para iniciantes e estudantes de desenvolvimento
- `tests/`: arquivos de apoio para testes e simulacoes

Ha tambem duas pastas de apoio:

- `configs/`: dependencias do projeto
- `.venv/`: ambiente virtual Python local

---

## Arvore resumida e atualizada

```text
Projeto_Agenda/
├── README.md
├── back/
│   ├── app/
│   │   ├── core/
│   │   │   ├── auth.py
│   │   │   └── security.py
│   │   ├── database/
│   │   │   ├── base.py
│   │   │   ├── connection.py
│   │   │   └── deps.py
│   │   ├── models/
│   │   │   ├── fake_db.py
│   │   │   └── user.py
│   │   ├── routers/
│   │   │   └── auth/
│   │   │       ├── login.py
│   │   │       └── register.py
│   │   ├── schemas/
│   │   │   └── auth/
│   │   │       ├── login.py
│   │   │       ├── register.py
│   │   │       └── user.py
│   │   └── main.py
│   └── mock/
│       └── db.json
├── configs/
│   └── requirements.txt
├── docs/
│   ├── beginner/
│   └── developer/
│       ├── back-end/
│       │   ├── app.md
│       │   └── security.md
│       ├── front-end/
│       │   ├── login.md
│       │   └── register.md
│       ├── future-requirements.md
│       └── project-structure.md
├── front/
│   ├── css/
│   ├── js/
│   ├── ui/
│   └── index.html
└── tests/
```

---

## Como o backend esta organizado

## 1. `back/app/main.py`

### O que e

O ponto de entrada da API.

### O que ele faz

- cria a aplicacao FastAPI
- registra CORS
- importa os routers de autenticacao
- garante a criacao das tabelas mapeadas pelo SQLAlchemy

### Por que ele e importante

Sem esse arquivo a API nao sobe. Ele conecta as partes principais do backend.

---

## 2. `back/app/database/`

Essa pasta concentra a base do acesso ao banco.

### `base.py`

Define o `Base` do SQLAlchemy, que serve como ponto comum para os modelos do banco.

### `connection.py`

Cria o `engine` e a `SessionLocal`, ou seja:

- a conexao com o PostgreSQL
- a fabrica de sessoes usadas nas operacoes com o banco

### `deps.py`

Explica ao FastAPI como abrir e fechar uma sessao de banco por requisicao.

Esse arquivo existe para que as rotas usem `Depends(get_db)` de forma limpa e segura.

---

## 3. `back/app/models/`

Essa pasta representa a estrutura persistida no banco.

### `user.py`

Define o modelo `User`, que hoje e a principal entidade persistida do sistema.

Campos principais:

- `id`
- `name`
- `email`
- `password`
- `phone`
- `cpf`
- `birthdate`
- `role`

### `fake_db.py`

E um arquivo legado de apoio ao estudo. O fluxo real de usuario ja nao depende dele para cadastro e login.

---

## 4. `back/app/schemas/`

Aqui ficam os contratos de entrada da API.

### Por que isso importa

O modelo do banco e o schema da API nao sao a mesma coisa.

- model: representa a tabela
- schema: representa o dado que entra ou sai da API

### Arquivos atuais

- `auth/user.py`: schema de criacao de usuario
- `auth/login.py`: schema de login
- `auth/register.py`: schema legado de registro, mantido para estudo e compatibilidade

---

## 5. `back/app/core/`

Essa pasta concentra regras reutilizaveis de autenticacao e seguranca.

### `security.py`

Responsavel por:

- gerar hash de senha
- verificar senha com bcrypt
- criar token JWT
- decodificar token JWT

### `auth.py`

Responsavel por:

- capturar o token Bearer da requisicao
- validar o JWT
- buscar o usuario autenticado no banco
- devolver o usuario atual para rotas protegidas

---

## 6. `back/app/routers/`

Essa pasta contem os endpoints.

### `routers/auth/register.py`

Implementa o cadastro real de usuario com:

- validacao do schema
- verificacao de email duplicado
- verificacao de CPF duplicado
- hash da senha
- persistencia no PostgreSQL

### `routers/auth/login.py`

Implementa o login com:

- busca do usuario por email
- verificacao da senha com bcrypt
- geracao de JWT
- rota protegida `/auth/me`

---

## Como o frontend conversa com o backend

O frontend esta separado da API e envia requisicoes HTTP para as rotas de autenticacao.

Conceitualmente, o fluxo atual e este:

1. a tela de cadastro envia os dados para `/auth/register`
2. a tela de login envia email e senha para `/auth/login`
3. o backend devolve um token JWT
4. o frontend usa esse token em `Authorization: Bearer ...`
5. rotas protegidas, como `/auth/me`, identificam o usuario logado

---

## Leitura recomendada para quem esta estudando

Se voce quer entender o projeto do jeito mais claro possivel, a ordem mais didatica e:

1. `main.py`
2. `database/connection.py`
3. `models/user.py`
4. `schemas/auth/user.py`
5. `routers/auth/register.py`
6. `core/security.py`
7. `routers/auth/login.py`
8. `core/auth.py`

Essa sequencia ajuda a perceber a arquitetura em camadas: entrada, validacao, regra de negocio, persistencia e autenticacao.
