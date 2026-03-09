import logging
from typing import Any


logger = logging.getLogger(__name__)


def handle_appointment_created(_event: Any) -> None:
    logger.info("Appointment created processed")


def handle_appointment_created_alias(_event: Any) -> None:
    handle_appointment_created(_event)
