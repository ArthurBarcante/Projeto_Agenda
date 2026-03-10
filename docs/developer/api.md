# API Reference

## Convencoes

- base local: `http://127.0.0.1:8000`
- autenticacao: `Authorization: Bearer <jwt>`
- formato: `application/json`

Modelo de erro padrao (handlers globais):

```json
{
  "erro": {
    "codigo": "VALIDATION_FAILED",
    "mensagem": "Dados de entrada invalids",
    "timestamp": "2026-03-09T18:00:00Z"
  }
}
```

## Autenticacao

## `POST /auth/login`

Rota legada equivalente: `POST /authentication/login`.

Request:

```json
{
  "company_identifier": "acme",
  "email": "user@acme.com",
  "senha": "123456"
}
```

Response 200:

```json
{
  "token_acesso": "<jwt>",
  "tipo_token": "bearer"
}
```

Erros comuns:

- 401: credenciais invalidas.

## Agenda

## `POST /appointments`

- permissao exigida: `agenda.criar`
- header opcional: `Idempotency-Key`

Request:

```json
{
  "title": "Reuniao de planejamento",
  "description": "Sprint semanal",
  "start_time": "2026-03-10T10:00:00Z",
  "end_time": "2026-03-10T11:00:00Z",
  "participant_ids": ["f7b1c4f0-75d9-4d5c-8f94-b5baf8f71a6a"]
}
```

Compatibilidade de payload:

- `participant_ids` (atual)
- `participantes_ids` (legado suportado por alias)

Response 201:

```json
{
  "id": "6f8472d2-7de8-4f92-95d0-52b4fc96f7df",
  "company_id": "3ecb70cb-0ea5-4c08-b95f-6118c27fdb53",
  "creator_id": "56e6f976-0e4d-4dbf-9f15-a6e0adac8268",
  "title": "Reuniao de planejamento",
  "description": "Sprint semanal",
  "start_time": "2026-03-10T10:00:00Z",
  "end_time": "2026-03-10T11:00:00Z",
  "status": "scheduled",
  "created_at": "2026-03-09T18:00:00Z",
  "updated_at": "2026-03-09T18:00:00Z"
}
```

Erros comuns:

- 403: sem permissao.
- 409: conflito de horario.
- 409: `Idempotency-Key` reutilizada com payload diferente.

## `PUT /appointments/{appointment_id}`

Atualiza campos do compromisso.

Request tipico:

```json
{
  "title": "Reuniao atualizada",
  "start_time": "2026-03-10T12:00:00Z",
  "end_time": "2026-03-10T13:00:00Z"
}
```

Erros comuns:

- 403: usuario nao e criador.
- 400: estado do compromisso nao permite update.
- 404: compromisso nao encontrado no tenant.

## `PATCH /appointments/{appointment_id}/cancel`

Cancela compromisso.

Erros comuns:

- 403: usuario nao e criador.
- 400: compromisso nao pode ser cancelado.
- 404: compromisso nao encontrado no tenant.

## Utilitario

## `GET /me`

Retorna identificadores do usuario autenticado.

Response 200:

```json
{
  "user_id": "56e6f976-0e4d-4dbf-9f15-a6e0adac8268",
  "company_id": "3ecb70cb-0ea5-4c08-b95f-6118c27fdb53"
}
```

## Exemplo de criacao com idempotencia

```bash
curl -X POST http://127.0.0.1:8000/appointments \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 7f005748-8c8e-4f89-92ea-9d4aa5e6b220" \
  -d '{
    "title": "Reuniao",
    "description": "planejamento",
    "start_time": "2026-03-10T10:00:00Z",
    "end_time": "2026-03-10T11:00:00Z",
    "participant_ids": []
  }'
```
