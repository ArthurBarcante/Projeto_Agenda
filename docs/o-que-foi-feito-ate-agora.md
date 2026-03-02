# O que foi feito até agora

Esta página registra o estado atual do projeto **AIgenda**.

- Repositório: https://github.com/ArthurBarcante/Projeto_Agenda
- Versão atual do projeto: **0.1**
- Tag de versão publicada: **v0.1**

## Publicação e versionamento

- Projeto publicado e sincronizado no GitHub (`main`).
- Tag anotada `v0.1` criada e enviada para o repositório remoto.
- `README.md` revisado para refletir a versão atual do projeto (`0.1`).

## Banco de dados e migrations

- Alembic configurado e funcionando.
- Migrations criadas:
  - `06b0bc232d22_create_companies_table` (tabela `companies`).
  - `3afa394c9de8_create_users_table` (tabela `users` + vínculo com `companies`).
  - `8f2c7a1b90d4_add_appointment_conflict_indexes` (índices para conflitos de agenda).
- Regras importantes de banco:
  - Unicidade de usuário por tenant (`company_id + email`).
  - Índice para busca/conflito em agendamentos (`company_id`, `starts_at`, `ends_at`, `status`).
  - Índice para participantes (`user_id`, `appointment_id`).

## Modelagem de domínio

- `Company` com plano (`FREE`, `PRO`, `ENTERPRISE`), status e relacionamento com usuários.
- `User` com UUIDv7, vínculo ao tenant (`company_id`) e autenticação por hash de senha.
- `Appointment` com:
  - status (`scheduled`, `cancelled`, `completed`);
  - validações de atualização/cancelamento;
  - relacionamento com criador e participantes;
  - escopo por tenant.
- `AppointmentParticipant` com chave composta e unicidade (`appointment_id`, `user_id`).

## Multi-tenant e segurança de dados

- Contexto de tenant implementado em `app/core/tenant.py`.
- Escopo por tenant aplicado automaticamente nas consultas para entidades tenant-scoped.
- Proteção contra vazamento de dados quando o tenant não está no contexto.
- `BaseRepository` com filtro de empresa aplicado desde a base.

## Autenticação e API

- Endpoint `POST /auth/login` implementado.
- Fluxo de login:
  - resolve empresa por `company_slug`;
  - valida usuário por `email + company_id`;
  - valida senha;
  - emite JWT com `sub`, `company_id`, `company_slug`.
- Endpoints de agenda implementados:
  - `POST /appointments` (criação);
  - `PUT /appointments/{appointment_id}` (edição);
  - `PATCH /appointments/{appointment_id}/cancel` (cancelamento).

## Regras de negócio já entregues

- Criação de compromisso com participantes (sem duplicar o criador como participante).
- Detecção de conflito de horário para criador e participantes.
- Bloqueio de edição/cancelamento para status inválidos.
- Apenas o criador pode editar/cancelar compromisso.
- Retorno `404` para acesso a compromisso fora do escopo do tenant.

## Testes existentes

- `tests/test_company_model.py`
- `tests/test_base_repository.py`
- `tests/test_tenant_scope_enforcement.py`
- `tests/test_appointment_model.py`
- `tests/test_appointment_time_conflict_service.py`
- `tests/test_appointment_cancel_service.py`

Os testes cobrem principalmente: regras de tenant, modelo de empresa, regras de agendamento (conflito/edição/cancelamento) e comportamento do serviço.

## Marco atual (v0.1)

- Base multi-tenant implementada.
- Autenticação por JWT implementada.
- Núcleo de agendamentos (criar, editar, cancelar) implementado com validações.
- Suite inicial de testes automatizados implementada.
- Código e documentação alinhados com a versão `0.1` no GitHub.

## Próximos passos sugeridos

- Adicionar paginação/filtros para listagem de compromissos.
- Expandir autorização por papéis (owner/admin/member).
- Cobrir autenticação e rotas com testes de integração ponta a ponta.
- Preparar release `0.2` com CRUD completo de usuários e empresas.
