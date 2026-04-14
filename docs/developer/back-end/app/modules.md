# 📦 Módulos do Backend

O backend segue uma arquitetura modular baseada em domínios.

Cada pasta dentro de back/app/modules representa uma responsabilidade de negócio e, quando aplicável, expõe a seguinte organização:

- model.py: entidade do banco
- schema.py: contratos de entrada e saída
- service.py: regras de negócio
- router.py: endpoints HTTP

---

## 🔐 Auth

Responsável por:

- registro de usuário
- login
- geração de JWT
- validação do usuário autenticado

Esse módulo centraliza a porta de entrada de autenticação da aplicação.

---

## 👤 Users

Responsável por:

- dados do usuário
- leitura do perfil autenticado
- atualização de perfil

É o módulo que sustenta a experiência da área de conta e identidade.

---

## 📌 Tasks

Responsável por:

- CRUD de tarefas
- marcação de conclusão
- integração com a camada de progresso

Esse módulo concentra grande parte da rotina operacional do usuário.

---

## 📅 Events

Responsável por:

- CRUD de eventos
- organização de compromissos
- suporte à agenda visual

---

## 📊 Progress

Responsável por:

- cálculo de progresso do usuário
- percentual de conclusão
- streak
- meta diária
- integração com badges e dashboard

---

## 🏆 Badges

Responsável por:

- definição de conquistas
- regras de desbloqueio
- representação visual de evolução

---

## Relação entre módulos

Em termos práticos:

- auth identifica o usuário
- users expõe os dados do perfil
- tasks e events alimentam a rotina
- progress resume desempenho
- badges enriquecem a gamificação