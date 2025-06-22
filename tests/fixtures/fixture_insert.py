# -- coding: utf-8 --

from datetime import datetime, timezone
from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_model import (
    Alert,
    Measures,
    Parameter,
    ParameterType,
    TypeAlert,
    WeatherStation,
)


@pytest_asyncio.fixture
async def parameter_types_fixture(
    db_session: AsyncSession,
) -> AsyncGenerator[list[ParameterType], None]:
    param1 = ParameterType(
        name="Temperatura",
        detect_type="climate",
        measure_unit="°C",
        qnt_decimals=2,
        offset=0.0,
        factor=1.0,
        is_active=True,
    )
    param2 = ParameterType(
        name="Umidade",
        detect_type="climate",
        measure_unit="%",
        qnt_decimals=1,
        offset=0.0,
        factor=1.0,
        is_active=True,
    )
    param3 = ParameterType(
        name="Pressão",
        detect_type="climate",
        measure_unit="hPa",
        qnt_decimals=0,
        offset=0.0,
        factor=1.0,
        is_active=False,
    )
    db_session.add_all([param1, param2, param3])
    await db_session.commit()
    yield [param1, param2]
    await db_session.delete(param1)
    await db_session.delete(param2)
    await db_session.delete(param3)
    await db_session.commit()


@pytest_asyncio.fixture
async def weather_stations_fixture(
    db_session: AsyncSession,
) -> AsyncGenerator[list[WeatherStation], None]:
    stations = []
    new_stations = [
        {
            "name": "Estação Meteorológica Central",
            "uid": "station-0001",
            "address": {"city": "São Paulo", "state": "SP", "country": "Brasil"},
            "latitude": -23.5505,
            "longitude": -46.6333,
            "is_active": True,
        },
        {
            "name": "Estação Meteorológica Norte",
            "uid": "station-0002",
            "address": {"city": "Rio de Janeiro", "state": "RJ", "country": "Brasil"},
            "latitude": -22.9068,
            "longitude": -43.1729,
            "is_active": True,
        },
        {
            "name": "Estação Meteorológica Sul",
            "uid": "station-0003",
            "address": {"city": "Belo Horizonte", "state": "MG", "country": "Brasil"},
            "latitude": -19.9167,
            "longitude": -43.9345,
            "is_active": False,
        },
    ]

    for station_data in new_stations:
        station = await db_session.execute(
            select(WeatherStation).where(WeatherStation.uid == station_data["uid"])
        )
        station = station.scalar_one_or_none()
        if station:
            stations.append(station)
        else:
            station_data = WeatherStation(**station_data)  # noqa: PLW2901
            db_session.add(station_data)
            await db_session.flush()
            await db_session.commit()
            stations.append(station_data)

    yield stations
    for station in stations:
        await db_session.delete(station)
        await db_session.commit()


@pytest_asyncio.fixture
async def parameters_fixture(
    db_session: AsyncSession,
    weather_stations_fixture: list[WeatherStation],
    parameter_types_fixture: list[ParameterType],
) -> AsyncGenerator[list[Parameter], None]:
    list_parameters = []
    parameters = [
        {
            "parameter_type_id": parameter_types_fixture[0].id,
            "station_id": weather_stations_fixture[0].id,
            "is_active": True,
        },
        {
            "parameter_type_id": parameter_types_fixture[1].id,
            "station_id": weather_stations_fixture[1].id,
            "is_active": True,
        },
    ]
    for param_data in parameters:
        param = await db_session.execute(
            select(Parameter).where(
                Parameter.parameter_type_id == param_data["parameter_type_id"],
                Parameter.station_id == param_data["station_id"],
            )
        )
        param = param.scalar_one_or_none()
        if not param:
            param = Parameter(**param_data)
            db_session.add(param)
            await db_session.flush()
            await db_session.commit()
            list_parameters.append(param)
        else:
            list_parameters.append(param)
    yield list_parameters
    for param in list_parameters:
        await db_session.delete(param)
        await db_session.commit()


@pytest_asyncio.fixture
async def type_alerts_fixture(
    db_session: AsyncSession,
    parameters_fixture: list[Parameter],
) -> AsyncGenerator[list[TypeAlert], None]:
    new_type_alerts = [
        {
            "parameter_id": parameters_fixture[0].id,
            "name": "Alerta de Temperatura",
            "value": 30,
            "math_signal": ">",
            "is_active": True,
            "status": "A",
        },
        {
            "parameter_id": parameters_fixture[1].id,
            "name": "Alerta de Umidade",
            "value": 70,
            "math_signal": "<",
            "is_active": True,
            "status": "A",
        },
    ]
    type_alerts = []
    for alert_data in new_type_alerts:
        type_alert = await db_session.execute(
            select(TypeAlert).where(
                TypeAlert.parameter_id == alert_data["parameter_id"],
                TypeAlert.name == alert_data["name"],
            )
        )
        type_alert = type_alert.scalar_one_or_none()
        if not type_alert:
            type_alert = TypeAlert(**alert_data)
            db_session.add(type_alert)
            await db_session.flush()
            await db_session.commit()
            type_alerts.append(type_alert)
        else:
            type_alerts.append(type_alert)
    yield type_alerts
    for type_alert in type_alerts:
        await db_session.delete(type_alert)
        await db_session.commit()


@pytest_asyncio.fixture
async def measures_fixture(
    db_session: AsyncSession,
    parameters_fixture: list[Parameter],
) -> AsyncGenerator[list[Measures], None]:
    measures = []
    new_measures = [
        {
            "parameter_id": parameters_fixture[0].id,
            "value": 25.5,
            "measure_date": int(datetime.now(timezone.utc).timestamp()),
        },
        {
            "parameter_id": parameters_fixture[1].id,
            "value": 60.0,
            "measure_date": int(datetime.now(timezone.utc).timestamp()),
        },
    ]

    for measure_data in new_measures:
        measure = await db_session.execute(
            select(Measures).where(
                Measures.parameter_id == measure_data["parameter_id"],
                Measures.measure_date == measure_data["measure_date"],
            )
        )
        measure = measure.scalar_one_or_none()
        if measure:
            measures.append(measure)
        else:
            measure_obj = Measures(**measure_data)
            db_session.add(measure_obj)
            await db_session.flush()
            await db_session.commit()
            measures.append(measure_obj)

    yield measures
    for measure in measures:
        await db_session.delete(measure)
        await db_session.commit()


@pytest_asyncio.fixture
async def alerts_fixture(
    db_session: AsyncSession,
    type_alerts_fixture: list[TypeAlert],
    measures_fixture: list[Measures],
) -> AsyncGenerator[list[Alert], None]:
    alert1 = Alert(
        type_alert_id=type_alerts_fixture[0].id,
        measure_id=measures_fixture[0].id,
        create_date=int(datetime.now(timezone.utc).timestamp()),
        is_read=False,
    )
    alert2 = Alert(
        type_alert_id=type_alerts_fixture[1].id,
        measure_id=measures_fixture[1].id,
        create_date=int(datetime.now(timezone.utc).timestamp()),
        is_read=False,
    )
    db_session.add_all([alert1, alert2])
    await db_session.commit()
    yield [alert1, alert2]
    await db_session.delete(alert1)
    await db_session.delete(alert2)
    await db_session.commit()
