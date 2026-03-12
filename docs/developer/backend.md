# Backend

O backend usa FastAPI e esta organizado por dominio.

No estado atual do projeto, a estrutura esta preparada para crescer em camadas, mesmo que varias implementacoes ainda estejam em nivel inicial.

## Modulos

Os modulos principais ficam em `backend/app/`.

- `auth/`: autenticacao e utilitarios de seguranca.
- `users/`: estruturas relacionadas a usuarios.
- `appointments/`: estruturas relacionadas a compromissos.
- `utils/`: validacoes e helpers compartilhados.

Cada modulo segue uma ideia parecida de separacao de responsabilidades.

## Routers

Os routers definem os grupos de endpoints da API.

No projeto atual, cada modulo possui um `router.py` com um `APIRouter` configurado por prefixo:

- `auth` usa `/auth`
- `users` usa `/users`
- `appointments` usa `/appointments`

Na documentacao funcional, o dominio `appointments` e descrito em portugues como `compromissos`.

O nome tecnico do modulo e da rota permanece em ingles para acompanhar o codigo.

O arquivo `backend/app/main.py` registra esses routers na aplicacao principal.

Essa abordagem centraliza a composicao da API e deixa cada modulo responsavel pelo proprio conjunto de rotas.

## Services

Os services ficam responsaveis pela regra de negocio.

Hoje eles ainda estao enxutos, mas a intencao arquitetural e clara: a rota deve delegar comportamento para uma classe de servico, em vez de concentrar logica diretamente no endpoint.

Exemplo:

- `AppointmentService` recebe uma sessao do banco.
- O service cria e usa o repositorio correspondente.
- A camada de rota pode depender desse service para executar operacoes futuras.

Essa separacao facilita testes, refatoracao e crescimento da aplicacao.

## Repositories

Os repositories representam a camada de acesso a dados.

No estado atual, eles encapsulam a sessao SQLAlchemy e apontam para o modelo principal do dominio.

Exemplo:

- `AppointmentRepository` trabalha com o modelo `Appointment`.
- O repositorio recebe `Session` no construtor.

Mesmo ainda simples, essa camada cria um ponto unico para concentrar consultas quando o projeto evoluir.

## Schemas

Os schemas ficam em `schema.py` dentro de cada modulo e servem para validar entrada e saida da API.

Essa e a fronteira entre o formato externo da requisicao e os objetos usados internamente.

## Models

Os models representam as tabelas do banco usando SQLAlchemy.

No backend atual, ha dois modelos principais ja definidos:

- `User`
- `Appointment`

Ambos herdam de uma base com campos comuns e de uma base orientada a tenant.

## Interacao com o banco de dados

A infraestrutura de banco fica em `backend/db/`.

Os arquivos mais importantes sao estes:

- `connection.py`: cria a engine SQLAlchemy.
- `session.py`: inicializa e entrega sessoes.
- `base.py`: define `Base`, `BaseModel` e `TenantModel`.
- `alembic/`: estrutura de migracoes.

O ponto arquitetural mais importante aqui e o uso de `TenantModel`.

Essa classe base adiciona o campo de empresa e reforca a ideia de isolamento entre tenants.

## Fluxo de backend

O fluxo esperado de uma operacao segue este desenho:

1. O router recebe a requisicao.
2. O schema valida os dados.
3. O service aplica a regra de negocio.
4. O repository acessa o banco.
5. O backend devolve a resposta.

Mesmo quando parte desse fluxo ainda nao esta completa em todos os modulos, a documentacao e a estrutura do codigo apontam para esse padrao.

## Observacoes sobre o estado atual

O backend ainda esta em fase de consolidacao.

Existem sinais de uma arquitetura mais completa no historico do projeto e na organizacao das pastas, mas o codigo atual exposto em `backend/app/` esta mais enxuto e serve como base para expansao segura.

Para contribuir, o melhor caminho e manter essa separacao entre router, service, repository, schema e model.