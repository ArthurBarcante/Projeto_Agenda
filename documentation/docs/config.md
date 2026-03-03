# Página de Config

Esta página consolida as tecnologias usadas no projeto e o papel de cada uma.

## Onde ficam as configurações

```text
config/
├── .env
├── .gitignore
├── alembic.ini
└── requirements.txt
```

Além desta pasta, o frontend mantém suas configurações em `frontend/aigenda-frontend/` (`package.json`, `next.config.ts`, `tsconfig.json`, `tailwind.config.ts`, `postcss.config.mjs`, `eslint.config.mjs`).

## Stack do backend (Python)

- **FastAPI**: framework da API HTTP.
- **Uvicorn**: servidor ASGI para execução da API.
- **SQLAlchemy**: ORM e camada de acesso ao banco.
- **Alembic**: versionamento e execução de migrações.
- **PostgreSQL + psycopg2-binary**: banco relacional e driver.
- **Pydantic**: validação e serialização de dados.
- **python-jose**: geração/validação de JWT.
- **passlib + bcrypt**: hash e verificação de senha.
- **python-dotenv**: leitura de variáveis de ambiente.
- **pytest**: testes automatizados.

## Stack do frontend (JavaScript/TypeScript)

- **Next.js**: framework React full-stack do frontend.
- **React / React DOM**: base da interface.
- **TypeScript**: tipagem estática no frontend.
- **Tailwind CSS**: utilitários de estilo.
- **PostCSS + Autoprefixer**: processamento de CSS.
- **ESLint + eslint-config-next**: lint e padronização do código.

## Objetivo da pasta `config`

- Centralizar o que define comportamento do projeto em ambiente local e CI.
- Facilitar onboarding de novos desenvolvedores.
- Evitar configurações espalhadas sem padrão.
