from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from ..core.models.db_model import WeatherStation, User
from ..schemas.weather_station import WeatherStationCreate, WeatherStationUpdate
from fastapi import HTTPException, status

class WeatherStationService:
	def __init__(self, session: AsyncSession):
		self._session = session 

	def _convert_dates(self, data: dict) -> dict:
		date_fields = ['initial_date', 'last_data', 'last_update']
		for field in date_fields:
			if field in data and isinstance(data[field], str):
				data[field] = datetime.strptime(data[field], "%Y-%m-%d")
		return data

	async def create_station(self, data: dict, user_id: int):

		result = await self._session.execute(select(User).where(User.id == user_id))
		if not result.scalar():
			raise HTTPException(status_code=404, detail="Usuário não encontrado")
		
		if 'create_date' in data:
			dt = data['create_date']
			if isinstance(dt, datetime):
				data['create_date'] = int(dt.timestamp())
			
		station_data = {
			**data,
		}
		
		new_station = WeatherStation(**station_data)
		self._session.add(new_station)
		await self._session.commit()
		return new_station

	