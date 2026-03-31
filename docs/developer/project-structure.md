# Estrutura do Projeto (Developer)

Data da analise: 31 de marco de 2026

## 1. Visao Tecnica Geral

Este projeto esta organizado em quatro blocos principais:

- `front/`: interface web (HTML, CSS, JS modular)
- `back/`: API em FastAPI
- `docs/`: documentacao para iniciantes e devs
- `tests/`: scripts de teste/simulacao

Tambem existem pastas de suporte:

- `.venv/`: ambiente virtual Python da raiz
- `configs/`: configuracoes de ambiente/dependencias
- `.vscode/`: configuracoes locais de editor/debug

## 2. Arvore Atual do Projeto

Observacao:
- `.venv/` e `node_modules/` existem, mas nao sao expandidas aqui por tamanho.

```text
Projeto_Agenda/
├── .gitignore
├── .venv/
├── .vscode/
│   ├── launch.json
│   └── settings.json
├── README.md
├── back/
│   ├── app/
│   │   ├── __pycache__/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __pycache__/
│   │   │   └── fake_db.py
│   │   ├── routers/
│   │   │   └── auth/
│   │   │       ├── __pycache__/
│   │   │       ├── login.py
│   │   │       └── register.py
│   │   └── schemas/
│   │       └── auth/
│   │           ├── __pycache__/
│   │           ├── login.py
│   │           └── register.py
│   └── mock/
│       └── db.json
├── configs/
│   └── requirements.txt
├── docs/
│   ├── beginner/
│   └── developer/
│       ├── back-end/
│       │   ├── models.md
│       │   ├── routers.md
│       │   └── schemas.md
│       ├── front-end/
│       │   ├── css.md
│       │   ├── js.md
│       │   └── ui.md
│       └── project-structure.md
├── front/
│   ├── css/
│   │   ├── auth/
│   │   │   ├── login.css
│   │   │   └── register.css
│   │   └── style.css
│   ├── index.html
│   ├── js/
│   │   ├── auth/
│   │   │   ├── login.js
│   │   │   └── register.js
│   │   └── core/
│   │       ├── api.js
│   │       └── router.js
│   └── ui/
│       └── auth/
│           ├── login.html
│           └── register.html
├── node_modules/
└── tests/
    ├── back/
    │   └── test.py
    └── front/
        └── login-simulation.js
```

## 3. Responsabilidade de Cada Camada

### 3.1 Backend (`back/app`)

- `main.py`: cria a instancia FastAPI, registra middlewares (CORS) e inclui routers.
- `models/fake_db.py`: "banco" em memoria para simular persistencia.
- `schemas/auth/*.py`: contratos de entrada (Pydantic) para login e registro.
- `routers/auth/*.py`: regras de negocio de autenticacao.

Fluxo simplificado no backend:

1. Request chega no endpoint.
2. Pydantic valida payload via schema.
3. Router executa regra de negocio.
4. Resposta JSON e retornada.

### 3.2 Frontend (`front`)

- `index.html`: shell principal da SPA simples.
- `js/core/router.js`: troca dinamica de telas (`login` e `register`).
- `js/core/api.js`: camada de integracao HTTP.
- `js/auth/*.js`: comportamento de cada tela (eventos, validacoes, chamadas de API).
- `ui/auth/*.html`: templates de interface.
- `css/auth/*.css` e `css/style.css`: apresentacao visual.

### 3.3 Dados Mock (`back/mock/db.json`)

Base usada com JSON Server para desenvolvimento rapido no frontend.

### 3.4 Documentacao (`docs`)

- `docs/beginner/`: explicacoes para publico nao tecnico.
- `docs/developer/`: visao tecnica para quem esta estudando desenvolvimento.

## 4. Integracao Mock x API Real

No frontend, `front/js/core/api.js` possui uma chave de alternancia:

- `USE_REAL_API = false` -> usa JSON Server (`localhost:3000`)
- `USE_REAL_API = true` -> usa FastAPI (`127.0.0.1:8000`)

Essa abordagem reduz acoplamento durante estudo e facilita migracao gradual para backend real.

## 5. Pontos de Atencao Tecnicos

- A pasta `__pycache__/` nao deve ser versionada em Git.
- `configs/requirements.txt` precisa refletir as dependencias reais do backend.
- O fake DB em memoria (`fake_db.py`) e util para aprendizado, mas nao substitui persistencia real.
- O projeto ainda esta em fase de consolidacao de testes automatizados.

## 6. Resumo para Estudantes de Desenvolvimento

Este projeto e um bom exemplo de arquitetura didatica em camadas:

- camada de interface (UI)
- camada de comportamento (JS de pagina)
- camada de acesso a dados (API client)
- camada de API (FastAPI)
- camada de contrato (schemas)
- camada de dados simulados (mock/in-memory)

A estrutura atual facilita estudar separacao de responsabilidades, evolucao incremental e migracao de mock para backend real.
