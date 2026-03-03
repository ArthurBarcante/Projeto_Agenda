# Página de Testes

Esta página descreve os testes automatizados atuais e o objetivo de cada arquivo.

## Estrutura de testes

```text
tests/
├── test_company_model.py
├── test_base_repository.py
├── test_tenant_scope_enforcement.py
├── test_appointment_model.py
├── test_appointment_time_conflict_service.py
├── test_appointment_cancel_service.py
└── test_env.py
```

## O que cada teste valida

- `test_company_model.py`: valida regras básicas do modelo de empresa.
- `test_base_repository.py`: garante escopo correto do repositório base.
- `test_tenant_scope_enforcement.py`: valida isolamento multi-tenant em consultas.
- `test_appointment_model.py`: testa regras de estado do compromisso no modelo.
- `test_appointment_time_conflict_service.py`: verifica detecção de conflito de horário no serviço.
- `test_appointment_cancel_service.py`: valida permissões e fluxo de cancelamento.
- `test_env.py`: endpoint/utilitário simples para validação rápida de ambiente.

## Cobertura funcional atual (resumo)

- regras de domínio de agendamento;
- isolamento por empresa;
- permissões de alteração/cancelamento;
- integridade da máquina de estados.

## Execução dos testes

Com a virtualenv ativa:

```bash
pytest -q
```

Para executar um arquivo específico:

```bash
pytest -q tests/test_appointment_time_conflict_service.py
```
