# -*- coding: utf-8 -*-
from pydantic import BaseModel


class AlertTypeCreate(BaseModel):
    parameter_id: int | None = None
    name: str
    value: int
    math_signal: str
    status: str | None = None

class AlertTypeUpdate(BaseModel):
    parameter_id: Optional[int] = None
    name: Optional[str] = None
    value: Optional[int] = None
    math_signal: Optional[str] = None   
    status: Optional[str] = None
    is_active: Optional[bool] = None
    
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
    

