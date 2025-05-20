from pydantic import BaseModel


class StationHistoryItem(BaseModel):
    title: str
    value: float
    measure_unit: str
    measure_date: int
    type: str 


class AlertTypeDistributionItem(BaseModel):
    name: str
    total: int


class AlertCounts(BaseModel):
    R: int
    Y: int
    G: int


class StationStatus(BaseModel):
    total: int
    active: int


class MeasuresStatusItem(BaseModel):
    label: str
    number: int
