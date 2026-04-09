# Login

## O que e

Esta funcionalidade e a porta de entrada do frontend para a area autenticada do sistema.

Ela coleta email e senha, chama a camada de API, grava a sessao local e redireciona o usuario para o dashboard quando a autenticacao da certo.

## Arquivos desta funcionalidade

- `front/ui/auth/login.html`
- `front/js/auth/login.js`
- `front/js/core/api/api.js`
- `front/js/core/configs/auth.js`
- `front/js/core/configs/session.js`
- `front/css/auth/login.css`

## Responsabilidade de cada arquivo

- `ui/auth/login.html`: define a estrutura visual do formulario de login.
- `js/auth/login.js`: coleta os dados, trata erros, chama a autenticacao e decide a navegacao.
- `js/core/api/api.js`: envia a requisicao para `/auth/login`, busca `/auth/me` e persiste a sessao valida.
- `js/core/configs/auth.js`: decide se o usuario esta autenticado e revalida a sessao quando a pagina recarrega.
- `js/core/configs/session.js`: grava token e usuario no armazenamento local e controla mensagens temporarias de autenticacao.
- `css/auth/login.css`: estiliza o cartao, inputs, botao e estado de erro da tela.

## Detalhes

### Tecnologias usadas

- HTML para a estrutura da pagina
- CSS para o estilo visual
- JavaScript modular com `type="module"`
- Fetch API para comunicacao com o backend
- `localStorage` e `sessionStorage` para sessao e mensagens de estado

### Fluxo atual do login no frontend

1. O usuario preenche email e senha.
2. `login.js` chama `authenticate(email, password)`.
3. `api.js` faz `POST /auth/login`.
4. Se o token vier correto, o frontend chama `GET /auth/me`.
5. Token e usuario sao salvos localmente.
6. A aplicacao navega para o dashboard.

### Comportamento atual

- se o usuario ja estiver autenticado, a tela de login redireciona para o dashboard
- mensagens de erro sao exibidas no proprio formulario
- a autenticacao pode rodar em modo real ou mock, dependendo da configuracao central

### Estado atual da funcionalidade

O login esta funcional no frontend e integrado ao backend real.

O que ainda nao existe nessa funcionalidade:

- feedback visual de carregamento durante a requisicao
- validacoes mais ricas no lado do cliente
- recuperacao de senha
