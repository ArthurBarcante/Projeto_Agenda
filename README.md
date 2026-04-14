# 📅 AIGENDA

Sistema de agenda inteligente para gerenciamento de tarefas, eventos e progresso do usuário.

O projeto combina um backend em FastAPI com um frontend em JavaScript Vanilla, oferecendo uma experiência simples de usar e fácil de evoluir para estudos, portfólio e desenvolvimento incremental.

---

## 🚀 Funcionalidades

- 🔐 Autenticação com JWT
- 👤 Cadastro, login e identificação do usuário autenticado
- 📌 CRUD completo de tarefas
- 📅 CRUD completo de eventos
- 📊 Sistema de progresso com meta diária, percentual e streak
- 🏅 Área de conquistas, badges e evolução do usuário
- ✏️ Perfil editável com feedback de validação
- 📆 Agenda com abas de calendário e compromissos
- ➕ Fluxo dedicado para criação de tarefas e eventos

---

## 🧠 Tecnologias

### Backend
- FastAPI
- SQLAlchemy
- JWT Authentication
- Pytest
- SQLite ou PostgreSQL

### Frontend
- JavaScript Vanilla modular
- HTML5
- CSS3

---

## 📁 Estrutura do Projeto

```bash
Projeto_Agenda/
├── back/
│   └── app/
│       ├── core/
│       ├── database/
│       ├── modules/
│       │   ├── auth/
│       │   ├── users/
│       │   ├── tasks/
│       │   ├── events/
│       │   ├── progress/
│       │   └── badges/
│       └── tests/
├── front/
│   ├── api/
│   ├── components/
│   ├── pages/
│   ├── router/
│   └── utils/
├── docs/
├── configs/
└── Makefile
```

---

## ⚙️ Como o projeto funciona

- O backend expõe uma API REST para autenticação, tarefas, eventos e progresso.
- O frontend consome essa API e organiza a navegação em páginas modulares.
- O projeto pode trabalhar com API real ou com mock local, dependendo da configuração do frontend.
- As variáveis de ambiente controlam banco de dados, chave JWT e inicialização automática das tabelas.

---

## ▶️ Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Projeto_Agenda
```

### 2. Criar e ativar o ambiente Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r configs/requirements.txt
```

### 3. Configurar o ambiente

Copie o arquivo de exemplo para o backend:

```bash
cp .env.example back/.env
```

Exemplo das variáveis principais:

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=troque-esta-chave-no-seu-ambiente
APP_INIT_DB_ON_STARTUP=1
```

### 4. Subir o backend

```bash
.venv/bin/python -m uvicorn app.main:app --reload --app-dir back
```

A API ficará disponível em:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

### 5. Abrir o frontend

Você pode abrir o arquivo `front/index.html` com a extensão Live Server no VS Code ou servir a pasta `front/` com um servidor estático local.

Exemplo com Python:

```bash
cd front
python3 -m http.server 5500
```

Depois, acesse no navegador:
- http://127.0.0.1:5500

### 6. Modo desenvolvimento rápido

Se quiser subir o ambiente auxiliar de desenvolvimento com backend + mock local:

```bash
make dev
```

---

## 🧪 Testes

### Backend

```bash
.venv/bin/pytest back/app/tests -q
```

### Frontend

```bash
node --test front/tests/front/profile.validation.test.mjs
```

---

## 🛣️ Roadmap

- Implementar notificações e lembretes para tarefas e eventos
- Adicionar recorrência de tarefas e compromissos
- Evoluir o dashboard com histórico, tendências e métricas semanais
- Expandir a gamificação com mais conquistas e missões
- Criar testes end-to-end para os principais fluxos do frontend
- Estruturar CI/CD e deploy em nuvem com ambiente de produção

---

## 👨‍💻 Autor

Arthur Barçante

