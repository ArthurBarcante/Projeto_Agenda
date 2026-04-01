# Quais funções o projeto tem hoje

Este arquivo explica o que o Projeto Agenda já consegue fazer neste momento.

Como o sistema ainda está em desenvolvimento, algumas funções já existem e outras ainda serão criadas mais para frente.

## Funções que já estão funcionando

Hoje, o projeto já possui um primeiro núcleo funcional, voltado para usuários e autenticação.

Na prática, isso quer dizer que o sistema já consegue lidar com o processo de entrada de uma pessoa no sistema.

### 1. Cadastro de usuário

Uma pessoa já pode criar uma conta informando dados como:

- nome
- email
- senha
- telefone
- CPF
- data de nascimento
- tipo de usuário

O sistema também faz algumas verificações automáticas, como:

- confirmar se a senha e a confirmação de senha são iguais
- impedir email repetido
- impedir CPF repetido

## 2. Login com email e senha

Depois do cadastro, o usuário já pode entrar no sistema com email e senha.

Se os dados estiverem corretos, o backend libera o acesso.

Se estiverem errados, o sistema responde com erro de forma segura, sem dizer exatamente se o problema foi no email ou na senha.

## 3. Senha protegida

As senhas não ficam salvas de forma aberta no banco.

Em vez disso, o sistema transforma a senha em um formato protegido chamado hash.

Isso é importante porque, mesmo que alguém veja o conteúdo salvo no banco, não enxerga a senha original do usuário de forma direta.

## 4. Usuário salvo de verdade no banco

O sistema já usa PostgreSQL, que é um banco de dados real.

Isso significa que o cadastro não fica apenas em um arquivo temporário ou em memória. Os dados do usuário ficam gravados de forma persistente.

Em outras palavras, mesmo que a aplicação seja reiniciada, o usuário continua existindo no sistema.

## 5. Login com token

Quando o usuário faz login com sucesso, o sistema gera um token.

Esse token funciona como uma prova de que a pessoa já foi autenticada.

Depois disso, ele pode ser enviado nas próximas requisições para o backend reconhecer quem está acessando o sistema.

## 6. Rota protegida para identificar o usuário logado

O projeto já possui uma rota protegida que permite verificar quem está autenticado naquele momento.

Na prática, isso mostra que o sistema já consegue:

- receber o token
- validar se ele é verdadeiro
- descobrir qual usuário fez a requisição

## 7. Telas iniciais no frontend

No frontend, já existem telas iniciais para:

- login
- cadastro
- navegação entre essas telas

Isso quer dizer que o projeto já tem uma base visual para o fluxo de autenticação.

## 8. Modo mock e modo real

O projeto ainda mantém um modo de dados simulados para facilitar testes no frontend.

Ao mesmo tempo, o backend já possui persistência real de usuários.

Isso faz com que o sistema esteja em uma fase de transição: parte dele ainda pode usar dados simulados, mas a área de autenticação de usuários já está conectada a um banco real.

## O que ainda não está pronto

Apesar de essas funções já existirem, o projeto ainda não possui a parte principal da agenda completa.

Ainda faltam funções como:

- tarefas por usuário
- eventos e compromissos salvos no banco
- organização da rotina
- missões
- streaks
- painéis de progresso

## Resumindo

Hoje, o Projeto Agenda já tem funções reais e importantes:

- cadastro
- login
- senha protegida
- usuário salvo em banco de dados
- autenticação por token
- rota protegida para saber quem está logado

Isso mostra que o sistema já possui uma base funcional de backend, mesmo que a parte completa da agenda ainda esteja em construção.
