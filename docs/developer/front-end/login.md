# Login (Front-end + Back-end)

## Objetivo deste documento

Este arquivo explica o que e a funcionalidade de login no sistema, o que ja foi implementado e qual e o papel dela no fluxo geral da aplicacao.

---

## O que e o login neste projeto

Login e o processo de autenticar um usuario que ja foi cadastrado.

No projeto, isso significa receber:

- email
- senha

e verificar se essas informacoes pertencem a um usuario valido salvo no banco.

O login envolve duas partes:

- a pagina do frontend, onde a pessoa digita os dados
- a rota do backend, que valida as credenciais e devolve um token JWT

---

## O que foi feito

Hoje o fluxo de login ja esta implementado com autenticacao real.

### No frontend

A interface de login existe como pagina dedicada dentro da estrutura de UI do projeto.

Ela tem a funcao de:

- capturar email e senha
- enviar esses dados para a API
- receber a resposta do backend

### No backend

Foi criada a rota `POST /auth/login`.

Essa rota faz o seguinte:

1. recebe os dados por schema
2. busca o usuario no PostgreSQL pelo email
3. verifica a senha com `bcrypt`
4. se estiver tudo certo, gera um token JWT
5. devolve `access_token` e `token_type`

Tambem foi criada a rota `GET /auth/me`, que usa esse token para descobrir quem esta autenticado.

---

## Qual e a funcao do login no sistema

O login e a porta de entrada para as partes protegidas da aplicacao.

Sem ele:

- o sistema nao sabe quem esta usando a aplicacao
- nao e possivel proteger funcionalidades por usuario
- nao e possivel ligar dados da agenda ao dono correto

Com ele:

- o backend reconhece o usuario
- o frontend pode guardar o token e reutiliza-lo
- rotas privadas passam a funcionar com autenticacao real

---

## Fluxo didatico do login

1. o usuario preenche email e senha na pagina
2. o frontend envia esses dados para `/auth/login`
3. o backend localiza o usuario pelo email
4. o backend compara a senha digitada com o hash salvo
5. se estiver correto, o backend gera um JWT
6. o frontend usa esse token nas proximas requisicoes

---

## Por que o token e importante

Depois que o login acontece, o sistema nao precisa pedir email e senha a cada nova requisicao.

Em vez disso, o frontend envia algo assim:

```text
Authorization: Bearer TOKEN
```

O backend le esse token e identifica o usuario autenticado.

Esse modelo e chamado de autenticacao stateless e e muito usado em APIs modernas.

---

## Resumo tecnico-didatico

Neste projeto, o login nao e apenas uma tela. Ele e uma funcionalidade completa que conecta interface, validacao, banco de dados e JWT.

Em termos práticos:

- a pagina coleta os dados
- a rota valida email e senha
- o backend gera o token
- o sistema passa a reconhecer o usuario logado
