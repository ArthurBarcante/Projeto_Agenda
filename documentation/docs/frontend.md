# Página do Frontend

Esta página descreve a estrutura do frontend e a função de cada arquivo principal.

## Estrutura do frontend

```text
frontend/
└── aigenda-frontend/
    ├── package.json
    ├── package-lock.json
    ├── next.config.ts
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── postcss.config.mjs
    ├── eslint.config.mjs
    ├── next-env.d.ts
    ├── .gitignore
    ├── public/
    │   ├── file.svg
    │   ├── globe.svg
    │   ├── next.svg
    │   ├── vercel.svg
    │   └── window.svg
    └── src/
        ├── app/
        │   ├── layout.tsx
        │   ├── page.tsx
        │   ├── globals.css
        │   ├── favicon.ico
        │   ├── (auth)/
        │   │   └── entrar/page.tsx
        │   └── (dashboard)/
        │       ├── painel/page.tsx
        │       ├── compromissos/page.tsx
        │       └── perfil/page.tsx
        ├── features/
        │   ├── autenticacao/
        │   │   ├── ui/EntrarView.tsx
        │   │   └── services/autenticacaoService.ts
        │   ├── compromissos/
        │   │   ├── ui/CompromissosView.tsx
        │   │   ├── ui/PainelView.tsx
        │   │   ├── hooks/useCompromissos.ts
        │   │   └── services/compromissosService.ts
        │   └── usuarios/
        │       └── ui/PerfilView.tsx
        ├── shared/
        │   ├── components/PaginaBase.tsx
        │   ├── lib/formatarDataHora.ts
        │   └── types/compromisso.ts
        ├── store/README.md
        └── styles/README.md
```

## Explicação breve por arquivo

### Configuração do projeto

- `package.json`: scripts e dependências do frontend.
- `next.config.ts`: configuração do Next.js.
- `tsconfig.json`: configuração TypeScript.
- `tailwind.config.ts`: configuração do Tailwind CSS.
- `postcss.config.mjs`: pipeline PostCSS para Tailwind/autoprefixer.
- `eslint.config.mjs`: regras de lint do projeto.
- `next-env.d.ts`: tipos automáticos do Next.js para TypeScript.

### App Router (src/app)

- `src/app/layout.tsx`: layout raiz da aplicação.
- `src/app/page.tsx`: página de entrada com links para os fluxos principais.
- `src/app/globals.css`: estilos globais.
- `src/app/(auth)/entrar/page.tsx`: rota de autenticação.
- `src/app/(dashboard)/painel/page.tsx`: visão geral da área autenticada.
- `src/app/(dashboard)/compromissos/page.tsx`: listagem de compromissos.
- `src/app/(dashboard)/perfil/page.tsx`: dados de perfil.

### Responsabilidade por página

- `/`: ponto de entrada e redirecionamento de navegação entre área pública e área autenticada.
- `/entrar`: autenticação (empresa, e-mail e senha) e obtenção de token de acesso.
- `/painel`: resumo operacional com atalhos para fluxos principais.
- `/compromissos`: listagem, busca e navegação de compromissos.
- `/perfil`: visualização e manutenção de dados do usuário autenticado.

### Organização por domínio

- `src/features/`: módulos funcionais por domínio (UI, hooks e services).
- `src/shared/`: componentes base, utilitários e tipos reutilizáveis.
- `src/store/`: estado global compartilhado entre features.
- `src/styles/`: estilos/tokens adicionais além do global.

### Assets

- `public/*.svg`: ícones e imagens públicas consumidas pelo frontend.

## Observação importante

- A pasta `.next/` é artefato de build/dev do Next.js e não representa código-fonte de domínio.
