# Front-end: CSS

## Objetivo da camada CSS no projeto

A camada de CSS define a aparencia visual da interface: cores, fontes, espacamentos, alinhamentos, responsividade e comportamento visual dos componentes.

No contexto deste projeto, o CSS organiza a experiencia do usuario nas telas de autenticacao (login e cadastro) e prepara o sistema para crescimento de outras telas.

## Estrutura atual de estilos

A organizacao atual segue esta divisao:

- front/css/style.css: estilos globais da aplicacao (variaveis, reset basico, layout base).
- front/css/auth/login.css: estilos especificos da tela de login.
- front/css/auth/register.css: estilos especificos da tela de cadastro.

Essa separacao ajuda a manter o codigo limpo e facilita manutencao, pois cada arquivo cuida de um escopo claro.

## Como o CSS funciona no sistema hoje

### 1. Estilos globais

No arquivo global, o projeto define:

- variaveis visuais reutilizaveis (cores e padroes de UI);
- configuracoes gerais de layout;
- comportamento base para centralizacao e consistencia visual.

Isso reduz repeticao e melhora padronizacao entre as telas.

### 2. Estilos por tela

Cada tela de autenticacao possui seu proprio arquivo, com regras especificas para:

- container principal;
- inputs;
- botoes;
- links de navegacao entre login e cadastro.

Com isso, o sistema consegue manter identidade visual unica e, ao mesmo tempo, permitir ajustes localizados por tela.

### 3. Padrao visual atual

Atualmente, login e cadastro seguem o mesmo padrao:

- tipografia consistente;
- caixa centralizada;
- campos com dimensoes equivalentes;
- espacos e margens equilibrados;
- feedback visual em hover/focus.

Esse alinhamento melhora a usabilidade e reduz atrito na navegacao.

## Boas praticas aplicadas

- Separacao entre estilo global e estilo de pagina.
- Reuso de variaveis CSS para manter consistencia.
- Nomes de classes descritivos (ex.: login-container, register-container, auth-wrapper).
- Evitar regras excessivamente genericas que possam quebrar outras telas.

## Pontos de evolucao recomendados

Para a proxima fase do projeto, evolucoes importantes incluem:

- Criar um design system simples (tokens de cor, espaco, tipografia e componentes).
- Padronizar nomenclatura de classes para escalabilidade.
- Melhorar responsividade em diferentes larguras de tela.
- Criar estados visuais de erro e sucesso em formularios (alem de alertas JS).
- Definir guia de estilo para garantir consistencia entre futuras telas (dashboard, tarefas, calendario).

## Resumo tecnico

No estado atual, o CSS cumpre bem o papel de entregar uma interface de autenticacao organizada e consistente. A base esta pronta para crescimento, desde que as proximas telas sigam o mesmo principio de separacao por responsabilidade e reutilizacao de estilos globais.
