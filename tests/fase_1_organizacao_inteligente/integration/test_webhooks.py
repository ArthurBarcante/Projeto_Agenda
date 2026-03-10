import hashlib
import hmac
import json
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import Mock, patch

import requests

from app.modules.notifications.services.webhook_service import WebhookService


class FakeWebhookRepository:
    def __init__(self, subscriptions):
        self.subscriptions = subscriptions
        self.ultima_busca = None

    def buscar_por_evento(self, event_type, company_id):
        self.ultima_busca = (event_type, company_id)
        return self.subscriptions


def _assinatura_esperada(payload, secret):
    corpo_json = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hmac.new(
        secret.encode("utf-8"),
        corpo_json.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def test_enviar_webhooks_dispara_post_com_assinatura_hmac():
    company_id = uuid4()
    payload = {
        "appointment_id": str(uuid4()),
        "user_id": str(uuid4()),
    }
    subscription = SimpleNamespace(
        url="https://cliente.exemplo.com/webhook",
        secret="segredo-super-seguro",
    )
    repository = FakeWebhookRepository([subscription])
    service = WebhookService(db=Mock(), repository=repository)

    with patch("app.modules.notifications.services.webhook_service.requests.post") as post_mock:
        service.enviar_webhooks(
            event_type="APPOINTMENT_CREATED",
            payload=payload,
            company_id=company_id,
        )

    assert repository.ultima_busca == ("APPOINTMENT_CREATED", company_id)
    post_mock.assert_called_once()

    args, kwargs = post_mock.call_args
    assert args[0] == "https://cliente.exemplo.com/webhook"
    assert kwargs["json"] == payload
    assert kwargs["headers"]["Content-Type"] == "application/json"
    assert kwargs["headers"]["X-AIGENDA-SIGNATURE"] == _assinatura_esperada(
        payload,
        "segredo-super-seguro",
    )


def test_enviar_webhooks_nao_propaga_erro_http():
    company_id = uuid4()
    payload = {"appointment_id": str(uuid4())}
    subscriptions = [
        SimpleNamespace(url="https://cliente1.exemplo.com/webhook", secret="s1"),
        SimpleNamespace(url="https://cliente2.exemplo.com/webhook", secret="s2"),
    ]
    repository = FakeWebhookRepository(subscriptions)
    service = WebhookService(db=Mock(), repository=repository)

    with patch(
        "app.modules.notifications.services.webhook_service.requests.post",
        side_effect=requests.RequestException("timeout"),
    ) as post_mock:
        service.enviar_webhooks(
            event_type="APPOINTMENT_CANCELLED",
            payload=payload,
            company_id=company_id,
        )

    assert post_mock.call_count == 2
