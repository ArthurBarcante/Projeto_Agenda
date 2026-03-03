# Roadmap de melhorias da Fase 1 (curto prazo)

Esta página organiza melhorias recomendadas para consolidar a **Fase 1 - Organização Inteligente** do **AIGENDA**.

## Objetivo

Elevar robustez, cobertura e governança da Fase 1 sem ampliar escopo funcional para fases futuras.

## Critérios de priorização

- **Impacto**: efeito em confiabilidade, segurança e manutenção.
- **Esforço**: custo técnico estimado para implementação.
- **Prioridade**: ordem sugerida de execução (`P0`, `P1`, `P2`).

## Backlog priorizado (impacto x esforço)

## P0 - alta prioridade

### 1) Testes de autenticação (`/auth/login`)

- **Impacto:** alto
- **Esforço:** baixo
- **Prioridade:** `P0`
- **Escopo:** cobrir login válido, credenciais inválidas, `company_slug` inválido, token inválido/expirado.
- **Resultado esperado:** fechar lacuna de cobertura na camada de autenticação.

### 2) Restringir alteração direta de `status` no update

- **Impacto:** alto
- **Esforço:** baixo
- **Prioridade:** `P0`
- **Escopo:** impedir transição de estado fora de fluxos explícitos (ex.: endpoint de cancelamento).
- **Resultado esperado:** reforço da máquina de estados e redução de inconsistências.

### 3) Regra temporal explícita (`starts_at < ends_at`)

- **Impacto:** alto
- **Esforço:** baixo
- **Prioridade:** `P0`
- **Escopo:** validar no schema/serviço com mensagem de erro padronizada.
- **Resultado esperado:** bloquear entradas inválidas antes da persistência.

## P1 - prioridade média

### 4) Testes de integração dos endpoints de agenda

- **Impacto:** alto
- **Esforço:** médio
- **Prioridade:** `P1`
- **Escopo:** validar `POST/PUT/PATCH` com banco de teste, autenticação e tenant.
- **Resultado esperado:** maior confiança no fluxo ponta a ponta.

### 5) Padronização de erros de domínio/API

- **Impacto:** médio
- **Esforço:** baixo
- **Prioridade:** `P1`
- **Escopo:** unificar estrutura de erro para conflito, permissão e estado inválido.
- **Resultado esperado:** previsibilidade para clientes e melhor suporte operacional.

### 6) Política de timezone (UTC) documentada e testada

- **Impacto:** médio
- **Esforço:** baixo
- **Prioridade:** `P1`
- **Escopo:** formalizar persistência em UTC e cobrir cenários de fronteira.
- **Resultado esperado:** redução de risco de inconsistência temporal.

## P2 - melhoria evolutiva

### 7) Observabilidade mínima para operações críticas

- **Impacto:** médio
- **Esforço:** médio
- **Prioridade:** `P2`
- **Escopo:** logs estruturados em create/update/cancel/login com `company_id` e `user_id`.
- **Resultado esperado:** melhor rastreabilidade e diagnóstico.

### 8) Matriz de rastreabilidade (requisito -> código -> teste)

- **Impacto:** médio
- **Esforço:** baixo
- **Prioridade:** `P2`
- **Escopo:** mapear cada requisito da Fase 1 para implementação e teste correspondente.
- **Resultado esperado:** auditoria de conformidade mais rápida.

## Sequência sugerida de execução

- **Sprint 1 (estabilização):** itens `1`, `2`, `3`.
- **Sprint 2 (confiabilidade):** itens `4`, `5`, `6`.
- **Sprint 3 (governança):** itens `7`, `8`.

## Resultado esperado ao final

- Fase 1 com maior robustez técnica;
- cobertura de testes mais homogênea;
- melhor previsibilidade operacional e manutenção futura.
