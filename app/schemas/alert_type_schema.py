# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel


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
    last_update: datetime | None = datetime.now()


class AlertTypeResponse(BaseModel):
    id: int
    parameter_id: int | None = None
    name: str
    value: int
    math_signal: str
    status: str | None | None
    is_active: bool
    create_date: int
    last_update: datetime

    model_config = {
        "from_attributes": True,
    }
