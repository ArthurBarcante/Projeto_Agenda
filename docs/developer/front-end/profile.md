# Perfil

## O que e

Esta funcionalidade representa a rota autenticada de perfil no frontend.

No estado atual, ela ja existe na navegacao, mas ainda nao possui interface ou logica de exibicao de dados do usuario.

## Arquivos desta funcionalidade

- `front/ui/app/profile.html`
- `front/js/app/profile.js`
- `front/js/core/configs/auth.js`
- `front/js/core/api/router.js`

## Responsabilidade de cada arquivo

- `ui/app/profile.html`: seria o HTML da pagina de perfil, mas hoje esta vazio.
- `js/app/profile.js`: protege a rota e redireciona usuarios sem sessao.
- `js/core/configs/auth.js`: oferece a verificacao de autenticacao usada pela pagina.
- `js/core/api/router.js`: carrega a rota `#/profile` quando o usuario navega pelo sistema.

## Detalhes

### Tecnologias usadas

- roteamento por hash
- JavaScript modular
- verificacao local de sessao

### Comportamento atual

- apenas usuarios autenticados conseguem entrar na rota
- usuarios sem sessao sao enviados para o login
- nao ha exibicao de dados pessoais nem edicao de perfil no estado atual

### Estado atual da funcionalidade

O perfil existe hoje como rota pronta para receber implementacao futura.

O que ainda falta nesta funcionalidade:

- interface de dados do usuario
- edicao de informacoes pessoais
- leitura de dados atuais do usuario autenticado