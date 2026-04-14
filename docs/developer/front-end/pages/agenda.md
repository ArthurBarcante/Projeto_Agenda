# 📆 Página Agenda

A página de agenda concentra a experiência operacional principal do sistema.

Ela reúne tarefas e eventos em uma única visão, com foco em organização diária, clareza visual e interação rápida.

---

## Responsabilidades da página

- listar tarefas e eventos do usuário autenticado
- alternar entre as abas de calendário e compromissos
- aplicar busca, status e ordenação
- abrir o fluxo dedicado de criação de itens
- editar, concluir e excluir registros já existentes
- manter a UI sincronizada com a API

---

## Experiência atual

A experiência foi refinada para funcionar em duas áreas:

- Calendário: visão mensal simplificada com os itens distribuídos por dia
- Compromissos: lista de tarefas e eventos em cards compactos com ações rápidas

A criação de novos itens foi movida para uma rota própria, melhorando a navegação e reduzindo a poluição visual da agenda.

---

## Módulos internos

- agenda.js: orquestra estado, carregamento, abas e feedback visual
- filters.js: aplica busca, filtros e ordenação
- calendar.js: monta a visualização do calendário
- eventCard.js: renderiza cards de eventos
- taskCard.js: renderiza cards de tarefas

---

## Fluxo resumido

1. a página busca dados nas APIs de tarefas e eventos
2. os dados são normalizados em memória
3. os filtros refinam o que deve ser exibido
4. a interface renderiza calendário, lista e estados visuais
5. ações de edição e exclusão sincronizam novamente a tela