# Documentacao para Desenvolvedores

Esta secao e voltada para quem vai implementar funcionalidades, revisar codigo, escrever testes ou estender o AIgenda. Os documentos detalham decisoes de arquitetura, padroes adotados, estrutura de modulos, fluxos internos e praticas de desenvolvimento do projeto.

---

## Documentos desta secao

| Documento | Descricao |
|-----------|-----------|
| [scope_project.md](scope_project.md) | Escopo atual do projeto: o que esta implementado e o que esta planejado |
| [architecture.md](architecture.md) | Arquitetura tecnica: multi-tenancy, outbox, RBAC e decisoes de design |
| [folder_structure.md](folder_structure.md) | Estrutura de pastas com responsabilidades detalhadas de cada camada |
| [modules.md](modules.md) | Modulos do backend e suas responsabilidades de dominio |
| [api.md](api.md) | Referencia dos endpoints, convencoes, autenticacao e exemplos de uso |
| [code.md](code.md) | Padroes de codigo, convencoes de nomenclatura e estrutura de implementacao |
| [setup.md](setup.md) | Setup completo do ambiente de desenvolvimento (backend, frontend, banco, Redis) |
| [workflow.md](workflow.md) | Fluxos internos: maquinas de estado, outbox, idempotencia e rate limiting |
| [testing.md](testing.md) | Estrategia de testes, organizacao da suite e como rodar cada nivel |
| [dependencies.md](dependencies.md) | Bibliotecas e dependencias do backend e frontend com justificativas |
| [performance.md](performance.md) | Recursos de performance e confiabilidade: locks, indices, filas |
| [extending.md](extending.md) | Como adicionar novos modulos, rotas e funcionalidades seguindo os padroes do projeto |
| [contributing.md](contributing.md) | Fluxo de contribuicao, branches, Pull Requests e checklist de qualidade |

---

## Ordem recomendada de leitura

Para quem esta entrando no projeto como desenvolvedor:

1. [scope_project.md](scope_project.md) — entenda o que o sistema cobre hoje.
2. [architecture.md](architecture.md) — compreenda as decisoes tecnicas fundamentais.
3. [folder_structure.md](folder_structure.md) — oriente-se na codebase.
4. [modules.md](modules.md) — entenda o dominio de negocio por modulo.
5. [setup.md](setup.md) — configure seu ambiente local completo.
6. [code.md](code.md) — leia os padroes antes de escrever codigo.
7. [testing.md](testing.md) — saiba como validar suas implementacoes.
8. [contributing.md](contributing.md) — siga o fluxo correto para abrir um PR.

---

> Para uma visao acessivel do sistema sem foco tecnico, acesse a secao [Beginner](../beginner/README.md).
