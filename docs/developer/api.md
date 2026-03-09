# API Reference (Estudo Tecnico)

## 1. Convencoes gerais
- Base local: `http://127.0.0.1:8000`
- Auth: `Authorization: Bearer <jwt>`
- Content-Type: `application/json`
- Modelo de erro padrao:

```json
{
  "erro": {
    "codigo": "VALIDATION_FAILED",
    "mensagem": "Dados de entrada invalids",
    "timestamp": "2026-03-09T18:00:00Z"
  }
}
```

## 2. Autenticacao
### `POST /auth/login`
Alias legado: `POST /authentication/login`

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

## 3. Agenda
### `POST /appointments`
- Permissao exigida: `agenda.criar`
- Header opcional: `Idempotency-Key`

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

Compatibilidade:
- `participantes_ids` tambem e aceito.

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
- 400/409: conflito de horario.
- 403: sem permissao.
- 409: `Idempotency-Key` reutilizada com payload diferente.

### `PUT /appointments/{appointment_id}`
Atualiza campos permitidos (`title`, `description`, `start_time`, `end_time`, `status`).

Erros comuns:
- 403: usuario nao e autor.
- 400: appointment fora de estado atualizavel.
- 404: appointment inexistente no tenant.

### `PATCH /appointments/{appointment_id}/cancel`
Cancela compromisso.

Erros comuns:
- 403: usuario nao e autor.
- 400: appointment nao pode ser cancelado.
- 404: nao encontrado no tenant.

## 4. Endpoint utilitario
### `GET /me`
Retorna identificadores de usuario e empresa com base no token.

Response 200:
```json
{
  "user_id": "56e6f976-0e4d-4dbf-9f15-a6e0adac8268",
  "company_id": "3ecb70cb-0ea5-4c08-b95f-6118c27fdb53"
}
```

## 5. Exemplo de chamada com idempotencia
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

## 6. API e evolucao por fases
- Fase 1: endpoints atuais cobrem autenticacao e agenda robusta.
- Fase 2: esperado adicionar APIs de metas, XP e painel.
- Fase 3: esperado adicionar APIs de niveis e feature unlock.
- Fase 4: esperado adicionar APIs de recomendacao e ajuste adaptativo.

Recomendacao de estudo:
- manter versionamento explicito quando fases 2-4 entrarem em producao para preservar compatibilidade de clientes existentes.
