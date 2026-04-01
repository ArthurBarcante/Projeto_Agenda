# Future Requirements (Developer)

## Objetivo deste documento

Este arquivo explica o que o projeto ainda precisa evoluir depois do que foi implementado ate agora.

Hoje o sistema ja possui:

- FastAPI como base da API
- PostgreSQL como banco real
- SQLAlchemy para persistencia
- cadastro de usuario com validacao
- hash de senha com `bcrypt`
- login com JWT
- rota protegida para identificar o usuario autenticado

Ou seja: o `requirements.txt` ja foi atualizado para sustentar a base atual do backend. O foco deste documento agora nao e mais "o que instalar para comecar", e sim "o que ainda falta para o sistema crescer com qualidade".

---

## Dependencias atuais mais importantes

Hoje, as bibliotecas centrais do projeto sao estas:

```txt
fastapi
uvicorn[standard]
pydantic[email]
sqlalchemy
psycopg2-binary
bcrypt
python-jose
```

Funcao de cada grupo:

- `fastapi` e `uvicorn`: criacao e execucao da API
- `pydantic[email]`: validacao dos dados recebidos
- `sqlalchemy` e `psycopg2-binary`: comunicacao com PostgreSQL
- `bcrypt`: protecao das senhas
- `python-jose`: criacao e leitura de tokens JWT

---

## Proximas evolucoes tecnicas recomendadas

## 1. Configuracao por ambiente

### O que e

Separar valores sensiveis e especificos de maquina do codigo-fonte.

### O que ainda precisa ser feito

- mover `DATABASE_URL` para variavel de ambiente
- mover `SECRET_KEY` para variavel de ambiente
- criar um arquivo `.env` local para desenvolvimento
- centralizar configuracoes em um modulo proprio

### Por que isso importa

Hoje parte da configuracao ainda esta escrita diretamente no codigo. Isso e aceitavel no estudo inicial, mas fica fragil quando o projeto cresce ou muda de ambiente.

---

## 2. Migracoes de banco de dados

### O que e

Um sistema para controlar mudancas de estrutura no banco de dados ao longo do tempo.

### O que ainda precisa ser feito

- adicionar `alembic`
- gerar a primeira migracao da tabela `users`
- parar de depender apenas de `Base.metadata.create_all()`

### Por que isso importa

`create_all()` e bom para estudo e primeiros passos. Em projetos maiores, migracoes versionadas tornam as mudancas previsiveis e rastreaveis.

---

## 3. Testes automatizados reais

### O que e

Verificacoes executadas automaticamente para provar que o sistema continua funcionando depois de cada alteracao.

### O que ainda precisa ser feito

- instalar `pytest`
- adicionar testes para `/auth/register`
- adicionar testes para `/auth/login`
- adicionar testes para `/auth/me`
- criar cenarios de erro, como email duplicado e token invalido

### Por que isso importa

Hoje o projeto ja foi validado manualmente, mas ainda depende bastante de testes feitos na mao. Testes automatizados reduzem regressao.

---

## 4. Evolucao do dominio da agenda

### O que e

Expandir o sistema para alem da autenticacao e transformar o projeto em uma agenda de fato.

### O que ainda precisa ser feito

- criar modelos reais de tarefas
- criar modelos reais de eventos
- relacionar tarefas e eventos ao usuario autenticado
- criar CRUD completo dessas entidades

### Por que isso importa

Hoje a autenticacao esta pronta, mas o dominio principal da aplicacao ainda nao esta persistido no banco com o mesmo nivel de maturidade.

---

## 5. Regras de permissao

### O que e

Definir o que cada tipo de usuario pode ou nao pode fazer.

### O que ainda precisa ser feito

- formalizar os papeis como `user`, `admin` e possiveis novos perfis
- criar verificacoes de permissao nas rotas
- evitar que qualquer usuario acesse recursos administrativos

### Por que isso importa

O campo `role` ja existe no modelo `User`, mas ainda nao esta sendo usado para controlar acesso.

---

## 6. Respostas de API mais consistentes

### O que e

Padronizar o formato das respostas que a API devolve.

### O que ainda precisa ser feito

- criar schemas de saida
- documentar melhor erros esperados
- manter padrao estavel entre sucesso e falha

### Por que isso importa

Isso melhora a integracao com o frontend e reduz ambiguidade para quem esta estudando o projeto.

---

## Ordem sugerida de evolucao

1. Externalizar configuracoes sensiveis.
2. Adicionar migracoes com Alembic.
3. Criar testes automatizados de autenticacao.
4. Implementar persistencia real de tarefas e eventos.
5. Adicionar autorizacao por perfil.

Essa ordem e pragmatica porque primeiro fortalece a base tecnica, depois expande a regra de negocio principal do sistema.
