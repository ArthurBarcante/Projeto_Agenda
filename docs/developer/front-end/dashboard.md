# Dashboard

## O que e

Esta funcionalidade representa a primeira area autenticada do frontend.

Hoje ela funciona como pagina inicial apos o login e serve como ponto de entrada para a navegacao interna do sistema.

## Arquivos desta funcionalidade

- `front/ui/app/dashboard.html`
- `front/js/app/dashboard.js`
- `front/js/components/sidebar/sideBar.js`
- `front/js/components/sidebar/sideBarController.js`
- `front/js/core/configs/auth.js`
- `front/css/app/dashboard.css`
- `front/css/components/sideBar.css`

## Responsabilidade de cada arquivo

- `ui/app/dashboard.html`: define o ponto de montagem da pagina autenticada.
- `js/app/dashboard.js`: protege a rota, monta o conteudo inicial do dashboard e injeta a sidebar.
- `js/components/sidebar/sideBar.js`: gera o HTML do menu lateral.
- `js/components/sidebar/sideBarController.js`: conecta abertura, fechamento, clique em links e logout.
- `js/core/configs/auth.js`: verifica se a sessao e valida antes de permitir acesso.
- `css/app/dashboard.css`: estiliza a area principal do dashboard.
- `css/components/sideBar.css`: estiliza a sidebar, overlay e botao de logout.

## Detalhes

### Tecnologias usadas

- HTML parcial carregado dinamicamente
- JavaScript modular para montagem da tela
- CSS dedicado para dashboard e menu lateral

### Comportamento atual

- usuarios nao autenticados sao redirecionados para o login
- o dashboard renderiza uma mensagem inicial simples
- a sidebar oferece acesso a dashboard, agenda, perfil e logout
- em telas menores, o menu lateral abre por botao e fecha com overlay

### Estado atual da funcionalidade

O dashboard ja funciona como shell autenticado da aplicacao.

O que ainda nao existe nessa funcionalidade:

- widgets reais de produtividade
- resumo de tarefas e eventos
- indicadores de progresso