import logging

from sqlalchemy.orm import Session

from app.core.events.event_bus import event_bus
from app.modules.outbox.repositories.outbox_repository import OutboxRepository


logger = logging.getLogger(__name__)


def processar_eventos(db: Session, limite: int = 100) -> int:
    repositorio = OutboxRepository(db)
    eventos = repositorio.buscar_eventos_pendentes(limite=limite)
    processados = 0

    for evento in eventos:
        try:
            repositorio.marcar_como_processando(evento)
            db.commit()

            logger.info(
                "Processando evento outbox",
                extra={
                    "evento_id": str(evento.id),
                    "company_id": str(evento.company_id),
                    "event_type": evento.event_type,
                    "payload": evento.payload,
                },
            )

            event_bus.dispatch(evento)

            repositorio.marcar_como_concluido(evento)
            db.commit()
            processados += 1
        except Exception:
            db.rollback()
            repositorio.incrementar_tentativa(evento)
            db.commit()

    return processados
