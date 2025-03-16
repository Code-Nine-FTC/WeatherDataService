from pydantic import BaseModel


class AlertTypeCreate(BaseModel):
    name: str
    value: int
    math_signal: str
    status: str


class AlertTypeResponse(BaseModel):
    id: int
    name: str
    value: int
    math_signal: str
    create_date: int
    last_update: int
    status: str
