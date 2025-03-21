from typing import Optional

from pydantic import BaseModel


class AlertTypeCreate(BaseModel):
    parameter_id:  int | None = None
    name: str
    value: int
    math_signal: str
    status: str | None = None

class AlertTypeUpdate(BaseModel):
    name: Optional[str]
    value: Optional[int]
    math_signal: Optional[str]
    status: Optional[str]
    
class AlertTypeResponse(BaseModel):
    id: int
    parameter_id: int | None = None
    name: str
    value: int
    math_signal: str
    status: str | None
    is_active: bool
    create_date: str
    last_update: str 

    model_config = {
        "from_attributes": True,
    }
    

