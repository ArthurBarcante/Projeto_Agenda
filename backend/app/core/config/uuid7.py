from __future__ import annotations

from uuid import UUID
from uuid import uuid4

try:
    from uuid import uuid7 as _stdlib_uuid7
except ImportError:  # pragma: no cover
    _stdlib_uuid7 = None

if _stdlib_uuid7 is None:  # pragma: no cover
    try:
        from uuid6 import uuid7 as _external_uuid7
    except ImportError:
        _external_uuid7 = None


def generate_uuid7() -> UUID:
    if _stdlib_uuid7 is not None:
        return _stdlib_uuid7()
    if _external_uuid7 is not None:
        return _external_uuid7()
    return uuid4()


def gerar_uuid7() -> UUID:
    return generate_uuid7()
