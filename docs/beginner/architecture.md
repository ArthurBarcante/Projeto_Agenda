# Arquitetura Explicada para Leigos

## Antes de tudo: o que e "arquitetura"?

Arquitetura de software e como as partes do sistema se organizam para funcionar juntas.

Analogia simples:

- **Frontend** = recepcao (onde voce conversa com o sistema).
- **Backend** = escritorio interno (onde regras sao aplicadas).
- **Banco de dados** = arquivo da empresa (onde tudo fica guardado).
- **Redis** = bloco de notas rapido (acesso muito veloz para controles temporarios).

## Visao geral das pecas

O projeto usa duas partes principais:

1. **Frontend (Next.js/React)**
Interface que o usuario enxerga.

2. **Backend (FastAPI/Python)**
API que recebe pedidos, valida regras e conversa com o banco.

Tambem existem apoios:

- **PostgreSQL**: banco principal (dados oficiais).
- **Redis**: apoio para limite de requisicoes e desempenho.

## Diagrama simples da comunicacao

```text
[Usuario no navegador]
         |
         v
[Frontend - telas e botoes]
         |
         v
[Backend API - regras do negocio]
     |             |
     v             v
[PostgreSQL]    [Redis]
 (dados)      (controle rapido)
```

## Como um pedido acontece (passo a passo)

Exemplo: criar uma reuniao.

1. Usuario preenche formulario no frontend.
2. Frontend envia os dados para a API.
3. Backend identifica empresa e usuario (seguranca).
4. Backend verifica permissoes (quem pode criar).
5. Backend checa conflito de horario.
6. Se estiver tudo certo, salva no banco.
7. Retorna resposta para o frontend.
8. Usuario ve confirmacao na tela.

## Partes importantes do backend (explicacao conceitual)

### 1) Rotas da API

Sao as "portas de entrada" (ex: criar compromisso, cancelar compromisso).

### 2) Modulos de negocio

Cada area tem suas regras:

- agenda,
- usuarios,
- permissoes,
- auditoria,
- idempotencia,
- notificacoes.

### 3) Seguranca e controle

- Login com token (JWT).
- RBAC (papeis e permissoes).
- Isolamento por empresa (multi-tenant).

### 4) Qualidade e confiabilidade

- Testes em camadas (`unit`, `integration`, `e2e`).
- Migracoes de banco com Alembic.
- Auditoria para rastrear acoes.

## Conceitos essenciais desta arquitetura

### Multi-tenant (isolamento por empresa)

Analogia: predio comercial com varias salas.
Cada empresa usa sua propria sala e nao pode entrar na sala da vizinha.

### RBAC (controle por papeis)

Analogia: hospital.
Medico, recepcionista e financeiro tem acessos diferentes.

### Idempotencia

Analogia: compra online.
Se voce clicar no botao "pagar" duas vezes por engano, o sistema evita cobrar duas vezes.

### Maquina de estados

Analogia: entrega de pedido.
Um pedido passa por estados validos: "criado -> confirmado -> concluido" ou "criado -> cancelado".
Nao faz sentido pular etapas proibidas.

## Fluxo de seguranca simplificado

```text
Pedido chega na API
   |
   v
Validar token (quem e voce?)
   |
   v
Validar tenant (de qual empresa?)
   |
   v
Validar permissao (voce pode fazer isso?)
   |
   v
Executar regra de negocio
```

## Por que essa arquitetura e boa para iniciantes entenderem?

- Separa responsabilidades (cada parte faz uma coisa).
- Facilita manutencao futura.
- Reduz erros em producao.
- Permite crescimento por fases sem quebrar tudo.

## Resumo rapido

O AIgenda usa uma arquitetura de "camadas":

- interface para o usuario,
- API com regras de negocio,
- banco de dados para persistencia,
- mecanismos extras de seguranca e performance.

Isso torna o sistema mais previsivel, seguro e pronto para evoluir.
