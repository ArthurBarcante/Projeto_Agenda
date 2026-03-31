# Front-end: JavaScript

## Objetivo da camada JavaScript no projeto

A camada JavaScript controla o comportamento da interface no cliente: eventos de clique, envio de formularios, chamadas HTTP, roteamento de paginas e integracao entre UI e API.

No projeto atual, o JavaScript e o principal responsavel por conectar as telas de login/cadastro ao backend real ou ao mock local.

## Estrutura atual de scripts

A organizacao esta separada por responsabilidade:

- front/js/core/api.js: comunicacao HTTP com backend (real e mock).
- front/js/core/router.js: roteamento de paginas no front-end.
- front/js/auth/login.js: logica da tela de login.
- front/js/auth/register.js: logica da tela de cadastro.

Essa divisao reduz acoplamento e facilita testes e evolucao.

## Como o JavaScript funciona no sistema hoje

### 1. Core de API (api.js)

O projeto usa uma estrategia de alternancia por flag:

- USE_REAL_API = false: usa JSON Server (mock).
- USE_REAL_API = true: usa FastAPI (backend real).

Com isso, as funcoes conseguem operar em ambos os ambientes:

- loginRequest(email, password)
- registerRequest(userData)
- getUserByEmail(email)

Essa abordagem permite desenvolver frontend e backend de forma progressiva, sem interromper o fluxo de testes.

### 2. Roteamento simples (router.js)

O router injeta o HTML da pagina selecionada no container principal e carrega o script correspondente.

Fluxo resumido:

1. escolher pagina (login ou register);
2. buscar o HTML da pagina;
3. inserir no DOM;
4. carregar o modulo JS da pagina.

Esse modelo e uma SPA simples (single-page application) sem framework, util para estudo de fundamentos.

### 3. Logica da tela de login

O modulo de login:

- captura email e senha;
- chama loginRequest;
- armazena usuario no localStorage em caso de sucesso;
- redireciona para cadastro quando o usuario clica no link correspondente.

### 4. Logica da tela de cadastro

O modulo de cadastro:

- captura dados do formulario (nome, email, senha, confirmacao, CPF, telefone, data);
- valida senhas iguais no cliente;
- verifica email duplicado no modo mock;
- envia os dados usando registerRequest;
- realiza fluxo de pos-cadastro (feedback e navegacao).

## Boas praticas aplicadas

- Separacao clara entre regra de API e regra de interface.
- Uso de async/await para codigo assicrono legivel.
- Tratamento de erro com try/catch nas operacoes criticas.
- Centralizacao da estrategia de ambiente em um unico arquivo (api.js).

## Pontos de evolucao recomendados

Para evoluir o front-end de forma profissional, os proximos passos recomendados sao:

- Criar camada de servicos para separar regras de negocio da camada de tela.
- Implementar validacoes mais robustas (formato de telefone, CPF e senha).
- Trocar alert por componentes de feedback visual no DOM.
- Adicionar testes automatizados de fluxos (login/cadastro).
- Evoluir roteamento para um padrao mais escalavel, com controle de estado de sessao.

## Resumo tecnico

O JavaScript atual ja entrega autenticacao funcional e alternancia entre mock e API real. A base e didatica e adequada para estudo, e tambem e suficientemente modular para crescer para um front-end mais complexo nas proximas etapas.
