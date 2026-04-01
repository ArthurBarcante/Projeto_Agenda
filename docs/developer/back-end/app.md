# App (Back-end)

## Objetivo deste documento

Este arquivo explica a parte mais basica da aplicacao backend: a estrutura que permite a API existir, conversar com o banco e organizar os dados de entrada e saida.

Pense nele como o "esqueleto" do back-end.

---

## O que e a camada `app`

Dentro de `back/app/` ficam os arquivos principais da API.

Essa camada junta quatro responsabilidades que costumam aparecer em qualquer backend moderno:

- inicializacao da API
- conexao com banco de dados
- modelos persistidos
- schemas de validacao

Mesmo sendo partes diferentes, elas trabalham em conjunto.

---

## O que foi feito nesta parte do projeto

Hoje, a camada `app` ja foi estruturada com os elementos essenciais para uma aplicacao real:

### 1. Inicializacao da API

Em `main.py` foi criado o ponto de entrada da aplicacao FastAPI.

Esse arquivo:

- instancia o `FastAPI()`
- registra CORS
- importa os routers de autenticacao
- executa `Base.metadata.create_all(bind=engine)` para criar as tabelas mapeadas

### 2. Base de banco de dados

Na pasta `database/` foram criados os arquivos fundamentais do SQLAlchemy:

- `base.py`: define o `Base`
- `connection.py`: cria `engine` e `SessionLocal`
- `deps.py`: entrega uma sessao de banco por requisicao

### 3. Modelo de usuario

Em `models/user.py` foi criado o modelo `User`, que representa a tabela `users` no PostgreSQL.

Esse modelo inclui os campos principais do cadastro:

- nome
- email
- senha
- telefone
- cpf
- data de nascimento
- papel do usuario

### 4. Schemas da API

Na pasta `schemas/auth/` foram criados os contratos de entrada usados pelas rotas.

Esses schemas validam os dados recebidos antes de chegar na regra de negocio.

Exemplo:

- validar formato de email
- garantir que senha e confirmacao de senha coincidam

---

## Qual e a funcao dessa parte no sistema

A funcao da camada `app` e dar base para todo o resto.

Sem ela:

- a API nao sobe
- o banco nao conecta
- os modelos nao existem
- os dados recebidos nao sao validados

Com ela, o sistema ganha organizacao em camadas.

Isso permite separar melhor:

- o que e dado de entrada
- o que e regra de negocio
- o que e estrutura de banco

---

## Como essas pecas se encaixam

Fluxo simplificado:

1. a requisicao chega em uma rota
2. o schema valida os dados
3. a rota usa uma sessao do banco
4. o modelo define como salvar ou consultar os dados
5. a API devolve a resposta

Esse desenho e importante para quem esta estudando, porque mostra a separacao de responsabilidades de um backend real.

---

## Resumo tecnico-didatico

Quando voce olha para a pasta `app`, nao deve pensar apenas em "arquivos soltos". Ela e a camada central que sustenta a API.

Em termos práticos:

- `main.py` liga a aplicacao
- `database/` liga a API ao PostgreSQL
- `models/` descreve as tabelas
- `schemas/` protege a entrada de dados
- `routers/` executa as regras

Essa base ja esta pronta para continuar evoluindo o sistema de agenda.
