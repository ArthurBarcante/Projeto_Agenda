# Estado atual do projeto

Hoje o Projeto Agenda já tem uma base funcional real, mas ainda não está completo.

Isso quer dizer o seguinte:

- a parte de usuários já funciona de verdade
- a parte principal da agenda ainda está em construção

## O que o projeto já tem hoje

Atualmente o sistema já está dividido em áreas diferentes:

- frontend, que é a parte visual
- backend, que é a parte que processa os dados
- banco de dados, onde os usuários ficam salvos
- documentação, que explica o projeto

Essa organização é importante porque facilita o crescimento do sistema ao longo do tempo.

## O que já funciona no backend

O backend já possui uma API feita em FastAPI.

Hoje, essa API já consegue:

- cadastrar usuários
- validar se o email já existe
- validar se o CPF já existe
- verificar se a senha e a confirmação de senha são iguais
- salvar a senha de forma protegida
- fazer login com email e senha
- gerar token de autenticação
- identificar o usuário logado em rota protegida

Isso significa que a área de autenticação do sistema já não está mais em fase de simulação. Ela já funciona com persistência real.

## O que já funciona no banco de dados

O projeto já usa PostgreSQL para salvar usuários.

Na prática, isso significa que:

- os dados do usuário ficam armazenados de verdade
- o cadastro continua existindo depois que a aplicação é fechada
- o sistema já tem uma tabela de usuários criada

Em resumo, o projeto já possui persistência real de usuários.

## O que já funciona no frontend

No frontend, já existem as telas iniciais de:

- login
- cadastro

Também já existe navegação entre essas telas.

O frontend ainda está em uma etapa de evolução. Ele já pode conversar com a API real, mas ainda mantém suporte a dados simulados em algumas situações de teste e desenvolvimento.

## O que significa "dados simulados"

Dados simulados, ou mock, são dados usados apenas para desenvolvimento e testes.

Eles ajudam quando a interface ainda está sendo construída ou quando nem tudo do backend está pronto.

No Projeto Agenda, isso ainda existe em partes do frontend, mas o cadastro e a autenticação de usuários no backend já usam banco real.

## O que ainda não está pronto

A proposta principal do projeto é ser uma agenda inteligente completa.

Essa parte ainda não foi implementada.

Hoje ainda faltam recursos como:

- agenda de compromissos por usuário
- tarefas salvas no banco
- eventos ligados a cada conta
- organização da rotina
- missões
- streaks
- acompanhamento visual de progresso

## O que isso mostra sobre o momento do projeto

O projeto já passou da fase de ideia e já entrou em uma fase de base funcional.

Ele ainda não entrega a experiência completa da agenda inteligente, mas já tem um primeiro bloco sólido e importante funcionando:

- autenticação real
- persistência de usuários
- segurança básica de senha
- identificação do usuário autenticado

## Resumindo

Hoje, o Projeto Agenda já tem um sistema real de usuários funcionando.

O que falta agora é expandir essa base para a parte mais visível da proposta: tarefas, eventos, rotina, progresso e recursos de acompanhamento.
