# Tarefas

## O que e

Esta funcionalidade implementa o CRUD de tarefas da API. Cada tarefa pertence a um usuario autenticado, e todas as operacoes sao filtradas por `user_id`.

No estado atual do projeto, esta parte ja esta pronta no backend, mas ainda nao foi integrada a uma interface visual no frontend.

## Arquivos desta funcionalidade

- `back/app/routers/agenda/tasks.py`
- `back/app/models/tasks.py`
- `back/app/schemas/agenda/tasks.py`
- `back/app/core/auth.py`
- `back/app/models/user.py`

## Responsabilidade de cada arquivo

- `routers/agenda/tasks.py`: define as rotas de criar, listar, consultar, atualizar e excluir tarefas.
- `models/tasks.py`: descreve a tabela `tasks` e seus campos persistidos.
- `schemas/agenda/tasks.py`: valida os dados de entrada e define o formato de resposta da API.
- `core/auth.py`: garante que apenas usuarios autenticados acessem a funcionalidade.
- `models/user.py`: sustenta o relacionamento entre usuario e tarefas.

## Detalhes

### Tecnologias usadas

- FastAPI para endpoints REST
- SQLAlchemy para consultas e persistencia
- Pydantic para contratos de entrada e saida
- JWT para autenticacao via dependencia compartilhada

### Endpoints implementados

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

### Modelo atual da tarefa

A entidade de tarefa possui hoje:

- `title`
- `description`
- `completed`
- `due_date`
- `user_id`

### Comportamento atual

- toda tarefa criada recebe o `user_id` do usuario autenticado
- a listagem retorna apenas tarefas do usuario logado
- busca, atualizacao e exclusao falham com `404` quando a tarefa nao pertence ao usuario ou nao existe
- atualizacao aceita apenas os campos enviados, usando update parcial pelo schema

### Estado atual da funcionalidade

A API de tarefas ja esta operacional e pronta para consumo por frontend ou cliente externo autenticado.

O que ainda nao existe nessa funcionalidade:

- interface visual para listar e editar tarefas
- ordenacao mais rica por prazo ou status
- filtros por periodo, prioridade ou categoria