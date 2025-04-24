from pydantic import BaseModel


class StationHistoryItem(BaseModel):
    name: str
    value: float
    measure_unit: str
    measure_date: int


class AlertTypeDistributionItem(BaseModel):
    name: str
    total: int


class AlertCounts(BaseModel):
    R: int
    Y: int
    G: int


class StationStatus(BaseModel):
    total: int
    inactive: int


class MeasuresStatusItem(BaseModel):
    label: str
    number: int
