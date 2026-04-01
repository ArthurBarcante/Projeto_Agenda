# Register (Front-end + Back-end)

## Objetivo deste documento

Este arquivo explica a funcionalidade de cadastro de usuario no sistema, o que ja foi implementado e por que ela e importante para a persistencia real dos dados.

---

## O que e o cadastro neste projeto

Cadastro e o fluxo em que uma pessoa informa seus dados para criar uma conta no sistema.

No projeto atual, esse fluxo trabalha com:

- nome
- email
- senha
- confirmacao de senha
- telefone
- cpf
- data de nascimento
- papel do usuario

Esse conjunto de dados forma o primeiro registro real persistido no PostgreSQL.

---

## O que foi feito

Hoje o cadastro ja esta implementado de ponta a ponta.

### No frontend

Existe uma pagina dedicada para o formulario de cadastro.

Essa tela tem a funcao de:

- coletar os dados do usuario
- enviar os dados para a API
- exibir o retorno de sucesso ou erro

### No backend

Foi criada a rota `POST /auth/register`.

Essa rota executa um fluxo completo:

1. recebe os dados por schema Pydantic
2. valida campos como email e confirmacao de senha
3. verifica se o email ja existe
4. verifica se o CPF ja existe
5. gera hash da senha com `bcrypt`
6. cria o usuario no PostgreSQL
7. devolve uma resposta com os dados basicos do usuario criado

---

## Qual e a funcao do cadastro no sistema

O cadastro e a base da persistencia de usuario.

Sem ele:

- nao existe conta para autenticar
- o login nao tem quem validar
- o sistema nao consegue associar dados a uma pessoa real

Com ele:

- o usuario passa a existir de verdade no banco
- os dados persistem entre execucoes da aplicacao
- o login passa a ter um registro real para autenticar

---

## Fluxo didatico do cadastro

1. o usuario preenche o formulario
2. o frontend envia os dados para `/auth/register`
3. o backend valida o payload
4. o backend verifica duplicidades
5. a senha e transformada em hash
6. o usuario e salvo na tabela `users`
7. a API devolve mensagem de sucesso

---

## Por que esse fluxo e importante para estudo

O cadastro concentra varios conceitos fundamentais de backend em um unico caso de uso:

- validacao com schema
- regra de negocio
- persistencia com ORM
- integridade de dados
- seguranca de senha

Por isso ele e um dos melhores pontos para estudar a arquitetura do projeto.

---

## Resumo tecnico-didatico

Neste projeto, o cadastro nao e apenas um formulario visual. Ele e o primeiro fluxo real de escrita no banco.

Em termos práticos:

- a pagina recolhe os dados
- o backend valida e protege a senha
- o PostgreSQL grava o usuario
- o sistema ganha uma conta autentica para uso futuro
