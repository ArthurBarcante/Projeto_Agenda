# 🧭 Estrutura de documentação e arquitetura

Este projeto adota dois níveis de documentação:

## Beginner

A pasta beginner reúne conteúdo simples, com linguagem não técnica, para apresentar:

- o que é o projeto
- o que ele faz
- qual problema ele resolve

Esse nível é ideal para apresentação, portfólio e leitura inicial.

---

## Developer

A pasta developer reúne a visão técnica do sistema, incluindo:

- arquitetura
- organização de pastas
- módulos do backend
- estrutura do frontend
- setup e manutenção

Esse nível é ideal para quem vai estudar, manter ou evoluir o código.

---

## 📁 Estrutura principal do projeto

- back/app/core: autenticação, segurança e configuração interna
- back/app/database: conexão, sessão e base ORM
- back/app/modules: módulos de domínio como auth, users, tasks, events, progress e badges
- front/pages: telas da aplicação com lógica, marcação e estilos
- front/api: comunicação entre interface e backend
- front/components: elementos reutilizáveis da interface
- front/utils: helpers de autenticação, sessão, DOM e formatação
- docs: documentação para iniciantes e desenvolvedores

---

## Padrão mental recomendado

Ao estudar o projeto:

1. comece por beginner para entender a proposta
2. avance para developer para entender a arquitetura
3. consulte os módulos específicos antes de alterar código