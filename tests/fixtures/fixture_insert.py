# # fixture do alert
# from datetime import datetime

# import pytest

# from app import db
# from app.routers import Alert, AlertType, Parameter, ParameterType, Station


# @pytest.fixture
# def station():
#     station = Station(name="Estação 1", location="Local 1")
#     db.session.add(station)
#     db.session.commit()
#     yield station
#     db.session.delete(station)
#     db.session.commit()


# @pytest.fixture
# def alert_type():
#     alert_type = AlertType(
#         name="Temperatura Alta",
#         value=30,
#         math_signal="gt",
#         status="active",
#         is_active=True,
#         create_date=datetime.utcnow(),
#         last_update=datetime.utcnow(),
#     )
#     db.session.add(alert_type)
#     db.session.commit()
#     yield alert_type
#     db.session.delete(alert_type)
#     db.session.commit()


# @pytest.fixture
# def alert(alert_type, station):
#     alert = Alert(
#         alert_type_id=alert_type.id,
#         station_id=station.id,
#         measure_value=35,
#         create_date=datetime.utcnow(),
#     )
#     db.session.add(alert)
#     db.session.commit()
#     yield alert
#     db.session.delete(alert)
#     db.session.commit()


# # fixture parameter_type
# @pytest.fixture
# def parameter_type_ativo():
#     """Cria um tipo de parâmetro ativo para os testes."""
#     tipo = ParameterType(
#         name="Temperatura",
#         measure_unit="°C",
#         qnt_decimals=2,
#         offset=None,
#         factor=1.0,
#         is_active=True,
#     )
#     db.session.add(tipo)
#     db.session.commit()
#     yield tipo
#     db.session.delete(tipo)
#     db.session.commit()


# @pytest.fixture
# def parameter_type_inativo():
#     """Cria um tipo de parâmetro inativo."""
#     tipo = ParameterType(
#         name="Pressão",
#         measure_unit="Pa",
#         qnt_decimals=1,
#         offset=0.0,
#         factor=1.2,
#         is_active=False,
#     )
#     db.session.add(tipo)
#     db.session.commit()
#     yield tipo
#     db.session.delete(tipo)
#     db.session.commit()


# @pytest.fixture
# def parameter_type_nao_existente_id():
#     """Retorna um ID que não existe no banco."""
#     return 99999


# # fixture station
# @pytest.fixture
# def setup_station():
#     parameter_type_1 = ParameterType(
#         name="Temperatura", measure_unit="°C", qnt_decimals=2, offset=None, factor=1.0
#     )
#     parameter_type_2 = ParameterType(
#         name="Pressão", measure_unit="Pa", qnt_decimals=2, offset=None, factor=1.0
#     )

#     db.session.add_all([parameter_type_1, parameter_type_2])
#     db.session.commit()

#     station = Station(
#         name="Estação Teste",
#         uid="12345-abcde",
#         latitude=-23.5505,
#         longitude=-46.6333,
#         address={"city": "São Paulo", "state": "SP", "country": "Brasil"},
#         parameter_types=[parameter_type_1.id, parameter_type_2.id],
#     )

#     db.session.add(station)
#     db.session.commit()

#     yield {"station": station, "parameter_types": [parameter_type_1, parameter_type_2]}

#     # Teardown
#     db.session.delete(station)
#     db.session.delete(parameter_type_1)
#     db.session.delete(parameter_type_2)
#     db.session.commit()


# # fixture alert_type
# @pytest.fixture
# def parameter():
#     """Cria um parâmetro válido."""
#     param = Parameter(
#         name="Temperatura", measure_unit="°C", qnt_decimals=2, offset=None, factor=1.0
#     )
#     db.session.add(param)
#     db.session.commit()
#     yield param
#     db.session.delete(param)
#     db.session.commit()


# @pytest.fixture
# def alert_type_active(parameter):
#     """Cria um tipo de alerta ativo."""
#     alert = AlertType(
#         parameter_id=parameter.id,
#         name="Temperatura alta",
#         value=30,
#         math_signal="gt",
#         status="active",
#         is_active=True,
#         create_date=datetime.now(),
#         last_update=datetime.now(),
#     )
#     db.session.add(alert)
#     db.session.commit()
#     yield alert
#     db.session.delete(alert)
#     db.session.commit()


# @pytest.fixture
# def alert_type_inactive(parameter):
#     """Cria um tipo de alerta inativo."""
#     alert = AlertType(
#         parameter_id=parameter.id,
#         name="Temperatura baixa",
#         value=10,
#         math_signal="lt",
#         status="inactive",
#         is_active=False,
#         create_date=datetime.now(),
#         last_update=datetime.now(),
#     )
#     db.session.add(alert)
#     db.session.commit()
#     yield alert
#     db.session.delete(alert)
#     db.session.commit()


# @pytest.fixture
# def parameter_not_in_db():
#     """Retorna um ID de parâmetro que não existe."""
#     return 99999

from datetime import datetime

import pytest

from app.core import db
from app.core.models.db_model import Alert, AlertType, Parameter, ParameterType, Station


class TestDataFixtures:
    """Classe que agrupa todas as fixtures usadas nos testes."""

    @staticmethod
    @pytest.fixture
    def parameter():
        param = Parameter(
            name="Temperatura", measure_unit="°C", qnt_decimals=2, offset=None, factor=1.0
        )
        db.session.add(param)
        db.session.commit()
        yield param
        db.session.delete(param)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def alert_type_active(parameter):
        alert = AlertType(
            parameter_id=parameter.id,
            name="Temperatura alta",
            value=30,
            math_signal="gt",
            status="active",
            is_active=True,
            create_date=datetime.now(),
            last_update=datetime.now(),
        )
        db.session.add(alert)
        db.session.commit()
        yield alert
        db.session.delete(alert)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def alert_type_inactive(parameter):
        alert = AlertType(
            parameter_id=parameter.id,
            name="Temperatura baixa",
            value=10,
            math_signal="lt",
            status="inactive",
            is_active=False,
            create_date=datetime.now(),
            last_update=datetime.now(),
        )
        db.session.add(alert)
        db.session.commit()
        yield alert
        db.session.delete(alert)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def alert(alert_type_active, station):
        alert = Alert(
            alert_type_id=alert_type_active.id,
            station_id=station.id,
            measure_value=35,
            create_date=datetime.utcnow(),
        )
        db.session.add(alert)
        db.session.commit()
        yield alert
        db.session.delete(alert)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def station():
        station = Station(name="Estação 1", location="Local 1")
        db.session.add(station)
        db.session.commit()
        yield station
        db.session.delete(station)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def alert_type():
        alert_type = AlertType(
            name="Temperatura Alta",
            value=30,
            math_signal="gt",
            status="active",
            is_active=True,
            create_date=datetime.utcnow(),
            last_update=datetime.utcnow(),
        )
        db.session.add(alert_type)
        db.session.commit()
        yield alert_type
        db.session.delete(alert_type)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def parameter_type_ativo():
        tipo = ParameterType(
            name="Temperatura",
            measure_unit="°C",
            qnt_decimals=2,
            offset=None,
            factor=1.0,
            is_active=True,
        )
        db.session.add(tipo)
        db.session.commit()
        yield tipo
        db.session.delete(tipo)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def parameter_type_inativo():
        tipo = ParameterType(
            name="Pressão",
            measure_unit="Pa",
            qnt_decimals=1,
            offset=0.0,
            factor=1.2,
            is_active=False,
        )
        db.session.add(tipo)
        db.session.commit()
        yield tipo
        db.session.delete(tipo)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def parameter_type_nao_existente_id():
        return 99999

    @staticmethod
    @pytest.fixture
    def setup_station(parameter_type_ativo, parameter_type_inativo):
        parameter_type_1 = parameter_type_ativo
        parameter_type_2 = parameter_type_inativo

        station = Station(
            name="Estação Teste",
            uid="12345-abcde",
            latitude=-23.5505,
            longitude=-46.6333,
            address={"city": "São Paulo", "state": "SP", "country": "Brasil"},
            parameter_types=[parameter_type_1.id, parameter_type_2.id],
        )

        db.session.add(station)
        db.session.commit()

        yield {"station": station, "parameter_types": [parameter_type_1, parameter_type_2]}

        db.session.delete(station)
        db.session.delete(parameter_type_1)
        db.session.delete(parameter_type_2)
        db.session.commit()

    @staticmethod
    @pytest.fixture
    def parameter_not_in_db():
        return 99999
