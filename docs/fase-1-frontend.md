# Fase 1 — Frontend

O frontend da Fase 1 entrega a camada de experiência da Organização Inteligente: autenticação, navegação de área autenticada e visualização dos compromissos com base na API.

## Base tecnológica

- Next.js (App Router)
- React + TypeScript
- Tailwind CSS

## Estrutura funcional da Fase 1

### Rotas de aplicação (`frontend/src/app`)

- `(auth)/entrar/page.tsx`: entrada/autenticação do usuário.
- `(dashboard)/painel/page.tsx`: visão de painel após login.
- `(dashboard)/compromissos/page.tsx`: visão focada em compromissos.
- `(dashboard)/perfil/page.tsx`: dados e contexto de perfil.

### Features por domínio (`frontend/src/features`)

- `autenticacao/`: tipos, serviços HTTP e UI de login.
- `compromissos/`: hooks, serviços, tipos e telas de compromissos/painel.
- `usuarios/`: UI de perfil.

### Camada compartilhada (`frontend/src/shared`)

- `api/`: cliente HTTP e endpoints centralizados.
- `components/`: componentes base reutilizáveis.
- `lib/`: utilitários de formatação e funções auxiliares.
- `types/`: tipagens compartilhadas.

## Resultado da Fase 1 no frontend

- Fluxo de autenticação inicial definido.
- Área de dashboard segregada por contexto de uso.
- Base modular para evolução das fases 2, 3 e 4 sem quebra estrutural.
