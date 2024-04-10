from pydantic import BaseModel


class CreatedModel(BaseModel):
    created_id: int


__all__ = [
    'CreatedModel'
]