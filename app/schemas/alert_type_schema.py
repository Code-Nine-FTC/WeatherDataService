from pydantic import BaseModel
from typing import Optional


class AlertTypeCreate(BaseModel):
    parameter_id: Optional[int] = None
    name: str
    value: int
    math_signal: str
