from gzip import decompress
from json import loads
from typing import Any


def deserialize(ser_type: str, binary: bytes) -> Any:
    if ser_type == 'json':
        return loads(binary.decode())
    if ser_type == 'cjson':
        decompressed = decompress(binary)
        data = decompressed.decode()
        return loads(data)
    

__all__ = [
    'deserialize'
]