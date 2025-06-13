from datetime import datetime, timezone
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_model import Alert, ParameterType, TypeAlert, WeatherStation


@pytest.fixture
async def parameter_types_fixture(db_session: AsyncSession):
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
    db_session.add_all([param1, param2])
    await db_session.commit()
    yield [param1, param2]
    await db_session.delete(param1)
    await db_session.delete(param2)
    await db_session.commit()


@pytest.fixture
async def station_with_existing_uid_fixture(db_session: AsyncSession, parameter_types_fixture):
    station = WeatherStation(
        name="Estação Existente",
        uid="uid-existente",
        latitude=-10.0,
        longitude=-50.0,
        address={"city": "Cuiabá", "state": "MT", "country": "Brasil"},
        create_date=int(datetime.now(timezone.utc).timestamp()),
        is_active=True,
    )
    station.parameter_types = parameter_types_fixture
    db_session.add(station)
    await db_session.commit()
    yield {"station": station, "parameter_types": parameter_types_fixture}
    await db_session.delete(station)
    await db_session.commit()


@pytest.fixture
async def full_station_fixture(db_session: AsyncSession, parameter_types_fixture):
    station = WeatherStation(
        name="Estação Completa",
        uid="uid-completo",
        latitude=-15.0,
        longitude=-45.0,
        address={"city": "Brasília", "state": "DF", "country": "Brasil"},
        create_date=int(datetime.now(timezone.utc).timestamp()),
        is_active=True,
    )
    station.parameter_types = parameter_types_fixture
    db_session.add(station)
    await db_session.commit()
    yield {"station": station, "parameter_types": parameter_types_fixture}
    await db_session.delete(station)
    await db_session.commit()


@pytest.fixture
async def parameter_type_ativo(
    db_session: AsyncSession,
) -> AsyncGenerator[ParameterType, None]:
    param = ParameterType(
        name="Temperatura",
        detect_type="climate",
        measure_unit="°C",
        qnt_decimals=2,
        offset=0.0,
        factor=1.0,
        is_active=True,
    )
    db_session.add(param)
    await db_session.commit()
    await db_session.refresh(param)
    yield param
    await db_session.delete(param)
    await db_session.commit()


@pytest.fixture
async def alert_type_fixture(
    db_session: AsyncSession, parameter_type_ativo: ParameterType
) -> AsyncGenerator[TypeAlert, None]:
    alert_type = TypeAlert(
        parameter_id=parameter_type_ativo.id,
        name="Alerta Ativo",
        value=30,
        math_signal=">",
        status="active",
        is_active=True,
        create_date=datetime.now(timezone.utc),
        last_update=datetime.now(timezone.utc),
    )
    db_session.add(alert_type)
    await db_session.commit()
    await db_session.refresh(alert_type)
    yield alert_type
    await db_session.delete(alert_type)
    await db_session.commit()


@pytest.fixture
async def alert_station_fixture(
    db_session: AsyncSession, parameter_types_fixture
) -> AsyncGenerator[WeatherStation, None]:
    station = WeatherStation(
        name="Estação 1",
        uid="alert-uid",
        latitude=-20.0,
        longitude=-40.0,
        address={"city": "Vitória", "state": "ES", "country": "Brasil"},
        create_date=int(datetime.now(timezone.utc).timestamp()),
        is_active=True,
    )
    station.parameter_types = parameter_types_fixture
    db_session.add(station)
    await db_session.commit()
    await db_session.refresh(station)
    yield station
    await db_session.delete(station)
    await db_session.commit()


@pytest.fixture
async def alert_fixture(
    db_session: AsyncSession,
    alert_station_fixture: WeatherStation,
    alert_type_fixture: TypeAlert,
) -> AsyncGenerator[Alert, None]:
    alert = Alert(
        station_id=alert_station_fixture.id,
        type_alert_id=alert_type_fixture.id,
        measure_value="35",
        create_date=datetime.now(timezone.utc),
    )
    db_session.add(alert)
    await db_session.commit()
    await db_session.refresh(alert)
    yield alert
    await db_session.delete(alert)
    await db_session.commit()
