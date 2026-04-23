import logging
import sys


def setup_logging() -> None:
    """Configura logging estruturado para stdout.

    Formato: [LEVEL] logger_name: mensagem
    Em produção, trocar StreamHandler por um handler compatível com
    a plataforma (ex: Render já captura stdout automaticamente).
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )

    root = logging.getLogger()
    if not root.handlers:
        root.addHandler(handler)

    root.setLevel(logging.INFO)

    # Silenciar logs verbosos de libs externas em produção
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
