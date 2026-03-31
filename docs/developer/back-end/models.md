# Models no Back-end

## O que e um model neste projeto
No contexto deste projeto, **model** e a camada que representa os dados usados pela aplicacao no servidor.

Atualmente, como o sistema esta em fase de estudo e prototipacao, o projeto usa um **banco fake em memoria** em vez de um banco de dados real.

Arquivo principal:
- `back/app/models/fake_db.py`

## Como funciona hoje
O arquivo `fake_db.py` define uma lista chamada `users_db`.

Essa lista funciona como uma tabela simples de usuarios, contendo dicionarios Python com campos como:
- `id`
- `name`
- `email`
- `password`
- `birth_date`
- `cpf`
- `phone`

Exemplo de uso no sistema atual:
- A rota de login percorre `users_db` para verificar email e senha.
- A rota de registro verifica duplicidade e adiciona novos usuarios nessa lista.

## Papel arquitetural
Mesmo sendo simples, essa camada cumpre um papel importante:
- centraliza os dados do dominio de autenticacao
- desacopla as rotas da origem dos dados
- permite evolucao futura para banco real com menor impacto

Em outras palavras, as rotas nao precisam saber se os dados vem de lista, arquivo, SQLite ou PostgreSQL. Elas apenas consomem a camada de dados.

## Limites do modelo atual
Como `users_db` esta em memoria:
- os dados podem ser perdidos ao reiniciar o servidor
- nao ha concorrencia controlada
- nao ha persistencia transacional
- nao ha criptografia de senha

Essas limitacoes sao aceitaveis para ambiente educacional, mas nao para producao.

## Evolucao recomendada
Para evoluir essa camada sem quebrar o restante do sistema:
1. criar um repositorio de usuarios (ex.: `UserRepository`)
2. mover as operacoes de busca/criacao para esse repositorio
3. trocar a implementacao interna para ORM (SQLModel/SQLAlchemy)
4. manter a interface usada pelas rotas

Com isso, o projeto preserva a organizacao em camadas e fica mais proximo de um back-end profissional.
