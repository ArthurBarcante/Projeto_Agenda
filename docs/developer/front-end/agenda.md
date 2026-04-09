# Agenda

## O que e

Esta funcionalidade representa a rota autenticada da agenda no frontend.

No estado atual, ela existe apenas como estrutura de navegacao protegida. A tela ainda nao foi preenchida com interface de tarefas ou eventos.

## Arquivos desta funcionalidade

- `front/ui/app/agenda.html`
- `front/js/app/agenda.js`
- `front/js/core/configs/auth.js`
- `front/js/core/api/router.js`

## Responsabilidade de cada arquivo

- `ui/app/agenda.html`: seria o markup da pagina, mas hoje esta vazio.
- `js/app/agenda.js`: protege o acesso da rota e impede que usuarios sem sessao acessem a pagina.
- `js/core/configs/auth.js`: fornece a verificacao de autenticacao usada na rota.
- `js/core/api/router.js`: carrega a pagina quando a rota `#/agenda` e acessada.

## Detalhes

### Tecnologias usadas

- roteamento por hash
- JavaScript modular
- validacao de sessao no cliente

### Comportamento atual

- o usuario precisa estar autenticado para entrar na rota
- se nao estiver autenticado, e redirecionado para login
- a pagina nao apresenta interface nem consumo de API no momento

### Estado atual da funcionalidade

A agenda existe hoje como placeholder tecnico para a proxima fase do frontend.

O que ainda falta nesta funcionalidade:

- layout da pagina
- listagem de tarefas
- listagem de eventos
- formularios de criacao e edicao
- integracao com `GET /tasks`, `POST /tasks`, `GET /events` e demais endpoints