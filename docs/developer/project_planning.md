# Project Planning

O AIgenda esta organizado como um projeto em evolucao incremental.

A ideia nao e construir tudo de uma vez, mas consolidar uma base confiavel e depois expandir funcionalidades com seguranca.

## Objetivo atual do projeto

O objetivo imediato e estruturar uma plataforma de agenda corporativa com autenticacao, separacao por empresa e organizacao clara entre backend, frontend e testes.

No estado atual do repositorio, a prioridade visivel foi consolidar a fundacao tecnica do sistema.

## Fases de desenvolvimento

Uma leitura coerente do projeto indica duas frentes principais.

### Fase 1: base operacional

Foco em:

- autenticacao;
- usuarios;
- compromissos;
- infraestrutura de banco;
- estrutura de frontend;
- organizacao inicial de testes.

Essa fase cria a espinha dorsal do sistema.

### Fase 2: amadurecimento funcional

Foco em:

- ampliar regras de negocio dos compromissos;
- fortalecer fluxo autenticado;
- melhorar experiencia de uso no frontend;
- aumentar cobertura de testes;
- consolidar integracao backend e frontend.

## Metas tecnicas de curto prazo

- transformar placeholders em fluxos completos;
- expandir implementacao de routers, services e repositories;
- conectar o frontend a respostas reais da API;
- aumentar profundidade dos testes;
- estabilizar o contrato entre tela e backend.

## Metas tecnicas de medio prazo

- amadurecer autorizacao e validacoes;
- ampliar observabilidade e tratamento de erro;
- fortalecer migracoes e ciclo de banco;
- melhorar experiencia de contribuicao para novos desenvolvedores.

## Organizacao do trabalho

O formato do repositorio favorece contribuicoes por modulo.

Uma contribuicao bem organizada normalmente segue esta ordem:

1. identificar a feature ou camada afetada;
2. ajustar backend ou frontend no modulo correto;
3. atualizar ou criar testes correspondentes;
4. revisar a documentacao impactada.

## Como contribuir sem perder consistencia

Ao evoluir o projeto, vale seguir algumas regras praticas:

- manter separacao entre camadas;
- evitar colocar regra de negocio em pagina ou router;
- criar testes no agrupamento correto da feature;
- documentar decisoes estruturais relevantes.

## Leitura de planejamento a partir do estado atual

Este nao e um projeto finalizado.

Ele esta melhor descrito como uma base arquitetural em consolidacao, com estrutura suficiente para ensino, estudo e expansao gradual.

Por isso, o planejamento mais sensato e evoluir por pequenos incrementos coerentes, em vez de adicionar muitas features sem fechar os fluxos principais.