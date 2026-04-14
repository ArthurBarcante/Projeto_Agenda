# ⚙️ Setup do Projeto

Este guia descreve o fluxo recomendado para preparar o AIGENDA em ambiente local.

---

## Requisitos

- Python 3.10 ou superior
- Git
- Node.js apenas se quiser usar o mock local ou recursos auxiliares do frontend

---

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Projeto_Agenda
```

---

## 2. Criar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install -r configs/requirements.txt
```

---

## 4. Configurar variáveis de ambiente

Use o arquivo base criado no projeto:

```bash
cp .env.example back/.env
```

Exemplo de conteúdo:

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=troque-esta-chave-no-seu-ambiente
APP_INIT_DB_ON_STARTUP=1
```

---

## 5. Rodar o backend

Na raiz do projeto:

```bash
.venv/bin/python -m uvicorn app.main:app --reload --app-dir back
```

URLs úteis:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

---

## 6. Rodar o frontend

Opção mais simples:

- abrir front/index.html com Live Server no VS Code

Ou usar um servidor estático local:

```bash
cd front
python3 -m http.server 5500
```

Depois acesse:

- http://127.0.0.1:5500

---

## 7. Mock local opcional

Se quiser testar o frontend com dados simulados:

```bash
npx json-server --watch back/mock/db.json --port 3002
```

---

## 8. Testes

### Backend

```bash
.venv/bin/pytest back/app/tests -q
```

### Frontend

```bash
node --test tests/front/profile.validation.test.mjs
```

---

## Observações de manutenção

- o backend lê a configuração a partir de back/.env
- é possível usar SQLite localmente para desenvolvimento rápido
- o frontend pode alternar entre modo real e mock conforme a configuração interna
