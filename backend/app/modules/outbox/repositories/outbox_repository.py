from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.outbox.models.outbox_event import OutboxEvent, StatusOutboxEvento
from app.core.db.repositories import BaseRepository


class OutboxRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def criar_evento(
        self,
        company_id: UUID,
        event_type: str,
        payload: dict[str, object],
    ) -> OutboxEvent:
        evento = OutboxEvent(
            company_id=company_id,
            event_type=event_type,
            payload=payload,
            status=StatusOutboxEvento.PENDING.value,
            attempts=0,
        )
        self.add(evento)
        self.flush()
        return evento

    def buscar_eventos_pendentes(self, limite: int = 100) -> list[OutboxEvent]:
        agora = datetime.now(timezone.utc)
        return (
            self.query(OutboxEvent)
            .filter(OutboxEvent.status == StatusOutboxEvento.PENDING.value)
            .filter(OutboxEvent.process_at <= agora)
            .order_by(OutboxEvent.process_at.asc(), OutboxEvent.created_at.asc())
            .limit(limite)
            .all()
        )

    def marcar_como_processando(self, evento: OutboxEvent) -> OutboxEvent:
        evento.status = StatusOutboxEvento.PROCESSING.value
        self.flush()
        return evento

    def marcar_como_concluido(self, evento: OutboxEvent) -> OutboxEvent:
        evento.status = StatusOutboxEvento.DONE.value
        self.flush()
        return evento

    def incrementar_tentativa(
        self,
        evento: OutboxEvent,
        max_tentativas: int = 3,
        retry_delay_segundos: int = 60,
    ) -> OutboxEvent:
        current_attempts = getattr(evento, "attempts", getattr(evento, "tentativas", 0))
        updated_attempts = current_attempts + 1
        if hasattr(evento, "attempts"):
            evento.attempts = updated_attempts
        else:
            evento.tentativas = updated_attempts

        if updated_attempts >= max_tentativas:
            evento.status = StatusOutboxEvento.FAILED.value
        else:
            evento.status = StatusOutboxEvento.PENDING.value
            retry_time = datetime.now(timezone.utc) + timedelta(seconds=retry_delay_segundos)
            if hasattr(evento, "process_at"):
                evento.process_at = retry_time
            else:
                evento.processar_em = retry_time
        self.flush()
        return evento
