import pytest
from fastapi.testclient import TestClient

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_UNPROCESSABLE_ENTITY = 422
QNT_DECIMALS_UPDATED = 3


@pytest.mark.asyncio  # Marca a classe de testes para permitir testes assíncronos
class TestParameterType:
    # 1. POST - Criação de tipo de parâmetro
    def test_create_parameter_type(self, authenticated_client: TestClient):
        response = authenticated_client.post(
            "/parameter_types/",
            json={
                "name": "Umidade",
                "detect_type": "climate",
                "measure_unit": "%",
                "qnt_decimals": 1,
                "offset": 0.0,
                "factor": 1.0,
            },
        )
        assert response.status_code == HTTP_OK
        assert response.json() == {"data": None}

    # 3. POST - Corpo vazio
    def test_create_parameter_type_invalid(self, authenticated_client: TestClient):
        response = authenticated_client.post("/parameter_types/", json={})
        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    # 4. GET - Lista todos os tipos de parâmetro
    def test_list_all_parameter_types(self, authenticated_client: TestClient):
        response = authenticated_client.get("/parameter_types/")
        assert response.status_code == HTTP_OK
        assert isinstance(response.json()["data"], list)

    # 5. GET - Filtra tipos de parâmetro ativos
    def test_list_only_active_parameter_types(self, authenticated_client: TestClient):
        response = authenticated_client.get("/parameter_types/", params={"is_active": True})
        assert response.status_code == HTTP_OK
        for item in response.json()["data"]:
            assert item["is_active"] is True

    # 6. GET - Filtra tipos de parâmetro por nome
    def test_filter_by_name(self, authenticated_client: TestClient):
        response = authenticated_client.get("/parameter_types/", params={"name": "Umidade"})
        assert response.status_code == HTTP_OK
        for item in response.json()["data"]:
            assert item["name"] == "Umidade"

    # 8. PATCH - Atualizar tipo de parâmetro inexistente
    def test_update_nonexistent_parameter_type(self, authenticated_client: TestClient):
        response = authenticated_client.patch(
            "/parameter_types/999999/update", json={"name": "Novo nome"}
        )
        assert response.status_code == HTTP_NOT_FOUND
