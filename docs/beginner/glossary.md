# Glossario para Iniciantes

Este glossario traduz termos tecnicos do projeto para linguagem simples.

## A

**API**
E a "porta" pela qual um sistema conversa com outro.
No AIgenda, o frontend envia pedidos para a API do backend.

**Autenticacao**
Processo de confirmar identidade (quem voce e).
Exemplo: login com email e senha.

**Autorizacao**
Define o que voce pode fazer apos entrar.
Exemplo: usuario comum nao pode acessar funcoes de administrador.

## B

**Backend**
Parte interna do sistema, onde ficam regras e processamento.

**Banco de dados**
Local onde informacoes ficam armazenadas de forma organizada.

## C

**Compromisso**
Evento/reuniao agendada no sistema.

**Conflito de horario**
Quando duas atividades ocupam o mesmo horario para a mesma pessoa.

## E

**E2E (End-to-End)**
Tipo de teste que valida o fluxo completo, como um usuario real usaria.

## F

**FastAPI**
Tecnologia usada no backend para criar APIs em Python.

**Frontend**
Parte visual do sistema: telas, botoes e formularios.

## I

**Idempotencia**
Mecanismo para impedir efeito duplicado ao repetir a mesma requisicao.
Exemplo: evitar criar dois compromissos iguais por clique duplo.

**Indice de performance**
Estrutura no banco que acelera buscas.

## J

**JWT (token)**
"Cracha digital" usado para provar que voce esta autenticado.

## M

**Maquina de estados**
Regras que controlam as mudancas de status de um compromisso.
Exemplo: criado -> confirmado -> concluido.

**Metricas de consistencia**
Indicadores que mostram se usuario mantem regularidade na rotina.

**Multi-tenant**
Arquitetura que separa dados por empresa.
Cada empresa acessa apenas o proprio conteudo.

## O

**Outbox**
Padrao para registrar eventos de forma segura antes de integra-los com outros sistemas.

## P

**Painel de desempenho**
Tela com indicadores de progresso (metas, consistencia, produtividade).

**Permissao**
Regra que libera ou bloqueia certas acoes para cada tipo de usuario.

## R

**Rate limit**
Limite de quantidade de requisicoes em um periodo de tempo.
Ajuda a proteger o sistema contra abuso.

**RBAC (Role-Based Access Control)**
Modelo de acesso baseado em papeis.
Exemplo: admin, gestor, colaborador.

**Redis**
Banco de dados em memoria, muito rapido, usado para controles temporarios.

## T

**Tenant**
Empresa/organizacao dentro de um sistema multi-tenant.

**Teste de integracao**
Teste que valida se modulos diferentes funcionam bem juntos.

**Teste unitario**
Teste de uma parte pequena e isolada do codigo.

## X

**XP (Experiencia)**
Pontos ganhos por boas praticas e constancia no uso do sistema.

## Dica final

Se algum termo parecer dificil, pense assim:

- "Quem usa" -> frontend
- "Quem decide regras" -> backend
- "Quem guarda historico" -> banco de dados

Com esse mapa mental, quase tudo fica mais facil de entender.
