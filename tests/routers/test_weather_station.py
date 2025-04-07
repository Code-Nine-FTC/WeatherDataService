import pytest
from fastapi.testclient import TestClient
from app import app
from app.core.models.db_model import User
from app.modules.security import TokenManager
from tests.fixtures.fixture_user import fake_user


class TestStation:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient):
        self.client = authenticated_client

    def test_create_station(self):
        data = {
            "name": "Estação Teste",
            "uid": "12345-abcde",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "address": {"city": "São Paulo", "state": "SP", "country": "Brasil"},
            "parameter_types": [1, 2],
        }

        response = self.client.post("/stations/", json=data)

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_update_station(self):
        station_id = 1
        data = {
            "name": "Estação Atualizada",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "address": {"city": "São Paulo", "state": "SP", "country": "Brasil"},
            "parameter_types": [2],
        }

        response = self.client.patch(f"/stations/{station_id}", json=data)

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_get_filtered_stations(self):
        filters = {"uid": "12345-abcde", "status": True}

        response = self.client.get("/stations/filters", params=filters)

        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, list)
        if len(data) > 0:
            assert "name_station" in data[0]
            assert "uid" in data[0]

    def test_disable_station(self):
        station_id = 1
        response = self.client.patch(f"/stations/disable/{station_id}")

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_remove_parameter_from_station(self):
        station_id = 1
        parameter_id = 2
        response = self.client.patch(f"/stations/{station_id}/parameter/{parameter_id}")

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_get_station_by_id(self):
        station_id = 1
        response = self.client.get(f"/stations/{station_id}")

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name_station"] == "Estação Teste"
        assert data["uid"] == "12345-abcde"
