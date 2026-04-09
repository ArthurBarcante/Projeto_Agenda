# Quais funcoes o projeto tem hoje

Este arquivo mostra o que o Projeto Agenda ja faz hoje e o que ainda vai ser implementado.

Como o projeto esta em desenvolvimento, e importante separar bem o que ja existe de verdade do que ainda esta planejado.

## Funcoes ja implementadas atualmente

### 1. Cadastro de usuario

Uma pessoa ja pode criar conta informando dados como:

- nome
- email
- senha
- telefone
- CPF
- data de nascimento

O sistema tambem valida:

- se a senha e a confirmacao batem
- se o email ja esta cadastrado
- se o CPF ja esta cadastrado

### 2. Login

O usuario ja pode entrar com email e senha.

Quando o login da certo, o sistema gera um token e passa a reconhecer quem esta autenticado.

### 3. Identificacao do usuario logado

Depois do login, o backend consegue verificar quem esta usando o sistema naquele momento.

Isso e importante porque tarefas e eventos precisam pertencer a um usuario especifico.

### 4. Tarefas no backend

O backend ja possui funcoes para:

- criar tarefa
- listar tarefas
- buscar uma tarefa especifica
- atualizar tarefa
- excluir tarefa

Importante: essa parte ja existe na API, mas ainda nao possui interface pronta no frontend.

### 5. Eventos no backend

O backend ja possui funcoes para:

- criar evento
- listar eventos
- buscar um evento especifico
- atualizar evento
- excluir evento

Assim como acontece com as tarefas, essa parte ja existe internamente no backend, mas ainda nao esta pronta visualmente no frontend.

### 6. Interface inicial do sistema

No frontend, hoje ja existem:

- tela de login
- tela de cadastro
- dashboard inicial
- menu lateral para navegar entre paginas autenticadas

### 7. Modo real e modo mock

O frontend pode funcionar de dois jeitos:

- conectado na API real
- conectado em um mock local para testes

## Funcoes que ainda vao ser implementadas

Estas partes ainda nao estao prontas no estado atual do projeto:

- interface completa da agenda
- interface completa de perfil
- uso visual de tarefas no frontend
- uso visual de eventos no frontend
- organizacao de rotina mais avancada
- recursos de progresso, acompanhamento ou motivacao

## Resumindo

Hoje o projeto ja tem uma base funcional importante:

- autenticacao real
- usuarios salvos em banco de dados
- tarefas e eventos no backend
- interface inicial para entrar na aplicacao

O que falta agora e transformar as funcoes que ja existem no backend em experiencia visual completa no frontend.
