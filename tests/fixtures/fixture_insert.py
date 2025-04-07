# fixture do alert
import pytest
from app import db
from app.routers import Alert, AlertType, Station
from datetime import datetime


@pytest.fixture(autouse=True)
def setup_alert_data():
    alert_type = AlertType(
        name="Temperatura Alta", value=30, math_signal="gt", status="active"
    )
    db.session.add(alert_type)
    db.session.commit()

    station = Station(name="Estação 1", location="Local 1")
    db.session.add(station)
    db.session.commit()

    alert = Alert(
        alert_type_id=alert_type.id,
        station_id=station.id,
        measure_value=35,
        create_date=datetime.utcnow(),
    )
    db.session.add(alert)
    db.session.commit()

    yield alert

    db.session.delete(alert)
    db.session.delete(station)
    db.session.delete(alert_type)
    db.session.commit()

    # fixture parameter


import pytest
from app import db
from app.routers import ParameterType
from datetime import datetime


@pytest.fixture(autouse=True)
def setup_parameter_type():
    parameter_type_data = {
        "name": "Temperatura",
        "measure_unit": "°C",
        "qnt_decimals": 2,
        "offset": None,
        "factor": 1.0,
    }

    parameter_type = ParameterType(**parameter_type_data)
    db.session.add(parameter_type)
    db.session.commit()

    yield parameter_type

    db.session.delete(parameter_type)
    db.session.commit()


# fixture do station
import pytest
from app import db
from app.routers import Station, ParameterType
from datetime import datetime


@pytest.fixture(autouse=True)
def setup_station():
    parameter_type_1 = ParameterType(
        name="Temperatura", measure_unit="°C", qnt_decimals=2, offset=None, factor=1.0
    )
    parameter_type_2 = ParameterType(
        name="Pressão", measure_unit="Pa", qnt_decimals=2, offset=None, factor=1.0
    )

    db.session.add(parameter_type_1)
    db.session.add(parameter_type_2)
    db.session.commit()

    station_data = {
        "name": "Estação Teste",
        "uid": "12345-abcde",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "address": {"city": "São Paulo", "state": "SP", "country": "Brasil"},
        "parameter_types": [parameter_type_1.id, parameter_type_2.id],
    }

    station = Station(
        name=station_data["name"],
        uid=station_data["uid"],
        latitude=station_data["latitude"],
        longitude=station_data["longitude"],
        address=station_data["address"],
        parameter_types=station_data["parameter_types"],
    )

    db.session.add(station)
    db.session.commit()

    yield station

    db.session.delete(station)
    db.session.delete(parameter_type_1)
    db.session.delete(parameter_type_2)
    db.session.commit()


# fixture do alert_type
import pytest
from app import db
from app.routers import AlertType, Parameter
from datetime import datetime


@pytest.fixture(autouse=True)
def setup_alert_type():
    parameter = Parameter(
        name="Temperatura", measure_unit="°C", qnt_decimals=2, offset=None, factor=1.0
    )
    db.session.add(parameter)
    db.session.commit()

    alert_type_data = {
        "parameter_id": parameter.id,
        "name": "Temperatura alta",
        "value": 30,
        "math_signal": "gt",
        "status": "active",
    }

    alert_type = AlertType(
        parameter_id=alert_type_data["parameter_id"],
        name=alert_type_data["name"],
        value=alert_type_data["value"],
        math_signal=alert_type_data["math_signal"],
        status=alert_type_data["status"],
        create_date=datetime.now(),
        last_update=datetime.now(),
    )

    db.session.add(alert_type)
    db.session.commit()

    yield alert_type, parameter

    db.session.delete(alert_type)
    db.session.delete(parameter)
    db.session.commit()
