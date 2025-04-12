import pytest
from fastapi.testclient import TestClient

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_UNPROCESSABLE_ENTITY = 422


class TestParameterType:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient):
        self.client = authenticated_client

    def test_create_parameter_type(self):
        response = self.client.post(
            "/parameter_types/",
            json={
                "name": "Umidade",
                "measure_unit": "%",
                "qnt_decimals": 1,
                "offset": 0.0,
                "factor": 1.0,
            },
        )
        assert response.status_code == HTTP_OK
        assert response.json() == {"data": None}

    def test_create_parameter_type_conflict(self, parameter_type_ativo):
        response = self.client.post(
            "/parameter_types/",
            json={
                "name": parameter_type_ativo.name,
                "measure_unit": parameter_type_ativo.measure_unit,
                "qnt_decimals": parameter_type_ativo.qnt_decimals,
                "offset": parameter_type_ativo.offset,
                "factor": parameter_type_ativo.factor,
            },
        )
        assert response.status_code == HTTP_CONFLICT
        assert "Tipo de parâmetro já existe" in response.json()["detail"]

    def test_create_parameter_type_invalid(self):
        response = self.client.post("/parameter_types/", json={})
        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    def test_list_all_parameter_types(self):
        response = self.client.get("/parameter_types/")
        assert response.status_code == HTTP_OK
        assert isinstance(response.json()["data"], list)

    def test_list_only_active_parameter_types(self, parameter_type_ativo):
        response = self.client.get("/parameter_types/", params={"is_active": True})
        assert response.status_code == HTTP_OK
        for item in response.json()["data"]:
            assert item["is_active"] is True

    def test_filter_by_name(self, parameter_type_ativo):
        response = self.client.get("/parameter_types/", params={"name": "Temperatura"})
        assert response.status_code == HTTP_OK
        for item in response.json()["data"]:
            assert item["name"] == "Temperatura"

    def test_filter_by_measure_unit(self, parameter_type_ativo):
        response = self.client.get("/parameter_types/", params={"measure_unit": "°C"})
        assert response.status_code == HTTP_OK
        for item in response.json()["data"]:
            assert item["measure_unit"] == "°C"

    def test_disable_parameter_type(self, parameter_type_ativo):
        response = self.client.patch(f"/parameter_types/{parameter_type_ativo.id}")
        assert response.status_code == HTTP_OK
        # Ideal: buscar de novo e verificar is_active=False

    def test_disable_nonexistent_parameter_type(self, parameter_type_nao_existente_id):
        response = self.client.patch(f"/parameter_types/{parameter_type_nao_existente_id}")
        assert response.status_code == HTTP_NOT_FOUND

    def test_get_parameter_type_by_id(self, parameter_type_ativo):
        response = self.client.get(f"/parameter_types/{parameter_type_ativo.id}")
        assert response.status_code == HTTP_OK
        data = response.json()["data"]
        assert data["id"] == parameter_type_ativo.id
        assert data["name"] == parameter_type_ativo.name

    def test_get_nonexistent_parameter_type(self, parameter_type_nao_existente_id):
        response = self.client.get(f"/parameter_types/{parameter_type_nao_existente_id}")
        assert response.status_code == HTTP_NOT_FOUND

    def test_update_parameter_type(self, parameter_type_ativo):
        response = self.client.patch(
            f"/parameter_types/{parameter_type_ativo.id}/update",
            json={
                "name": "Temperatura Atualizada",
                "measure_unit": "K",
                "qnt_decimals": 3,
                "offset": 1.0,
                "factor": 2.0,
            },
        )
        assert response.status_code == HTTP_OK

    def test_update_nonexistent_parameter_type(self, parameter_type_nao_existente_id):
        response = self.client.patch(
            f"/parameter_types/{parameter_type_nao_existente_id}/update", json={"name": "X"}
        )
        assert response.status_code == HTTP_NOT_FOUND
