import pytest
from fastapi.testclient import TestClient
from app.core.models.db_model import WeatherStation
from datetime import datetime
from tests.fixtures.fixture_insert import setup_station
from tests.fixtures.fixture_insert import db_session


HTTP_STATUS_OK = 200
HTTP_STATUS_CONFLICT = 409
HTTP_STATUS_UNPROCESSABLE = 422
HTTP_STATUS_NOT_FOUND = 404


class TestStation:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient, setup_station):
        self.client = authenticated_client
        self.station = setup_station["station"]
        self.param_types = setup_station["parameter_types"]

    # 1. POST - Criação de estação não precisa de fixture
    def test_create_station(self):
        data = {
            "name": "Estação Nova",
            "uid": "nova-uid-123",
            "latitude": -10.0,
            "longitude": -50.0,
            "address": {"city": "Cuiabá", "state": "MT", "country": "Brasil"},
            "parameter_types": [pt.id for pt in self.param_types],
        }
        response = self.client.post("/stations/", json=data)
        assert response.status_code == HTTP_STATUS_OK

    # 2. POST - UID existente precisa de uma fixture com uma estação cadastrada, e nessa função precisa passar o mesmo uid
    def test_create_station_with_existing_uid(self):
        # A estação já existe por conta da fixture setup_station, que cria a estação
        data = {
            "name": "Repetida",
            "uid": self.station.uid,  # Usando o mesmo UID da estação criada na fixture
            "latitude": -22.0,
            "longitude": -44.0,
            "address": {"city": "SP", "state": "SP", "country": "Brasil"},
            "parameter_types": [pt.id for pt in self.param_types],
        }
        response = self.client.post("/stations/", json=data)
        assert response.status_code == HTTP_STATUS_CONFLICT

    # 3. POST - Campos ausentes não precisa de fixture
    def test_create_station_with_missing_fields(self):
        data = {"name": "Incompleta"}
        response = self.client.post("/stations/", json=data)
        assert response.status_code == HTTP_STATUS_UNPROCESSABLE

    # 4. POST - Com tipos de parâmetros e checagem de vínculo não precisa de fixture
    def test_create_station_with_parameters_and_verify_link(self):
        data = {
            "name": "Vinculada",
            "uid": "com-parametro",
            "latitude": -25.0,
            "longitude": -45.0,
            "address": {"city": "Joinville", "state": "SC", "country": "Brasil"},
            "parameter_types": [pt.id for pt in self.param_types],
        }
        response = self.client.post("/stations/", json=data)
        assert response.status_code == HTTP_STATUS_OK

        response = self.client.get("/stations/filters", params={"uid": "com-parametro"})
        data = response.json()["data"][0]
        assert len(data["parameters"]) == len(self.param_types)

    # 5. GET - Lista estações precisa de fixture para ter algo para listar
    def test_list_stations(self):
        response = self.client.get("/stations/filters")
        assert response.status_code == HTTP_STATUS_OK
        assert isinstance(response.json()["data"], list)

    # 6. GET - Lista com filtros precisa de fixture para ter algo para filtrar
    def test_list_stations_with_filters(self):
        response = self.client.get(
            "/stations/filters",
            params={"uid": self.station.uid, "name": self.station.name, "status": True},
        )
        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        assert len(data) > 0

    # 7. GET - Parâmetro por ID precisa de fixture para ter algo para buscar
    def test_get_parameter_by_valid_type_id(self):
        param_id = self.param_types[0].id
        response = self.client.get(f"/stations/parameters/{param_id}")
        assert response.status_code == HTTP_STATUS_OK

    # 8. GET - Parâmetro inexistente não precisa de fixture
    def test_get_parameter_by_invalid_type_id(self):
        response = self.client.get("/stations/parameters/99999")
        assert response.status_code == HTTP_STATUS_NOT_FOUND

    # 9. GET - Estação por ID precisa de fixture para ter algo para buscar
    def test_get_station_by_id(self):
        response = self.client.get(f"/stations/{self.station.id}")
        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        assert data["uid"] == self.station.uid

    # 10. GET - Estação inexistente não precisa de fixture
    def test_get_station_by_invalid_id(self):
        response = self.client.get("/stations/99999")
        assert response.status_code == HTTP_STATUS_NOT_FOUND

    # 11. PATCH - Atualizar estação com parâmetros precisa de fixture para ter algo para atualizar
    def test_update_station_with_new_parameters(self):
        data = {
            "name": "Estação Atualizada",
            "parameter_types": [self.param_types[1].id],
            "latitude": -20.0,
            "longitude": -50.0,
            "address": {"city": "Floripa", "state": "SC", "country": "Brasil"},
        }
        response = self.client.patch(f"/stations/{self.station.id}", json=data)
        assert response.status_code == HTTP_STATUS_OK

    # 12. PATCH - Atualizar com ID inválido não precisa de fixture
    def test_update_station_invalid_id(self):
        data = {"name": "Falha"}
        response = self.client.patch("/stations/99999", json=data)
        assert response.status_code == HTTP_STATUS_NOT_FOUND

    # 13. PATCH - Remover parâmetros precisa de fixture para poder remover o parametro
    def test_remove_parameter_from_station_and_check_cleanup(self):
        # Remove um parâmetro da estação
        param_id = self.param_types[1].id
        response = self.client.patch(f"/stations/{self.station.id}/parameter/{param_id}")
        assert response.status_code == HTTP_STATUS_OK

        # Confere se ele não aparece mais no GET da estação
        response = self.client.get(f"/stations/{self.station.id}")
        data = response.json()["data"]
        param_ids = [p["id"] for p in data["parameters"]]
        assert param_id not in param_ids
