# Front-end: UI (Interface do Usuario)

## O que e a camada de UI neste projeto

A camada de UI representa a estrutura visual das paginas em HTML e a forma como os componentes sao apresentados ao usuario.

Em termos praticos, ela define:

- o que o usuario ve;
- onde cada campo aparece;
- como os fluxos de navegacao sao exibidos;
- como os elementos visuais se organizam no layout.

## Estrutura atual de UI

A pasta de UI esta organizada por dominio de funcionalidade:

- front/ui/auth/login.html: interface da tela de login.
- front/ui/auth/register.html: interface da tela de cadastro.

As paginas sao carregadas dinamicamente pelo router, sem recarregar o site inteiro.

## Como a UI funciona no sistema hoje

### 1. Tela de login

A UI de login contem:

- cabecalho visual do sistema;
- formulario com email e senha;
- botao de acesso;
- link para navegar para cadastro.

Essa tela e o ponto inicial de entrada do usuario.

### 2. Tela de cadastro

A UI de cadastro contem:

- titulo principal da tela;
- formulario com campos completos de registro;
- confirmacao de senha;
- link para retornar ao login.

Os campos atuais refletem o padrao funcional definido no backend e no mock:

- name
- email
- password
- confirm_password
- birth_date
- cpf
- phone

### 3. Navegacao entre telas

A navegacao entre login e cadastro e feita por links internos que chamam o router do front-end. Esse fluxo evita refresh completo da pagina e melhora experiencia de uso.

## Decisoes de design atuais

- Estrutura simples e didatica para estudo.
- Componentes focados em autenticacao.
- Consistencia visual entre login e cadastro.
- Formularios orientados ao fluxo real de dados do sistema.

## Pontos de evolucao recomendados

Para evoluir a UI na proxima fase do projeto:

- Criar componentes reutilizaveis (input, botao, mensagem de erro).
- Adicionar feedback visual inline de validacao (sem depender so de alert).
- Preparar estrutura de layout para dashboard, calendario e tarefas.
- Melhorar acessibilidade (labels, contraste, navegacao por teclado).
- Padronizar semantica HTML para facilitar manutencao e testes.

## Relacao entre UI, JS e CSS

No projeto atual, a UI e a camada estrutural que trabalha em conjunto com:

- CSS: define a apresentacao visual;
- JavaScript: define o comportamento e integracao com API.

Essa separacao de responsabilidade e um principio importante em desenvolvimento de front-end e ajuda estudantes a entender arquitetura de aplicacoes web modernas.
