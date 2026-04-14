# 👤 Página Profile

A página de perfil reúne identidade do usuário, resumo de atividade, conquistas e atualização de dados pessoais.

---

## Responsabilidades da página

- carregar o perfil do usuário autenticado
- exibir estatísticas resumidas de progresso e streak
- apresentar as abas Dados, Progresso e Conquistas
- permitir edição de dados pessoais
- validar campos antes do envio
- mostrar feedback visual de carregamento, erro e sucesso

---

## Estrutura técnica

A implementação usa:

- app.js: controle de estado, renderização, troca de abas e eventos da tela
- style.css: estilos da experiência visual e animações entre painéis
- validation.mjs: regras puras de validação para nome, email, telefone e data

---

## Fluxo resumido

1. a página busca os dados do usuário e do progresso
2. armazena o retorno em estado local
3. renderiza a interface em abas animadas
4. valida os dados antes de salvar
5. atualiza a sessão local após sucesso
6. reflete conquistas e estatísticas da conta