import logging
from typing import Any


logger = logging.getLogger(__name__)


def handle_appointment_cancelled(_event: Any) -> None:
    logger.info("Appointment cancelled processed")


def handle_appointment_cancelled_alias(_event: Any) -> None:
    handle_appointment_cancelled(_event)
