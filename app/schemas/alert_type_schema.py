from pydantic import BaseModel


class AlertTypeCreate(BaseModel):
    parameter_id: int
    name: str
    value: int
    math_signal: str


class AlertTypeResponse(BaseModel):
    id: int
    name: str
    value: int
    math_signal: str
    create_date: int
    last_update: int
    status: str
