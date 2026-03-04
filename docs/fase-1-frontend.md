# Fase 1 — Frontend

O frontend da Fase 1 é responsável por oferecer uma interface objetiva para autenticação e visualização inicial da agenda, conectando-se ao backend da Organização Inteligente.

## Objetivo do frontend na Fase 1

- Permitir login de usuário
- Exibir área inicial autenticada
- Servir como base para evolução das próximas fases

## Estrutura atual

Diretório: `frontend/src`

- `main.tsx`: ponto de entrada da aplicação React
- `App.tsx`: composição principal do app
- `Login.tsx`: tela de autenticação
- `Dashboard.tsx`: painel principal após login

## Papel funcional de cada tela

### Login

Centraliza o fluxo de entrada do usuário no sistema e prepara o consumo das rotas protegidas no backend.

### Dashboard

Apresenta a área inicial do usuário autenticado. Na fase atual, funciona como estrutura-base para acoplar listagem de compromissos, métricas e blocos de produtividade nas fases seguintes.

## Integração com backend

O frontend da Fase 1 foi organizado para consumir endpoints de autenticação e agenda do backend FastAPI. O objetivo é manter separação clara entre apresentação (frontend) e regras de negócio (backend).

## Resultado da Fase 1 no frontend

- Fluxo inicial de autenticação definido
- Estrutura de telas pronta para expansão
- Base técnica para incorporar engajamento e personalização sem refatorações profundas
