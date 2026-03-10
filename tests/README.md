# Estrutura de testes automatizados

Esta pasta centraliza todos os testes automáticos do projeto.

## Classificacao por fase

### 1. FASE 1 - Organizacao Inteligente (concluida)

Cobre:
- cadastro de compromissos (titulo, inicio/fim, descricao, participantes)
- participantes multiplos
- prevencao automatica de conflito de horario
- controle de autoria
- maquina de estados de compromissos
- isolamento multi-tenant
- testes estruturais por nivel (unit, integration, e2e)
- indices de performance

Pastas:
- `tests/fase_1_organizacao_inteligente/unit`
- `tests/fase_1_organizacao_inteligente/integration`
- `tests/fase_1_organizacao_inteligente/e2e`

### 2. FASE 2 - Engajamento

Cobre:
- sistema de metas
- XP (experiencia)
- painel de desempenho
- metricas de consistencia

Pastas:
- `tests/fase_2_engajamento/unit`
- `tests/fase_2_engajamento/integration`
- `tests/fase_2_engajamento/e2e`

## Regra de organizacao

- Sempre criar novos testes dentro de `tests/`.
- Classificar primeiro por fase (`fase_1_...` ou `fase_2_...`).
- Dentro da fase, classificar por nivel: `unit`, `integration` ou `e2e`.
