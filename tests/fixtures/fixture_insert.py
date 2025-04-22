from datetime import datetime, timezone
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_model import Alert, Parameter, ParameterType, TypeAlert, WeatherStation
from app.dependency.database import Database

# ============================================
# Fixtures de sessão assíncrona
# ============================================

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with Database().session as session:
        yield session

# ============================================
# Fixtures de Parâmetros
# ============================================

@pytest.fixture
async def parameter(db_session: AsyncSession, parameter_type_ativo: ParameterType):
    param = Parameter(
        name="Temperatura",
        measure_unit="°C",
        qnt_decimals=2,
        offset=None,
        factor=1.0,
        parameter_type_id=parameter_type_ativo.id,  # Correção: associando corretamente o parameter_type_id
    )
    db_session.add(param)
    await db_session.commit()
    yield param
    await db_session.delete(param)
    await db_session.commit()

@pytest.fixture
def parameter_not_in_db():
    return 999999

@pytest.fixture
async def parameter_type_ativo(db_session: AsyncSession):
    param_type = ParameterType(
        name="Temperatura",
        detect_type="climate",
        measure_unit="°C",
        qnt_decimals=2,
        offset=0.0,
        factor=1.0,
        is_active=True,
    )
    db_session.add(param_type)
    await db_session.commit()
    yield param_type
    await db_session.delete(param_type)
    await db_session.commit()

@pytest.fixture
def parameter_type_nao_existente_id():
    return 999999

# ============================================
# Fixtures de Tipos de Alerta
# ============================================

@pytest.fixture
async def type_alert_active(db_session: AsyncSession, parameter):
    alert = TypeAlert(
        parameter_id=parameter.id,
        name="Alerta Ativo",
        value=50,
        math_signal="gt",
        status="active",
        is_active=True,
    )
    db_session.add(alert)
    await db_session.commit()
    yield alert
    await db_session.delete(alert)
    await db_session.commit()

@pytest.fixture
async def type_alert_inactive(db_session: AsyncSession, parameter):
    alert = TypeAlert(
        parameter_id=parameter.id,
        name="Alerta Inativo",
        value=30,
        math_signal="lt",
        status="inactive",
        is_active=False,
    )
    db_session.add(alert)
    await db_session.commit()
    yield alert
    await db_session.delete(alert)
    await db_session.commit()

# ============================================
# Fixtures de Estações Meteorológicas
# ============================================

@pytest.fixture
async def weather_station(db_session: AsyncSession, parameter_type_ativo):
    station = WeatherStation(
        name="Estação Teste",
        uid="test-uid-123",
        latitude=-23.5505,
        longitude=-46.6333,
        address={"city": "São Paulo", "state": "SP", "country": "Brasil"},
        create_date=int(datetime.now(timezone.utc).timestamp()),
        is_active=True,
    )
    # Associando corretamente os tipos de parâmetros à estação
    station.parameter_types = [parameter_type_ativo]
    db_session.add(station)
    await db_session.commit()
    yield station
    await db_session.delete(station)
    await db_session.commit()

@pytest.fixture
async def setup_station(db_session: AsyncSession):
    # Criando dois tipos de parâmetros
    param_type_1 = ParameterType(
        name="Temperatura",
        detect_type="climate",
        measure_unit="°C",
        qnt_decimals=2,
        offset=0.0,
        factor=1.0,
        is_active=True,
    )
    param_type_2 = ParameterType(
        name="Umidade",
        detect_type="climate",
        measure_unit="%",
        qnt_decimals=1,
        offset=0.0,
        factor=1.0,
        is_active=True,
    )
    db_session.add_all([param_type_1, param_type_2])
    await db_session.commit()

    # Criando a estação meteorológica
    station = WeatherStation(
        name="Estação Teste",
        uid="test-uid-123",
        latitude=-10.0,
        longitude=-50.0,
        address={"city": "Cuiabá", "state": "MT", "country": "Brasil"},
        create_date=int(datetime.now(timezone.utc).timestamp()),
        is_active=True,
    )

    # Associando os tipos de parâmetros à estação
    station.parameter_types = [param_type_1, param_type_2]

    db_session.add(station)
    await db_session.commit()

    # Retornando a estação e os tipos de parâmetros
    yield {"station": station, "parameter_types": [param_type_1, param_type_2]}

    # Cleanup: deletando a estação e os tipos de parâmetros
    await db_session.delete(station)
    await db_session.delete(param_type_1)
    await db_session.delete(param_type_2)
    await db_session.commit()

# ============================================
# Fixtures de Alertas
# ============================================

@pytest.fixture
async def alert(db_session: AsyncSession, type_alert_active, weather_station):
    alert = Alert(
        measure_value="35",
        create_date=int(datetime.now(timezone.utc).timestamp()),
        type_alert_id=type_alert_active.id,
        station_id=weather_station.id,
    )
    db_session.add(alert)
    await db_session.commit()
    yield alert
    await db_session.delete(alert)
    await db_session.commit()
