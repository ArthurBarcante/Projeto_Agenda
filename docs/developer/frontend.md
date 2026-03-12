# Frontend

O frontend esta organizado com Next.js, React e TypeScript.

A estrutura segue uma divisao por rotas, features, servicos compartilhados e hooks reutilizaveis.

## Estrutura geral

Os pontos centrais do frontend ficam em `frontend/src/`.

- `app/`: rotas, layouts e providers.
- `features/`: organizacao por dominio funcional.
- `components/`: componentes compartilhados.
- `hooks/`: hooks reutilizaveis fora de uma feature especifica.
- `services/`: infraestrutura de comunicacao com a API.
- `utils/`: utilitarios de apoio.

## Routing

O projeto usa o App Router do Next.js.

As paginas atuais ficam em `frontend/src/app/` com route groups para separar fluxos autenticados e nao autenticados.

Exemplos:

- `(auth)/signin/page.tsx`
- `(dashboard)/dashboard/page.tsx`
- `(dashboard)/appointments/page.tsx`
- `(dashboard)/profile/page.tsx`

Essa organizacao deixa claro quais paginas pertencem ao fluxo publico e quais pertencem a area interna.

Na documentacao, o fluxo e descrito como `login` ou `autenticacao`.

No codigo do frontend, a rota concreta desse fluxo aparece como `signin`.

## Layouts e providers

O frontend possui layouts e providers em pastas dedicadas.

- `layout/`: layouts como `MainLayout` e `DashboardLayout`.
- `providers/`: contexto de autenticacao e tema.

O objetivo desses arquivos e concentrar comportamento transversal, evitando repeticao nas paginas.

## Features

As features agrupam codigo por objetivo de negocio.

As areas atuais sao:

- `features/auth/`
- `features/appointments/`
- `features/users/`

Dentro de cada feature aparecem, quando necessario:

- `pages/`
- `services/`
- `hooks/`
- `types.ts`

Essa escolha reduz acoplamento entre dominios e ajuda o aluno ou desenvolvedor a encontrar rapidamente tudo o que pertence a uma funcionalidade.

## Components

Os componentes compartilhados ficam em `frontend/src/components/`.

Hoje a pasta ja reserva espacos para:

- `Button/`
- `Input/`
- `Modal/`
- `Table/`

Mesmo que varios desses diretórios ainda estejam vazios, a intencao arquitetural e boa: componentes genericos devem ficar fora das features para serem reutilizados com facilidade.

## Services

O servico HTTP comum esta em `frontend/src/services/api.ts`.

Esse arquivo centraliza:

- URL base da API;
- mapa de endpoints;
- funcao HTTP generica;
- tratamento padrao de erro com `HttpError`.

As features usam esse servico em vez de falar diretamente com `fetch` em varios lugares.

Exemplo:

- `features/auth/services/authService.ts` usa o cliente compartilhado para chamar `/auth/login`.

## Hooks

Os hooks compartilhados atuais sao:

- `useAuth.ts`
- `useDebounce.ts`

Nas features tambem existem hooks especificos, como `useAppointments.ts`.

O objetivo dos hooks e encapsular estado e comportamento reutilizavel sem poluir componentes de pagina.

## Como o frontend conversa com o backend

O fluxo principal e este:

1. A pagina renderiza a interface.
2. Um componente ou hook chama um service.
3. O service usa `api.ts` para enviar a requisicao.
4. O backend responde.
5. A pagina atualiza o estado e a interface.

## Observacoes sobre o estado atual

O frontend ja tem uma base coerente de organizacao, mas ainda possui varias telas de placeholder.

Isso significa que a estrutura esta mais madura do que a quantidade de funcionalidades visiveis.

Para contribuir com consistencia, prefira adicionar novos arquivos dentro da feature correta e reutilizar `api.ts`, layouts e hooks compartilhados.