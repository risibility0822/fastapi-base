"""Init."""

import orjson
from typing import Any, Callable


def orjson_dumps(v: Any, *, default: Callable) -> str:
    """Orjson.dumps returns bytes to match standard json.

    Dumps we need to decode.

    Args:
        v: 要序列化的Python對象
        default: 當遇到無法序列化的對象時，會調用這個函數

    Returns:
        _type_: 序列化後的JSON字符串
    """
    return orjson.dumps(v, default=default).decode()
