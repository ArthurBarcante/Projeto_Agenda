# Contribuindo com o Projeto

## Fluxo recomendado

1. Crie branch a partir da `main`.
2. Implemente a alteracao com testes.
3. Rode validacoes locais.
4. Abra Pull Request com contexto tecnico.

## Comandos uteis

```bash
# backend
source .venv/bin/activate
pytest

# frontend
cd frontend
npm run lint
npm run test:fase2
```

## Checklist para PR

- mudanca documentada em `docs/` quando necessario;
- testes novos/atualizados para comportamento alterado;
- sem regressao de contratos de API;
- mensagens e codigos de erro consistentes.

## Boas praticas

- mantenha separacao Router -> Service -> Repository;
- preserve isolamento de tenant em qualquer consulta;
- para escrita critica, avaliar idempotencia/outbox quando aplicavel;
- prefira evoluir compatibilidade sem quebrar rotas legadas abruptamente.
