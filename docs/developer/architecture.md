# Arquitetura Tecnica (Developer)

## 1. Objetivo do sistema
AIgenda e uma plataforma de agendamento para ambientes corporativos multi-tenant. O foco da arquitetura e garantir:
- isolamento de dados por empresa (tenant);
- consistencia de agenda (sem conflitos de horario);
- confiabilidade de escrita (idempotencia + outbox);
- seguranca por autenticacao JWT e autorizacao RBAC;
- observabilidade minima com trilha de auditoria.

## 2. Macrovisao em camadas

```text
+-----------------------------------------------------------+
|                       Cliente HTTP                        |
|        (Frontend Next.js, integracoes externas)           |
+------------------------------+----------------------------+
                               |
                               v
+-----------------------------------------------------------+
|                     FastAPI (API Layer)                   |
| Routers: /auth, /appointments, /me                        |
+------------------------------+----------------------------+
                               |
                               v
+-----------------------------------------------------------+
|               Middlewares e Cross-cutting                 |
| TenantContextMiddleware | RateLimitMiddleware             |
+------------------------------+----------------------------+
                               |
                               v
+-----------------------------------------------------------+
|                     Application Services                  |
| AppointmentService | IdempotencyService | PermissionService|
| AuditService | OutboxService | WebhookService             |
+------------------------------+----------------------------+
                               |
                               v
+-----------------------------------------------------------+
|                   Repositories / ORM                      |
| SQLAlchemy repos + models tenant-scoped                   |
+------------------------------+----------------------------+
                               |
                               v
+------------------------+   +------------------------------+
| PostgreSQL             |   | Redis                        |
| dados + constraints    |   | rate limit por minuto        |
+------------------------+   +------------------------------+
```

## 3. Componentes principais
- API Layer (`backend/app/api/routers/`): define contratos HTTP, valida payloads e injeta dependencias.
- Service Layer (`backend/app/modules/*/services/`): regras de negocio, orquestracao de transacoes e publicacao de eventos.
- Repository Layer (`backend/app/modules/*/repositories/`): persistencia e consultas otimizadas.
- Core Layer (`backend/app/core/`): infraestrutura transversal (DB session, tenant context, seguranca, erros, eventos).
- Middleware Layer (`backend/app/middleware/`): aplicacao de politicas globais por request.

## 4. Padroes arquiteturais usados
- Arquitetura em camadas (Router -> Service -> Repository -> DB).
- Multi-tenancy por contexto de execucao (`ContextVar`) + filtros ORM.
- RBAC (roles, permissions, associacao user_role e role_permission).
- Idempotencia para operacoes de escrita com chave por tenant.
- Transactional outbox para integracao assicrona e entrega eventual.
- Event bus interno com registro explicito de handlers.

## 5. Multi-tenant: isolamento de dados
### 5.1 Estrategia
- `TenantContextMiddleware` extrai tenant do JWT e seta no contexto.
- Entidades tenant-scoped usam `company_id`.
- Queries de entidades tenant-scoped exigem tenant no contexto; sem isso, erro de execucao.

### 5.2 Beneficio
- reduz risco de vazamento cross-tenant;
- centraliza enforcement de escopo sem depender de cada endpoint lembrar filtro manual.

## 6. Confiabilidade de escrita
### 6.1 Idempotencia
- Header `Idempotency-Key` e opcional em `POST /appointments`.
- Hash canonico do request body evita reuso da mesma chave com payload diferente.
- Resposta original e armazenada e reaproveitada em repeticao legitima.

### 6.2 Outbox
- Evento de dominio e persistido em tabela `outbox_events` na mesma transacao da operacao principal.
- Worker processa pendentes, faz dispatch no event bus e controla retentativas.

## 7. Fluxo de eventos (conceitual)

```text
create_appointment()
  -> persiste appointment
  -> registra audit_log
  -> registra outbox_event(APPOINTMENT_CREATED)
  -> commit

outbox_worker
  -> busca eventos pendentes
  -> marca processing
  -> event_bus.dispatch(event)
       -> schedule handlers
       -> notifications/webhook handlers
  -> marca done
```

## 8. Fases do projeto na arquitetura
## Fase 1 (concluida)
- agenda com estados, conflitos, autoria, multi-participantes;
- multi-tenant e seguranca (JWT + RBAC);
- idempotencia, outbox, auditoria, rate limit;
- base de testes unit/integration/e2e.

## Fase 2 (engajamento - planejada)
- adicionar modulo de metas e XP;
- eventos de progresso para dashboard;
- metricas de consistencia com agregacoes por periodo.

## Fase 3 (evolucao/personalizacao - planejada)
- niveis e liberacao progressiva de recursos;
- backend passa a servir regras de feature unlock por maturidade.

## Fase 4 (inteligencia adaptativa - planejada)
- indice comportamental;
- ajuste automatico de metas;
- sugestoes de reorganizacao com base em historico.

## 9. Decisoes de design relevantes
- DB-first para integridade: constraint de exclusao para intervalo de tempo + indices.
- Defesa em profundidade para conflito: checagem aplicacional + protecao no banco.
- Compatibilidade de rotas legadas (`/authentication`) para migracao controlada de clientes.
- Modelo de erro padronizado (`erro.codigo`, `erro.mensagem`, `erro.timestamp`).

## 10. Riscos tecnicos observados
- Alguns pontos do codigo apresentam nomenclatura mista (pt/en) e alias redundantes.
- Ha sinais de duplicacao em migracoes e servicos que merecem refino para reduzir risco de manutencao.
- Para evolucao das fases 2-4, sera importante formalizar contratos de eventos e metricas desde o inicio.
