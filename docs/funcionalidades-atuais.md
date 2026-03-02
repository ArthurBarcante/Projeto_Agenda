# Funcionalidades Atuais (Implementadas)

Esta página destaca exclusivamente as funcionalidades já implementadas no **AIGENDA**.

## Fase 1 - Organização Inteligente (concluída)

## 1) Cadastro de compromissos

O usuário pode:

- criar compromisso;
- definir título, descrição, horário de início e término;
- informar participantes;
- atualizar compromisso (se for o criador);
- cancelar compromisso (se for o criador).

### Estados do compromisso

- `scheduled`
- `cancelled`
- `completed` (preparado para evolução futura)

### Regras de estado

- Apenas compromissos `scheduled` podem ser alterados.
- Apenas compromissos `scheduled` podem ser cancelados.
- Estados finais não são mutáveis.

## 2) Alocação automática e prevenção de conflito

Ao criar ou atualizar compromisso, o sistema valida disponibilidade de:

- criador;
- todos os participantes.

Regra de sobreposição aplicada:

`(start_a < end_b) AND (end_a > start_b)`

Se houver conflito, a operação é bloqueada com erro.

Garantia atual:

- nenhum usuário pode ter dois compromissos `scheduled` sobrepostos.

## 3) Regras de prevenção (implementadas)

- conflito verificado no create;
- conflito verificado no update;
- o próprio compromisso é ignorado no update;
- apenas compromissos `scheduled` entram na verificação;
- isolamento por tenant aplicado automaticamente.

## 4) Segurança e governança

### Multi-tenant

- dados isolados por empresa no nível da sessão ORM;
- filtros de empresa aplicados desde o repositório base;
- proteção contra acesso fora do tenant.

### Controle de auditoria

- apenas o criador pode editar ou cancelar compromisso.

### Máquina de estados

- estados finais não podem ser modificados.

## 5) Autenticação

- endpoint `POST /auth/login` implementado;
- login por `company_slug` + `email` + senha;
- emissão de JWT com `sub`, `company_id`, `company_slug`.

## 6) Banco e performance

- migration de `companies`;
- migration de `users`;
- migration com índices de conflito de agenda.

Índices principais:

- `appointments(company_id, starts_at, ends_at, status)`;
- `appointment_participants(user_id, appointment_id)`.

## 7) Testes automatizados

Cobertura atual inclui:

- modelo de empresa;
- regras de tenant;
- regras de agendamento (conflito/edição/cancelamento);
- comportamento de repositório e serviços.

Arquivos:

- `tests/test_company_model.py`
- `tests/test_base_repository.py`
- `tests/test_tenant_scope_enforcement.py`
- `tests/test_appointment_model.py`
- `tests/test_appointment_time_conflict_service.py`
- `tests/test_appointment_cancel_service.py`
