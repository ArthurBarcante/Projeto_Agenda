# Eventos

## O que e

Esta funcionalidade implementa o CRUD de eventos do sistema. Assim como nas tarefas, cada evento pertence a um usuario autenticado.

No estado atual do projeto, o backend desta funcionalidade esta pronto, enquanto o frontend ainda nao possui tela para consumi-lo.

## Arquivos desta funcionalidade

- `back/app/routers/agenda/events.py`
- `back/app/models/events.py`
- `back/app/schemas/agenda/events.py`
- `back/app/core/auth.py`
- `back/app/models/user.py`

## Responsabilidade de cada arquivo

- `routers/agenda/events.py`: define as rotas de criar, listar, consultar, atualizar e excluir eventos.
- `models/events.py`: descreve a tabela `events` e seus campos persistidos.
- `schemas/agenda/events.py`: valida payloads e resposta da API, incluindo a validacao de intervalo de datas.
- `core/auth.py`: protege os endpoints por usuario autenticado.
- `models/user.py`: sustenta o relacionamento entre usuario e eventos.

## Detalhes

### Tecnologias usadas

- FastAPI para endpoints REST
- SQLAlchemy para acesso a banco
- Pydantic para validacao
- JWT para identificar o usuario da requisicao

### Endpoints implementados

- `POST /events`
- `GET /events`
- `GET /events/{event_id}`
- `PUT /events/{event_id}`
- `DELETE /events/{event_id}`

### Modelo atual do evento

A entidade de evento possui hoje:

- `title`
- `description`
- `start_at`
- `end_at`
- `location`
- `user_id`

### Comportamento atual

- todo evento criado recebe o `user_id` do usuario autenticado
- a listagem retorna apenas eventos do usuario logado
- busca, atualizacao e exclusao usam filtro por id e por usuario
- o schema impede `end_at` menor que `start_at`

### Estado atual da funcionalidade

A API de eventos ja pode ser usada por clientes autenticados e esta pronta para ser integrada ao frontend.

O que ainda nao existe nessa funcionalidade:

- interface visual para agenda e calendario
- visualizacao por dia, semana ou mes
- regras de conflito entre eventos