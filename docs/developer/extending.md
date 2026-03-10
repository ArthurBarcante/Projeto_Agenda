# Como Adicionar Novas Funcionalidades

## Roteiro sugerido

1. Defina o caso de uso e regras de negocio.
2. Modele schema de entrada/saida (`modules/<dominio>/schemas`).
3. Implemente service com regras e transacao.
4. Implemente repositorio para persistencia.
5. Exponha endpoint em `api/routers`.
6. Adicione migracao Alembic se houver mudanca de banco.
7. Adicione testes unit/integration/e2e.
8. Atualize a documentacao em `docs/beginner/` e `docs/developer/`.

## Exemplo de esqueleto

```python
# backend/app/modules/example/services/example_service.py
class ExampleService:
    def __init__(self, db):
        self.db = db

    def execute(self, data, current_user):
        # regra de negocio
        # persistencia
        # auditoria/outbox quando necessario
        return result
```

## Quando usar idempotencia

Use em operacoes de criacao/escrita sujeitas a retentativas de cliente/rede.

## Quando usar outbox

Use quando a operacao principal precisa publicar evento sem acoplar resposta HTTP a integracoes externas.

## Compatibilidade de API

- evite quebrar contratos ja publicados;
- mantenha aliases legados quando houver clientes antigos;
- documente claramente qualquer deprecacao.
