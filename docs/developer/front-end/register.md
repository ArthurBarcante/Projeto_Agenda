# Cadastro

## O que e

Esta funcionalidade permite criar uma nova conta pelo frontend.

Ela coleta os dados do usuario, aplica algumas validacoes simples no cliente, envia a requisicao para a API e decide o proximo passo com base no modo atual da aplicacao.

## Arquivos desta funcionalidade

- `front/ui/auth/register.html`
- `front/js/auth/register.js`
- `front/js/core/api/api.js`
- `front/js/core/configs/config.js`
- `front/js/core/configs/session.js`
- `front/css/auth/register.css`

## Responsabilidade de cada arquivo

- `ui/auth/register.html`: define os campos do formulario de criacao de conta.
- `js/auth/register.js`: aplica mascara de CPF, valida confirmacao de senha, chama a API e redireciona o fluxo.
- `js/core/api/api.js`: executa o cadastro em modo real ou mock.
- `js/core/configs/config.js`: define se o frontend esta usando backend real ou mock.
- `js/core/configs/session.js`: salva sessao local quando o modo mock autentica automaticamente apos o cadastro.
- `css/auth/register.css`: estiliza o formulario e os estados visuais da pagina.

## Detalhes

### Tecnologias usadas

- HTML para o formulario
- CSS para a composicao visual
- JavaScript modular para logica da pagina
- Fetch API para comunicacao com backend ou mock

### Fluxo atual do cadastro no frontend

1. O usuario preenche os campos do formulario.
2. `register.js` valida se senha e confirmacao coincidem.
3. Em modo mock, o frontend consulta se o email ja existe.
4. O frontend envia os dados para `registerRequest`.
5. Em modo real, o usuario volta para o login depois do sucesso.
6. Em modo mock, o usuario ja entra direto no dashboard.

### Comportamento atual

- o CPF recebe mascara durante a digitacao
- a confirmacao de senha e validada no frontend antes da chamada principal
- em modo real, a verificacao de email duplicado fica concentrada no backend
- mensagens de sucesso e erro usam `alert` no estado atual

### Estado atual da funcionalidade

O cadastro esta funcional e atende o fluxo basico da aplicacao.

O que ainda nao existe nessa funcionalidade:

- exibicao inline de erros por campo
- validacoes de UX mais completas
- feedback visual de carregamento
