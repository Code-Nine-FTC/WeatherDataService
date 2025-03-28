from typing import Optional

from pydantic import BaseModel


class ParameterTypeResponse(BaseModel):
    measure_unit: str
    qnt_decimals: int
    offset: Optional[int] = None
    factor: Optional[int] = None
    name: str
