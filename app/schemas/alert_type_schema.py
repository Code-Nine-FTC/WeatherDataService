from pydantic import BaseModel


class AlertTypeCreate(BaseModel):
    parameter_id: int
    name: str
    value: int
    math_signal: str
