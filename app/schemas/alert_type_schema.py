from typing import Optional

from pydantic import BaseModel


class AlertTypeCreate(BaseModel):
    parameter_id:  int | None = None
    name: str
    value: int
    math_signal: str
