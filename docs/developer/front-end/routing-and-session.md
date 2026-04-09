# Roteamento e sessao

## O que e

Esta funcionalidade organiza como o frontend troca de pagina sem recarregar toda a aplicacao e como a sessao do usuario e mantida entre navegacoes.

Ela e a base tecnica que conecta login, dashboard, paginas protegidas e alternancia entre mock e API real.

## Arquivos desta funcionalidade

- `front/index.html`
- `front/js/core/api/router.js`
- `front/js/core/api/routerRules.js`
- `front/js/core/configs/auth.js`
- `front/js/core/configs/config.js`
- `front/js/core/configs/session.js`
- `front/js/core/api/api.js`
- `front/css/style.css`

## Responsabilidade de cada arquivo

- `front/index.html`: carrega os estilos globais, o container `#app` e o modulo principal de roteamento.
- `js/core/api/router.js`: normaliza rotas, carrega HTML parcial, injeta o script da pagina e trata falhas de carregamento.
- `js/core/api/routerRules.js`: define as regras de acesso publico e privado entre as rotas.
- `js/core/configs/auth.js`: revalida token, decide autenticacao atual e executa logout.
- `js/core/configs/config.js`: centraliza modo de autenticacao e URLs de API.
- `js/core/configs/session.js`: grava token e usuario em armazenamento local e limpa sessao invalida.
- `js/core/api/api.js`: dispara evento de nao autorizado e centraliza chamadas autenticadas.
- `css/style.css`: define reset, variaveis e estilos globais da aplicacao.

## Detalhes

### Tecnologias usadas

- hash routing no navegador
- Fetch API
- `localStorage` para token e usuario
- `sessionStorage` para mensagens temporarias

### Comportamento atual

- a rota inicial cai em login quando nao ha sessao valida
- rotas privadas sao protegidas antes do carregamento da pagina
- a sessao real e revalidada no reload chamando `/auth/me`
- ao receber `401`, o frontend limpa a sessao e volta para o login
- a aplicacao pode alternar entre modo mock e modo real

### Estado atual da funcionalidade

Essa camada esta madura o suficiente para sustentar a expansao do frontend.

O que ainda nao existe nessa funcionalidade:

- carregamento de estado global mais estruturado
- tratamento visual padrao para loading
- cache de dados de dominio alem dos templates HTML