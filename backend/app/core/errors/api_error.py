from datetime import datetime, timezone

from app.core.errors.error_codes import ErrorCode


class APIError(Exception):
    def __init__(
        self,
        *,
        codigo: ErrorCode | str,
        mensagem: str,
        status_code: int,
    ) -> None:
        super().__init__(mensagem)
        self.codigo = codigo.value if isinstance(codigo, ErrorCode) else codigo
        self.mensagem = mensagem
        self.status_code = status_code

    @staticmethod
    def _utc_iso_timestamp() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {
            "erro": {
                "codigo": self.codigo,
                "mensagem": self.mensagem,
                "timestamp": self._utc_iso_timestamp(),
            }
        }
