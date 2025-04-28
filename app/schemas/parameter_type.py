from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ParameterTypeResponse(BaseModel):
    id: int
    detect_type: str
    measure_unit: str
    qnt_decimals: int
    offset: float | None = None
    factor: float | None = None
    name: str
    is_active: bool

    model_config = {
        "from_attributes": True,
    }


class CreateParameterType(BaseModel):
    name: str
    detect_type: str
    measure_unit: str
    qnt_decimals: int
    offset: float | None = None
    factor: float | None = None


class FilterParameterType(BaseModel):
    name: str | None = None
    is_active: bool | None = True


class UpdateParameterType(BaseModel):
    name: str | None = None
    measure_unit: str | None = None
    qnt_decimals: int | None = None
    offset: float | None = None
    factor: float | None = None
    json_data: dict[str, Any] | None = None
    is_active: bool | None = None
    last_update: datetime = datetime.now()
