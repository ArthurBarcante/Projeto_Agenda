# Schemas no Back-end

## O que e um schema
No FastAPI (com Pydantic), **schema** e a estrutura que define:
- quais campos a API espera receber
- quais tipos cada campo deve ter
- quais validacoes devem acontecer antes da regra de negocio

Na pratica, schemas funcionam como contrato de dados entre cliente e servidor.

Arquivos atuais:
- `back/app/schemas/auth/login.py`
- `back/app/schemas/auth/register.py`

## Login Schema
Arquivo: `back/app/schemas/auth/login.py`

Classe atual:
- `LoginRequest`

Campos:
- `email: str`
- `password: str`

Uso no sistema:
- aplicado na rota `POST /auth/login`
- garante que o payload tenha os campos esperados

## Register Schema
Arquivo: `back/app/schemas/auth/register.py`

Classe atual:
- `RegisterRequest`

Campos:
- `name: str`
- `email: EmailStr`
- `password: str`
- `confirm_password: str`
- `birth_date: date`
- `cpf: str`
- `phone: str`

### Validacoes aplicadas
O schema usa `@field_validator("confirm_password")` para garantir que:
- `confirm_password` seja igual a `password`

Se for diferente, o schema levanta erro de validacao com a mensagem:
- `As senhas nao coincidem`

### Campo somente para validacao
O campo `confirm_password` existe para validacao de formulario e **nao deve ser persistido**.

Para apoiar esse fluxo, a classe possui `to_user_data()`, que:
1. gera um dicionario com `model_dump()`
2. remove `confirm_password`
3. retorna somente os dados que podem ser salvos

## Beneficios de usar schemas
- reduz erros de payload no endpoint
- melhora documentacao automatica no Swagger
- concentra validacoes em um ponto unico
- facilita manutencao e testes

## Evolucao recomendada
Para amadurecer a camada de schemas:
1. criar schemas separados de entrada e saida (Request/Response)
2. ocultar campos sensiveis (ex.: nunca retornar `password`)
3. adicionar validadores para CPF e telefone
4. padronizar mensagens de erro
5. versionar contratos de API quando houver mudancas grandes

Esse caminho fortalece o contrato da API e torna o sistema mais previsivel para front-end e testes automatizados.
