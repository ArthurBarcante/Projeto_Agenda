# Routers no Back-end

## O que e um router
No FastAPI, um **router** organiza endpoints por contexto de negocio.

Em vez de colocar tudo em `main.py`, cada grupo de rotas fica em modulos separados. Isso melhora legibilidade, manutencao e escalabilidade.

Arquivos atuais:
- `back/app/routers/auth/login.py`
- `back/app/routers/auth/register.py`

## Como os routers estao organizados
Ambos os routers usam:
- `APIRouter(prefix="/auth", tags=["Auth"])`

Isso significa que os endpoints ficam agrupados sob `/auth` e aparecem categorizados como **Auth** no Swagger.

### Login Router
Arquivo: `back/app/routers/auth/login.py`

Endpoint atual:
- `POST /auth/login`

Fluxo:
1. recebe `email` e `password` via schema `LoginRequest`
2. percorre `users_db`
3. se encontrar correspondencia, retorna mensagem e dados basicos do usuario
4. se nao encontrar, retorna `401` com detalhe de credenciais invalidas

### Register Router
Arquivo: `back/app/routers/auth/register.py`

Endpoint atual:
- `POST /auth/register`

Fluxo:
1. recebe payload tipado por `RegisterRequest`
2. valida duplicidade de email
3. valida duplicidade de CPF
4. cria novo usuario com `id` incremental
5. adiciona em `users_db`
6. retorna mensagem e resumo do usuario criado

## Integracao com o app principal
Os routers sao conectados em `back/app/main.py` com:
- `app.include_router(auth_login.router)`
- `app.include_router(register.router)`

Esse padrao permite adicionar novos modulos de rota com baixo acoplamento.

## Boas praticas observadas
- separacao entre rotas de login e registro
- uso de schemas para validar entrada
- retorno de erros HTTP com status adequados (400 e 401)
- prefixo e tags padronizados

## Pontos de melhoria tecnica
Para evoluir a camada de routers:
1. mover regras de negocio para camada de servicos
2. deixar routers focados em I/O (request/response)
3. padronizar formato de resposta e erros
4. adicionar testes de rota com `TestClient`
5. introduzir autenticacao por token (JWT) nas rotas protegidas

Com isso, os routers ficam mais limpos e o back-end cresce com menos risco de regressao.
