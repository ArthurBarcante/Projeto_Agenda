import logging
from typing import Any


logger = logging.getLogger(__name__)


def handle_compromisso_cancelado(_event: Any) -> None:
    logger.info("Compromisso cancelado processado")
