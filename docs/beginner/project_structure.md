# Estrutura do Projeto (Explicacao Simples)

## Visao geral

Pense no projeto como uma empresa com setores:

- `backend/`: setor que decide as regras do negocio.
- `frontend/`: setor que mostra as telas para o usuario.
- `tests/`: setor que confere se tudo funciona.
- `docs/`: setor de manuais e guias.

## Pastas principais

## `backend/`

Aqui mora o "cerebro" do sistema.

- `main.py`: arquivo que liga a API.
- `app/api/routers/`: portas de entrada das funcoes (login, agenda, etc.).
- `app/modules/`: regras por assunto (agenda, permissoes, notificacoes).
- `app/middleware/`: validacoes globais em toda requisicao.
- `app/core/`: configuracoes de seguranca, banco, erros e infraestrutura.
- `alembic/`: controle de mudancas do banco de dados.

## `frontend/`

Aqui mora a interface visual.

- `src/intelligent_organization/`: telas principais de login, dashboard, perfil e compromissos.
- `src/engagement/`: modulo de engajamento (metas, XP, consistencia).
- `package.json`: comandos para iniciar, testar e gerar build.

## `tests/`

Aqui ficam os testes automatizados.

- `fase_1_organizacao_inteligente/`: testes da base da agenda.
- `fase_2_engajamento/`: testes do modulo de engajamento.
- `unit/`: testa partes pequenas.
- `integration/`: testa partes juntas.
- `e2e/`: testa fluxo ponta a ponta.

## `docs/`

Aqui fica a documentacao oficial.

- `docs/beginner/`: explicacao para quem nao programa.
- `docs/developer/`: explicacao tecnica para desenvolvedores.

## Arquivos importantes na raiz

- `README.md`: resumo principal do projeto.
- `requirements.txt`: bibliotecas Python.
- `pyproject.toml`: metadados e configuracao do backend.
- `.env.example`: modelo de variaveis de ambiente.
- `alembic.ini`: configuracao de migracoes do banco.
