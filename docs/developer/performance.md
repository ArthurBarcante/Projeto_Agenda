# Performance, Indices e Confiabilidade Estrutural

## 1. Objetivo de performance da Fase 1
Garantir baixa latencia e previsibilidade em cenarios de agenda corporativa com seguranca de consistencia.

Pilares:
- consultas com filtro de tenant + intervalo temporal;
- prevencao de corrida de escrita em conflitos;
- protecao contra duplicidade de requests;
- desacoplamento de integracoes externas via outbox.

## 2. Otimizacoes de banco (migracoes)
## 2.1 Indices de agenda
- indice composto em `appointments(company_id, start_time, end_time, status)`.
- indice em participantes `appointment_participants(user_id, appointment_id)`.

Impacto:
- acelera deteccao de sobreposicao por janela de tempo e usuario;
- reduz custo de joins na checagem de conflito.

## 2.2 Constraint de exclusao (PostgreSQL)
- `EXCLUDE USING GIST` com `company_id` e `tstzrange(start_time, end_time, '[)')`.

Impacto:
- adiciona protecao forte no banco contra sobreposicao por tenant;
- complementa validacao aplicacional e reduz risco de inconsistencias sob concorrencia.

## 2.3 Outras estruturas relevantes
- `idempotency_keys`: unique `(company_id, key)` para deduplicacao eficiente.
- `outbox_events`: indices por `company_id`, `status`, `processar_em` para polling escalavel.
- `webhook_subscriptions`: indice composto `(company_id, event_type, is_active)`.

## 3. Estrategias de runtime
## 3.1 Rate limit por tenant
- chave Redis por minuto: `rate_limit:<tenant>:<yyyymmddHHMM>`.
- protege API de rajadas e abuso.

## 3.2 Locking otimista/pragmatico
- consulta de conflito com `with_for_update()` para reduzir corrida entre transacoes concorrentes.

## 3.3 Idempotencia de escrita
- evita retrabalho e duplicidade em retentativas de cliente/rede.
- garante mesma resposta para mesma operacao logica.

## 3.4 Outbox para integracao
- evita bloquear request em dependencias externas (ex.: webhook lento).
- troca latencia de request por consistencia eventual controlada.

## 4. Testes estruturais relacionados a performance/confiabilidade
Suite de integracao cobre:
- `test_appointment_time_conflict_service.py`: conflitos de horario;
- `test_idempotency_appointments.py`: deduplicacao por chave;
- `test_rate_limit.py`: throttling por tenant;
- `test_outbox_events.py`: ciclo de vida de eventos outbox;
- `test_tenant_scope_enforcement.py`: enforce de escopo tenant em queries;
- `test_permissions.py`: gate de autorizacao em endpoint critico.

## 5. Metricas recomendadas (operacao)
Mesmo que ainda nao estejam instrumentadas no codigo, este conjunto e recomendado para as proximas fases:
- p50/p95/p99 de latencia por endpoint;
- taxa de conflito de agenda por tenant;
- taxa de 429 por tenant;
- taxa de hit de idempotencia;
- backlog de outbox pendente e tempo medio ate processamento;
- taxa de falha de webhook e tentativas medias por evento.

## 6. Evolucao de performance por fase
## Fase 2 (engajamento)
- agregacoes de XP/metas podem exigir tabelas de fatos e snapshots periodicos.
- considerar cache de dashboard por tenant+periodo.

## Fase 3 (personalizacao)
- feature unlock por nivel pode aumentar cardinalidade de regras;
- sugerido materializar permissoes efetivas por perfil para leitura rapida.

## Fase 4 (inteligencia adaptativa)
- analises comportamentais tendem a ser custosas;
- mover processamento para jobs assicronos e manter API de leitura com dados precomputados.

## 7. Riscos observados no estado atual
- migracoes com sinais de duplicidade podem impactar manutencao e reproducibilidade se nao revisadas.
- nomenclatura mista de campos/erros dificulta observabilidade e padronizacao de metricas.
- recomendavel consolidar padrao de mensagens/codigos antes da expansao das fases 2-4.
