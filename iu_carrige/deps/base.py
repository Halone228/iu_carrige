from abc import ABC, abstractmethod


class BaseDep(ABC):

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


__all__ = [
    'BaseDep'
]