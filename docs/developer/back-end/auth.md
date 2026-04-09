# Autenticacao

## O que e

Esta funcionalidade concentra o fluxo de identidade do sistema: cadastro, login, geracao de token e leitura do usuario autenticado.

No estado atual do projeto, ela e a parte mais completa do backend e tambem a base para proteger tarefas e eventos por usuario.

## Arquivos desta funcionalidade

- `back/app/routers/auth/register.py`
- `back/app/routers/auth/login.py`
- `back/app/core/security.py`
- `back/app/core/auth.py`
- `back/app/models/user.py`
- `back/app/schemas/auth/user.py`
- `back/app/schemas/auth/login.py`
- `back/app/database/deps.py`

## Responsabilidade de cada arquivo

- `register.py`: recebe o cadastro, valida duplicidade de email e CPF, gera hash da senha e persiste o usuario.
- `login.py`: recebe email e senha, valida as credenciais, gera o JWT e expoe a rota protegida `/auth/me`.
- `security.py`: centraliza hash de senha, verificacao de senha, criacao de token e decodificacao de token.
- `auth.py`: implementa a dependencia `get_current_user`, que le o token Bearer, extrai o `sub` e busca o usuario no banco.
- `user.py`: define a tabela `users` e os relacionamentos com tarefas e eventos.
- `schemas/auth/user.py`: valida a entrada do cadastro, incluindo confirmacao de senha.
- `schemas/auth/login.py`: valida a entrada do login.
- `database/deps.py`: entrega a sessao de banco por requisicao para as rotas que precisam do SQLAlchemy.

## Detalhes

### Tecnologias usadas

- FastAPI para expor as rotas
- Pydantic para validar payloads
- SQLAlchemy para leitura e escrita no banco
- PostgreSQL como persistencia principal
- bcrypt para proteger senha
- python-jose para JWT

### Fluxo de cadastro

1. A requisicao chega em `POST /auth/register`.
2. O schema valida formato e confirmacao de senha.
3. A rota verifica email e CPF duplicados.
4. A senha e transformada em hash.
5. O usuario e salvo na tabela `users`.
6. A resposta devolve mensagem de sucesso e dados basicos do usuario.

### Fluxo de login

1. A requisicao chega em `POST /auth/login`.
2. O backend busca o usuario pelo email.
3. A senha enviada e comparada com o hash salvo.
4. Se estiver correta, o backend gera um JWT com `sub` igual ao id do usuario.
5. O cliente pode reutilizar esse token nas rotas protegidas.

### Fluxo de usuario autenticado

1. O cliente envia `Authorization: Bearer TOKEN`.
2. `get_current_user` decodifica o token.
3. O `sub` e convertido para inteiro.
4. O usuario e buscado no banco.
5. A rota protegida recebe o usuario ja resolvido.

### Estado atual da funcionalidade

O fluxo de autenticacao esta funcional de ponta a ponta e possui testes automatizados para cadastro, login e `/auth/me`.

O que ainda nao existe nessa funcionalidade:

- refresh token
- revogacao de token
- permissao por papel de usuario
- recuperacao de senha