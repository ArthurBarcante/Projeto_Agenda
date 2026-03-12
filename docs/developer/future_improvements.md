# Future Improvements

As melhorias futuras do AIgenda podem ser divididas entre consolidacao da base atual e expansao funcional.

## Melhorias de backend

- implementar endpoints completos para usuarios, autenticacao e compromissos;
- ampliar regras de negocio nos services;
- enriquecer repositories com consultas reais;
- adicionar tratamento de erro mais consistente;
- fortalecer o ciclo de migracoes e inicializacao do banco.

## Melhorias de frontend

- substituir telas placeholder por fluxos completos;
- criar formularios reais de login, perfil e compromissos;
- adicionar estados de carregamento, erro e sucesso;
- consolidar componentes compartilhados de interface;
- melhorar navegacao e experiencia da area autenticada.

## Melhorias de integracao

- alinhar contratos entre tipos do frontend e schemas do backend;
- ampliar uso de autenticacao real ponta a ponta;
- conectar listagem e criacao de compromissos com persistencia completa.

## Melhorias de testes

- sair de smoke tests para testes comportamentais mais profundos;
- cobrir fluxos completos de autenticacao;
- validar cenarios de erro e autorizacao;
- criar testes de integracao mais proximos do uso real;
- aumentar cobertura de frontend com interacao de tela.

## Melhorias arquiteturais

- reforcar a separacao entre camadas em todos os modulos;
- documentar convencoes de contribuicao junto com exemplos reais;
- revisar pontos do projeto herdados de estruturas antigas;
- eliminar residuos de organizacoes anteriores quando surgirem.

## Possiveis features futuras

- edicao completa de compromissos pela interface;
- gestao de participantes;
- dashboard mais informativo;
- filtros e busca de compromissos;
- historico de atividades;
- notificacoes e integracoes externas.

## Prioridade recomendada

Antes de adicionar muitas funcionalidades novas, o melhor retorno tecnico tende a vir de tres frentes:

1. fechar os fluxos principais;
2. aumentar cobertura de testes;
3. consolidar o contrato entre frontend e backend.