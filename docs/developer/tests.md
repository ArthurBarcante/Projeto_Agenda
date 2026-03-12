# Tests

Os testes do projeto ficam centralizados em `tests/`.

A organizacao atual separa backend e frontend por area funcional, o que facilita manutencao e leitura.

## Estrutura geral

- `tests/backend/`: testes do backend.
- `tests/frontend/`: testes do frontend.
- `tests/config/`: arquivos de configuracao de ferramentas.

## Backend tests

Os testes de backend estao organizados por modulo:

- `tests/backend/appointments/`
- `tests/backend/auth/`
- `tests/backend/database/`
- `tests/backend/users/`

Os nomes atuais indicam o tipo de unidade validada dentro de cada modulo:

- `test_model.py`
- `test_repository.py`
- `test_router.py`
- `test_service.py`

Essa convencao reflete a arquitetura do backend e ajuda a localizar rapidamente a camada afetada por uma mudanca.

## Frontend tests

Os testes de frontend tambem estao separados por area funcional:

- `tests/frontend/appointments/`
- `tests/frontend/auth/`
- `tests/frontend/components/`
- `tests/frontend/users/`

Os nomes atuais costumam seguir o tipo de elemento testado, como paginas, hooks e componentes.

## Organizacao por feature

A principal regra estrutural do projeto e esta:

cada dominio funcional deve ter seus testes reunidos no mesmo agrupamento.

Isso aproxima o teste do contexto de negocio e evita uma pasta unica misturando responsabilidades diferentes.

## Configuracao

Os arquivos de configuracao ficam em `tests/config/`.

- `pytest.ini`: define `pythonpath`, `testpaths` e cache do pytest.
- `vitest.config.ts`: define a configuracao de testes do frontend.

## Leitura do estado atual

Os testes atuais ainda sao, em grande parte, estruturais e de smoke test.

Isso quer dizer que a suite ja registra a organizacao esperada do projeto, mesmo quando algumas regras de negocio ainda nao estao profundamente cobertas.

Essa base e util porque cria espacos claros para aumentar cobertura conforme a implementacao evolui.

## Direcao recomendada para novos testes

Ao adicionar uma funcionalidade nova:

1. coloque o teste no lado correto, backend ou frontend;
2. agrupe pela feature;
3. use o nome da camada ou do comportamento validado;
4. mantenha a correspondencia com a estrutura do codigo.