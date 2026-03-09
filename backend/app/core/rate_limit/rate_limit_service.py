from datetime import datetime, timezone
from uuid import UUID

from redis.asyncio import Redis

from app.core.config import settings

_redis_client: Redis | None = None


def _obter_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client


def _chave_minuto_atual(company_id: UUID | str) -> str:
    minuto_atual = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
    return f"rate_limit:{company_id}:{minuto_atual}"


async def verificar_rate_limit(company_id: UUID | str) -> bool:
    redis = _obter_redis_client()
    key = _chave_minuto_atual(company_id)

    contador = await redis.incr(key)
    if contador == 1:
        await redis.expire(key, 60)

    return contador > settings.RATE_LIMIT_REQUESTS_PER_MINUTE
