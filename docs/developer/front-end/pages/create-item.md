# ➕ Página Create Item

A página de criação foi adicionada para separar o fluxo de cadastro de tarefas e eventos da tela principal da agenda.

---

## Responsabilidades da página

- permitir escolher entre tarefa e evento
- exibir o formulário adequado para cada tipo
- validar campos obrigatórios antes do envio
- salvar o item no backend autenticado
- retornar o usuário para a agenda com feedback visual

---

## Estrutura técnica

A implementação usa:

- app.js: seleção de tipo, submissão e retorno para a agenda
- style.css: layout do fluxo guiado e responsividade
- render.html: ponto de montagem da página

---

## Fluxo resumido

1. o usuário escolhe se deseja criar uma tarefa ou um evento
2. a página monta o formulário correspondente
3. o envio chama a API correta
4. após sucesso, a agenda recebe uma mensagem de confirmação