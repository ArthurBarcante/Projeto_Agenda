# Project Structure

O projeto esta dividido em quatro areas principais: backend, frontend, testes e documentacao.

Essa divisao facilita manutencao, estudo e evolucao independente de cada parte.

## Visao geral

- `backend/`: API, regras de negocio e acesso ao banco.
- `frontend/`: interface web construida com Next.js, React e TypeScript.
- `tests/`: testes automatizados separados por contexto funcional.
- `docs/`: material de apoio para iniciantes e desenvolvedores.

## Como as partes se relacionam

O frontend envia requisicoes HTTP para o backend.

O backend interpreta essas requisicoes, aplica regras de negocio e usa a camada de banco para ler ou gravar dados.

Os testes verificam se essas partes continuam funcionando conforme o esperado.

## Estrutura principal do backend

- `backend/app/main.py`: ponto de entrada da aplicacao FastAPI.
- `backend/app/auth/`: autenticacao e seguranca.
- `backend/app/users/`: dominio de usuarios.
- `backend/app/appointments/`: dominio de compromissos.

Nos textos desta documentacao, o termo funcional `compromissos` corresponde ao modulo tecnico `appointments`.
- `backend/app/utils/`: funcoes auxiliares.
- `backend/db/`: engine, sessao, base ORM e migracoes Alembic.

## Estrutura principal do frontend

- `frontend/src/app/`: rotas e layouts do App Router.
- `frontend/src/features/`: organizacao por dominio funcional.
- `frontend/src/components/`: componentes reutilizaveis.
- `frontend/src/hooks/`: hooks compartilhados.
- `frontend/src/services/`: comunicacao HTTP comum.
- `frontend/src/utils/`: funcoes utilitarias.

## Estrutura principal de testes

- `tests/backend/`: testes do backend por modulo.
- `tests/frontend/`: testes do frontend por area funcional.
- `tests/config/`: configuracoes compartilhadas de pytest e Vitest.

## Leitura recomendada da estrutura

Para entender o sistema do inicio ao fim, vale seguir esta ordem:

1. `backend/app/main.py`
2. modulos de `backend/app/`
3. `backend/db/`
4. `frontend/src/app/`
5. `frontend/src/features/`
6. `tests/`