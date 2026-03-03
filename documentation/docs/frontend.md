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
        │   ├── (auth)/.gitkeep
        │   └── (dashboard)/.gitkeep
        ├── features/
        ├── shared/
        ├── store/
        └── styles/
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
- `src/app/page.tsx`: página inicial atual do frontend.
- `src/app/globals.css`: estilos globais.
- `src/app/(auth)/.gitkeep`: reserva da área de autenticação.
- `src/app/(dashboard)/.gitkeep`: reserva da área de dashboard.

### Organização por domínio

- `src/features/`: módulos funcionais do produto (appointments, auth, users).
- `src/shared/`: componentes e utilitários compartilhados.
- `src/store/`: estado global da aplicação.
- `src/styles/`: estilos organizados fora do escopo global.

### Assets

- `public/*.svg`: ícones e imagens públicas consumidas pelo frontend.

## Observação importante

- A pasta `.next/` é artefato de build/dev do Next.js e não representa código-fonte de domínio.
