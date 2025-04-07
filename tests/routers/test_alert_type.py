import pytest
from fastapi.testclient import TestClient
from app import app
from app.schemas.alert_type_schema import AlertTypeCreate, AlertTypeUpdate
from tests.fixtures.fixture_user import fake_user
from app.modules.security import TokenManager


class TestAlertType:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient):
        self.client = authenticated_client

    def test_create_alert_type(self):
        alert_type_data = {
            "parameter_id": 1,
            "name": "Temperatura alta",
            "value": 30,
            "math_signal": "gt",
            "status": "active",
        }

        response = self.client.post("/alert_type/", json=alert_type_data)

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_list_alert_types(self):
        response = self.client.get("/alert_type/")

        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "name" in data[0]
            assert "value" in data[0]
            assert "math_signal" in data[0]
            assert "status" in data[0]
            assert "is_active" in data[0]
            assert "create_date" in data[0]
            assert "last_update" in data[0]

    def test_get_alert_type_by_id(self):
        alert_type_id = 1
        response = self.client.get(f"/alert_type/{alert_type_id}")

        assert response.status_code == 200
        data = response.json()["data"]
        assert "id" in data
        assert "name" in data
        assert "value" in data
        assert "math_signal" in data
        assert "status" in data
        assert "is_active" in data
        assert "create_date" in data
        assert "last_update" in data

    def test_update_alert_type(self):
        alert_type_id = 1
        alert_type_data = {
            "name": "Temperatura crítica",
            "value": 40,
            "math_signal": "gt",
            "status": "inactive",
        }

        response = self.client.patch(f"/alert_type/{alert_type_id}", json=alert_type_data)

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_delete_alert_type(self):
        alert_type_id = 1
        response = self.client.patch(f"/alert_type/disables/{alert_type_id}")

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_get_alert_type_by_id_not_found(self):
        alert_type_id = 999
        response = self.client.get(f"/alert_type/{alert_type_id}")

        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == f"Tipo de alerta com a ID {alert_type_id} não encontrado."
        )

    def test_update_alert_type_conflict(self):
        alert_type_id = 1
        alert_type_data = {
            "name": "Temperatura alta",
            "value": 25,
            "math_signal": "lt",
            "status": "inactive",
        }

        response = self.client.patch(f"/alert_type/{alert_type_id}", json=alert_type_data)

        assert response.status_code == 409
        assert response.json()["detail"] == "Tipo de alerta já cadastrado."

    def test_create_alert_type_parameter_not_found(self):
        alert_type_data = {
            "parameter_id": 999,
            "name": "Pressão baixa",
            "value": 50,
            "math_signal": "lt",
            "status": "active",
        }

        response = self.client.post("/alert_type/", json=alert_type_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Parâmetro com a ID 999 não encontrado."
