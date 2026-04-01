# Security (Back-end)

## Objetivo deste documento

Este arquivo explica a parte de seguranca que foi criada para tornar a persistencia de usuario confiavel no sistema.

Aqui estao os mecanismos que impedem o projeto de salvar senha em texto puro e que permitem identificar quem esta autenticado.

---

## O que e a camada de seguranca neste projeto

No contexto atual, seguranca significa principalmente duas coisas:

- proteger a senha do usuario
- controlar a autenticacao por token

Esses dois problemas aparecem juntos porque persistencia de usuario nao e apenas "salvar dados no banco". E preciso salvar de forma segura e depois reconhecer esse usuario nas proximas requisicoes.

---

## O que foi feito

Hoje o projeto possui uma base completa de autenticacao e seguranca para o fluxo de usuario.

### 1. Hash de senha com bcrypt

No arquivo `back/app/core/security.py` foram criadas funcoes para:

- gerar hash da senha antes de salvar
- verificar se a senha informada no login corresponde ao hash guardado

Isso significa que a senha original nao fica gravada no banco.

Em vez de salvar algo como:

```text
123456
```

o sistema salva algo parecido com:

```text
$2b$12$...
```

### 2. Criacao de token JWT

No mesmo arquivo tambem foi implementada a funcao que cria o token JWT depois do login.

Esse token leva informacoes como:

- o identificador do usuario em `sub`
- o tempo de expiracao em `exp`

### 3. Leitura e validacao do token

Ainda na parte de seguranca, o sistema consegue decodificar o JWT e identificar se ele ainda e valido.

### 4. Usuario autenticado por dependencia

Em `back/app/core/auth.py` foi criada a funcao `get_current_user`.

Ela faz este fluxo:

1. recebe o token Bearer da requisicao
2. decodifica o JWT
3. extrai o `sub`
4. busca o usuario no banco
5. devolve esse usuario para a rota protegida

---

## Qual e a funcao dessa parte no sistema

Essa camada tem tres funcoes principais.

### 1. Proteger dados sensiveis

Se houver vazamento do banco, a senha original nao estara exposta diretamente.

### 2. Permitir autenticacao real

No login, o backend consegue conferir se a senha digitada combina com o hash salvo.

### 3. Manter o usuario identificado entre requisicoes

Depois do login, o token JWT passa a funcionar como prova de autenticacao. Assim o sistema consegue saber quem esta fazendo a chamada sem depender de sessao tradicional no servidor.

---

## Relacao com a persistencia de usuario

Este ponto e importante: seguranca e persistencia caminham juntas.

Quando o usuario e cadastrado, o sistema nao salva apenas um registro. Ele salva um registro protegido.

Quando o usuario faz login, o sistema nao apenas compara campos. Ele valida uma credencial de forma segura.

Isso transforma o cadastro e o login em um fluxo real de autenticacao, e nao apenas em um formulario que grava texto no banco.

---

## Onde isso aparece no fluxo real

### Cadastro

- a rota recebe os dados
- valida o schema
- gera hash da senha
- salva o usuario no PostgreSQL

### Login

- a rota busca o usuario pelo email
- usa `verify_password`
- cria um JWT com `sub`
- devolve `access_token` e `token_type`

### Rota protegida

- o frontend envia `Authorization: Bearer TOKEN`
- `get_current_user` valida o token
- a rota recebe o usuario autenticado

---

## Resumo tecnico-didatico

A camada de seguranca do projeto faz a ponte entre duas necessidades fundamentais:

- salvar usuario com seguranca
- autenticar usuario nas proximas requisicoes

Em outras palavras:

- `security.py` protege senha e gera token
- `auth.py` identifica quem esta logado

Sem essa camada, o sistema ate poderia cadastrar usuarios, mas nao teria autenticacao confiavel.
