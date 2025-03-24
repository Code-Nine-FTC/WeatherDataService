# -*- coding: utf-8 -*-
from pydantic import BaseModel
from datetime import datetime


class AlertTypeCreate(BaseModel):
    parameter_id: int | None = None
    name: str
    value: int
    math_signal: str
    status: str | None = None

class AlertTypeUpdate(BaseModel):
    parameter_id: int | None = None
    name: str | None = None
    value: int | None = None
    math_signal: str | None = None   
    status: str | None = None
    is_active: bool | None = None
    last_update: datetime = datetime.now()
    
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
    

