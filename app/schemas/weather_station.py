from pydantic import BaseModel, field_serializer, field_validator, ConfigDict, model_serializer
from datetime import datetime
from typing import Optional

class WeatherStationBase(BaseModel):
	name: str
	uid: str
	address: list[str]
	latitude: float
	longitude: float
	create_date: datetime 
	is_active: bool

	@field_validator('create_date', mode='before')
	def parse_create_date(cls, value):
		if isinstance(value, str):
			return datetime.fromisoformat(value)
		return value

class WeatherStationCreate(WeatherStationBase):
	pass

class WeatherStationUpdate(BaseModel):
	name: str | None = None
	uid: str | None = None
	address: list[str] | None = None
	latitude: float | None = None
	longitude: float | None = None
	is_active: bool | None = None

class WeatherStationResponse(WeatherStationBase):
	id: int
	model_config = ConfigDict(from_attributes=True)
