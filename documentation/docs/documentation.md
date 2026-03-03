# Página de Documentation

Esta página resume o estado da documentação do projeto e o direcionamento evolutivo.

## Fase atual do projeto

**Fase 1 - Organização Inteligente (implementada)**

Resumo breve:

- criação, edição e cancelamento de compromissos;
- validação automática de conflitos de horário;
- isolamento por empresa (multi-tenant);
- autenticação com JWT;
- regras de auditoria (apenas criador altera/cancela).

## Planejamento de funcionalidades futuras

### Fase 2 - Engajamento

- **Sistema de metas:** organização por objetivos.
- **XP:** feedback de progresso e consistência.
- **Painel de desempenho:** visão consolidada de execução.
- **Métricas de consistência:** acompanhamento de disciplina ao longo do tempo.

### Fase 3 - Evolução e personalização

- **Sistema de níveis:** progressão de maturidade.
- **Personalização progressiva:** UI e experiência adaptadas ao uso.
- **Expansão de recursos:** funcionalidades liberadas conforme evolução.

### Fase 4 - Inteligência adaptativa

- **Índice comportamental:** leitura de regularidade do uso.
- **Ajuste automático de metas:** metas recalibradas conforme comportamento.
- **Sugestões de reorganização:** recomendações de agenda.
- **Análise de regularidade:** visão contínua de padrão de execução.

## Roadmap da Fase 1 (resumo)

- **P0:** fortalecer autenticação, regras de estado e validação temporal.
- **P1:** ampliar testes de integração, padronizar erros e consolidar política de timezone.
- **P2:** melhorar observabilidade e rastreabilidade requisito-código-teste.

## Diretriz de arquitetura (Fase 5)

- **Frontend (feature-based):**
	- `src/app`: apenas roteamento e composição de páginas.
	- `src/features`: regras por domínio (`autenticacao`, `compromissos`, `usuarios`).
	- `src/shared/api`: cliente HTTP e endpoints centralizados.
	- `src/shared`: componentes base, utilitários e tipos reutilizáveis.

- **Backend (modularização progressiva):**
	- `app/api`: camada HTTP.
	- `app/modules/compromissos/services`: serviço de domínio em português.
	- `app/modules/schedule/services`: mantido como compatibilidade para transição.
	- `app/models` e `app/schemas`: contratos e persistência.

- **Princípios de evolução contínua:**
	- Nova regra de negócio nasce no módulo de domínio (`modules/<dominio>/services`).
	- Camada de API não implementa regra de negócio; apenas orquestra dependências e contratos.
	- Serviços de frontend devem consumir a API via `shared/api/httpClient.ts`.

## Referências rápidas

- [Página inicial](../../README.md)
- [Página do backend](backend.md)
- [Página do frontend](frontend.md)
- [Página de config](config.md)
- [Página de virtualenv](virtualenv.md)
- [Página de testes](tests.md)
