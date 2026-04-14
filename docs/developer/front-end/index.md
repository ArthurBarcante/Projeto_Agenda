# 🎨 Frontend Architecture

O frontend segue uma arquitetura modular baseada em páginas, rotas protegidas e componentes reutilizáveis.

A aplicação foi organizada para separar com clareza telas, comunicação com API, utilitários e elementos compartilhados da interface.

---

## 📁 Estrutura

- pages: telas da aplicação, como dashboard, agenda, create-item, perfil, login e cadastro
- components: elementos reutilizáveis, como sidebar e estilos globais
- api: comunicação com backend por domínio
- utils: autenticação, sessão, formatação e helpers locais
- router: regras de navegação e proteção da SPA

---

## 🔁 Fluxo de dados

O fluxo mais comum da interface segue este padrão:

1. a rota carrega a página correspondente
2. a página chama a camada de API
3. a API busca ou envia dados ao backend
4. os dados são guardados em estado local
5. a interface é renderizada novamente com feedback visual

---

## Exemplo prático na Agenda

Na agenda, a composição está dividida em responsabilidades menores:

- agenda.js: controla o estado principal da página
- filters.js: aplica busca, status e ordenação
- calendar.js: renderiza a visão de calendário
- eventCard.js: exibe compromissos em cards compactos
- taskCard.js: exibe tarefas com ações rápidas

Além disso, a rota create-item foi criada para isolar o fluxo de criação e melhorar a experiência do usuário.

---

## Entrada da aplicação

A entrada principal da SPA é front/index.html.

Esse arquivo carrega os estilos globais, inicializa o roteador e aplica o shell autenticado nas páginas internas do sistema.