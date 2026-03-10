# Testes

## Estrategia

A suite foi organizada por fase de produto e por nivel de teste:

- `tests/fase_1_organizacao_inteligente/`
- `tests/fase_2_engajamento/`

Dentro de cada fase:

- `unit/`: regra isolada.
- `integration/`: integracao entre componentes.
- `e2e/`: fluxo completo.

## Execucao

## Backend (pytest)

```bash
source .venv/bin/activate
pytest
```

## Frontend (vitest)

```bash
cd frontend
npm run test:fase2
```

## Configuracoes relevantes

- `tests/conftest.py` carrega fixtures compartilhadas.
- Se `DATABASE_URL` nao estiver definido, o setup de testes usa SQLite em memoria.
- `pyproject.toml` define `pythonpath = ["backend"]` e `testpaths = ["tests"]`.

## Cobertura funcional atual (resumo)

- conflito de horario;
- idempotencia;
- enforce de tenant;
- autorizacao RBAC;
- rate limit;
- fluxo de outbox;
- calculos do modulo de engajamento.
