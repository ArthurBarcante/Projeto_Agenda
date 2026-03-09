# Setup de Ambiente (Backend + Frontend)

## 1. Requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Git

## 2. Variaveis de ambiente
Baseie-se em `.env.example`:

```env
DATABASE_URL=postgresql+psycopg://aigenda:aigenda@localhost:5432/aigenda
SECRET_KEY=change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development
REDIS_URL=redis://localhost:6379/0
RATE_LIMIT_REQUESTS_PER_MINUTE=100
```

Passos:
1. Copie `cp .env.example .env`.
2. Ajuste credenciais locais de banco, segredo JWT e Redis.

## 3. Setup do backend
No diretorio raiz `aigenda/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic -c alembic.ini upgrade head
uvicorn backend.main:app --reload
```

API local: `http://127.0.0.1:8000`

## 4. Setup do frontend
Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend local: `http://localhost:3000`

## 5. Execucao de testes
No backend:

```bash
source .venv/bin/activate
pytest
```

Observacao:
- `pyproject.toml` aponta testes para `backend/tests`.
- Ha testes unitarios e de integracao que validam regras centrais da Fase 1.

## 6. Bootstrap de dados (sugestao para estudo)
Para estudos locais, prepare:
1. uma `company` (tenant);
2. usuarios da mesma empresa;
3. papeis/permissoes basicas (ex.: `agenda.criar`);
4. login para obter JWT.

## 7. Erros comuns de ambiente
- `Tenant context is required`: request sem tenant no contexto (token ausente/invalido ou query fora do fluxo esperado).
- `429 RATE_LIMIT_EXCEEDED`: limite por minuto do tenant excedido.
- `401 Invalid token`: token expirado, assinatura invalida ou payload incompleto.
- `409 Idempotency-Key ... payload diferente`: mesma chave reaproveitada com request body diferente.

## 8. Configuracoes importantes para performance local
- Use Postgres real para validar constraints de intervalo/indices (SQLite nao reflete todos os comportamentos).
- Mantenha Redis ativo para testar middleware de rate limit.
- Em cenarios de carga, reduza logs de debug para evitar ruido de I/O.

## 9. Roadmap de setup por fase
- Fase 1: setup atual ja cobre tudo.
- Fase 2: adicionar possivel storage de metricas/XP e seeds de metas.
- Fase 3: adicionar configuracao de feature flags por nivel.
- Fase 4: adicionar jobs de analise comportamental e pipelines de recomendacao.
