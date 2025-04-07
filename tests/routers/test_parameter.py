import pytest
from fastapi.testclient import TestClient
from app import app
from app.schemas.parameter_type import (
    CreateParameterType,
    UpdateParameterType,
    FilterParameterType,
)
from app.service.parameter_type import ParameterTypeService
from unittest.mock import patch
from tests.fixtures.fixture_user import fake_user
from app.modules.security import TokenManager


class TestParameterType:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient):
        self.client = authenticated_client

    def test_create_parameter_type(self):
        data = {
            "name": "Temperatura",
            "measure_unit": "°C",
            "qnt_decimals": 2,
            "offset": None,
            "factor": 1.0,
        }

        response = self.client.post("/parameter_types/", json=data)

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_update_parameter_type(self):
        parameter_type_id = 1
        data = {
            "name": "Temperatura Atualizada",
            "measure_unit": "°F",
            "qnt_decimals": 1,
            "offset": 0.0,
            "factor": 1.2,
        }

        response = self.client.patch(f"/parameter_types/{parameter_type_id}/update", json=data)

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_list_parameter_types(self):
        filters = {"name": "Temperatura"}

        response = self.client.get("/parameter_types/", params=filters)

        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, list)
        if len(data) > 0:
            assert "name" in data[0]
            assert "measure_unit" in data[0]

    def test_disable_parameter_type(self):
        parameter_type_id = 1
        response = self.client.patch(f"/parameter_types/{parameter_type_id}")

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_get_parameter_type_by_id(self):
        parameter_type_id = 1
        response = self.client.get(f"/parameter_types/{parameter_type_id}")

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == parameter_type_id
        assert data["name"] == "Temperatura"

    def test_filter_parameter_types(self):
        filters = {"name": "Temperatura", "measure_unit": "°C"}

        response = self.client.get("/parameter_types/", params=filters)

        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, list)
        if len(data) > 0:
            assert "name" in data[0]
            assert "measure_unit" in data[0]

    def test_create_parameter_type_conflict(self):
        data = {
            "name": "Pressão",
            "measure_unit": "Pa",
            "qnt_decimals": 2,
            "offset": None,
            "factor": 1.0,
        }

        response = self.client.post("/parameter_types/", json=data)
        assert response.status_code == 200
        assert response.json() == {"data": None}

        response = self.client.post("/parameter_types/", json=data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Tipo de parâmetro já existe."
