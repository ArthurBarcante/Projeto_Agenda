# Padroes de Codigo e Convencoes

## Estrutura de implementacao

Padrao predominante no backend:

`Router -> Dependency -> Service -> Repository -> ORM/DB`

Objetivo:

- manter regra de negocio fora de router;
- isolar persistencia em repositorios;
- facilitar testes por camada.

## Convencoes de nomes

- ha coexistencia pt/en por historico do projeto;
- campos HTTP privilegiam `snake_case`;
- alguns aliases legados sao mantidos para compatibilidade.

## Modelagem e persistencia

- IDs baseados em UUID;
- timestamps de auditoria (`created_at`, `updated_at`);
- entidades tenant-scoped usam `company_id`;
- repositorios da agenda exigem tenant no contexto.

## Dependencias FastAPI

Dependencias principais em `backend/app/dependencies/fastapi.py`:

- `get_current_user`;
- `get_current_company`;
- `require_permission(permission_code)`.

Exemplo de guarda de permissao:

```python
@router.post("/appointments")
async def create_appointment(
    current_user: User = Depends(require_permission("agenda.criar")),
):
    ...
```

## Tratamento de erro

Erros sao padronizados por handlers globais em `backend/app/core/errors/error_handlers.py`.

Formato esperado:

```json
{
  "erro": {
    "codigo": "...",
    "mensagem": "...",
    "timestamp": "..."
  }
}
```

## Regras para escrita critica

- considerar idempotencia para endpoints de criacao;
- registrar auditoria em alteracoes relevantes;
- publicar eventos via outbox quando houver integracao externa.

## Fronteira backend/frontend

Frontend usa cliente HTTP compartilhado em
`frontend/src/intelligent_organization/shared/api/httpClient.ts`.

Recomendacoes:

- centralizar novos endpoints em `shared/api/endpoints.ts`;
- manter tipos de payload/response em `features/*/types`.

## Guia rapido para nova feature

1. adicionar/ajustar schema;
2. implementar regra no service;
3. implementar acesso ao banco no repositorio;
4. expor endpoint no router;
5. cobrir com testes;
6. atualizar docs.
