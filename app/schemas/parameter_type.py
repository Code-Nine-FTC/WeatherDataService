from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ParameterTypeResponse(BaseModel):
    id: int
    measure_unit: str
    qnt_decimals: int
    offset: int | None = None
    factor: int | None = None
    name: str

    model_config = {
        "from_attributes": True,
    }


class CreateParameterType(BaseModel):
    name: str
    measure_unit: str
    qnt_decimals: int
    offset: float | None = None
    factor: float | None = None


class FilterParameterType(BaseModel):
    name: str | None = None
    measure_unit: str | None = None
    is_active: bool | None = None


class UpdateParameterType(BaseModel):
    name: str | None = None
    measure_unit: str | None = None
    qnt_decimals: int | None = None
    offset: float | None = None
    factor: float | None = None
    json: dict[str, Any] | None = None
    is_active: bool | None = None
    last_update: datetime = datetime.now()
