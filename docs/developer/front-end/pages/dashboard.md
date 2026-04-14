# Dashboard

Página inicial autenticada com métricas de progresso.

## Responsabilidades

- ler o resumo de progresso do usuário
- apresentar nível, streak e taxa de conclusão
- permitir ajuste da meta diária
- servir como porta de entrada da área autenticada

## Integração atual

- lê `GET /progress`
- atualiza meta diária com `PUT /progress`
