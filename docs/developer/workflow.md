# Workflows Internos, Estados e Interacoes

## 1. Maquina de estados de appointment

```text
scheduled ----cancel()----> cancelled
scheduled ----complete()---> completed (conceitual/planejado)

Regras:
- update permitido somente em scheduled
- cancel permitido somente em scheduled
- cancel permitido somente para o creator
```

## 2. Fluxo de login
1. Cliente envia `company_identifier`, `email`, `senha`.
2. API localiza empresa por slug.
3. API valida usuario no tenant da empresa.
4. API valida hash de senha.
5. API emite JWT com `sub` e `company_id`.
6. Requests seguintes usam `Authorization: Bearer <token>`.

## 3. Fluxo de criacao de compromisso (principal)

```text
Client
  -> POST /appointments (+ token + opcional Idempotency-Key)
      -> TenantContextMiddleware (set tenant)
      -> RateLimitMiddleware (incr Redis por tenant/min)
      -> require_permission("agenda.criar")
      -> IdempotencyService.verificar_idempotencia()
           -> se hit: retorna resposta antiga
      -> AppointmentService.create_appointment()
           -> valida conflito de horario
           -> cria appointment + participantes
           -> registra audit log
           -> registra outbox event
           -> commit
      -> IdempotencyService.registrar_resposta()
      -> 201 Created
```

## 4. Fluxo de atualizacao
1. `PUT /appointments/{id}`.
2. Carrega appointment no tenant corrente.
3. Valida autoria (creator).
4. Valida estado (`scheduled`).
5. Se horario alterou, revalida conflitos.
6. Persiste alteracoes e grava auditoria.

## 5. Fluxo de cancelamento
1. `PATCH /appointments/{id}/cancel`.
2. Carrega appointment no tenant.
3. Executa `appointment.cancel(current_user)`.
4. Se nao for autor -> 403.
5. Se estado invalido -> 400.
6. Persiste status cancelado + auditoria.

## 6. Fluxo de idempotencia
- Sem header `Idempotency-Key`: processamento normal.
- Com header:
  - chave nao vista: processa e salva resposta;
  - chave+hash iguais: retorna resposta anterior;
  - chave igual e hash diferente: retorna 409.

## 7. Fluxo de eventos e webhooks
1. Evento e gravado em `outbox_events` na transacao do caso de uso.
2. Worker busca pendentes por lote.
3. Worker marca `processing`, faz dispatch no `EventBus`.
4. Handler de notificacao dispara webhooks assinados (`X-AIGENDA-SIGNATURE`).
5. Em sucesso: status `done`; em falha: incremento de tentativa + reprogramacao.

## 8. Triggers tecnicas
- Trigger de tenant: middleware por request autenticada.
- Trigger de rate limit: middleware por tenant/minuto.
- Trigger de conflito: validacao de service + constraints/indices de banco.
- Trigger de auditoria: operacoes de create/update/cancel.
- Trigger de integracao: gravacao de evento outbox.

## 9. Fluxos por fase do produto
## Fase 1 (concluida)
- foco em robustez transacional e governanca.
- fluxo centrado em agenda, permissao, isolamento e confiabilidade.

## Fase 2 (engajamento)
Fluxo esperado:
1. usuario conclui rotina/meta;
2. evento de progresso gera XP;
3. dashboard agrega consistencia por periodo.

## Fase 3 (evolucao/personalizacao)
Fluxo esperado:
1. XP acumulado muda nivel;
2. nivel habilita recursos e personalizacao de interface;
3. backend entrega matriz de recursos por maturidade.

## Fase 4 (inteligencia adaptativa)
Fluxo esperado:
1. historico alimenta indice comportamental;
2. motor ajusta metas automaticamente;
3. sistema sugere reorganizacao da agenda;
4. usuario aceita/rejeita sugestoes, retroalimentando o modelo.

## 10. Ponto de estudo: consistencia eventual
O design separa escrita transacional de entrega externa. Isso evita acoplamento forte entre API e integracoes, mas exige:
- monitoramento do backlog do outbox;
- politicas claras de retentativa;
- idempotencia tambem no consumidor externo, quando possivel.
