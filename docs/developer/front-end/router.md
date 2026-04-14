# Router

A pasta `front/router` contém a navegação SPA:

- `router.js`: carregamento de páginas e scripts por rota.
- `routerRules.js`: regras de proteção por autenticação.

## Estado atual

Hoje o roteador já protege rotas internas como dashboard, agenda, create-item, perfil e missões.

Ele também evita acessos indevidos quando a sessão não está ativa.
