import pytest
from fastapi.testclient import TestClient

# Códigos HTTP usados nos testes
HTTP_STATUS_OK = 200
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_CONFLICT = 409
HTTP_STATUS_UNPROCESSABLE = 422


class TestAlertType:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient):
        self.client = authenticated_client

    # 1. Criar tipo de alerta com dados válidos
    def test_create_alert_type(self, parameter):
        data = {
            "parameter_id": parameter.id,
            "name": "Temperatura crítica",
            "value": 35,
            "math_signal": "gt",
            "status": "active",
        }

        response = self.client.post("/alert_type/", json=data)

        assert response.status_code == HTTP_STATUS_OK
        assert response.json() == {"data": None}

    # 2. Tenta criar alerta existente (mesmo nome, valor e sinal)
    def test_create_alert_type_conflict(self, type_alert_active):
        data = {
            "parameter_id": type_alert_active.parameter_id,
            "name": "Alerta de temperatura",
            "value": 50,
            "math_signal": "gt",
            "status": "active",
        }

        response = self.client.post("/alert_type/", json=data)

        assert response.status_code == HTTP_STATUS_CONFLICT
        assert "detail" in response.json()

    # 3. Tenta criar alerta com parâmetro inexistente
    def test_create_alert_type_parameter_not_found(self, parameter_not_in_db):
        data = {
            "parameter_id": parameter_not_in_db,
            "name": "Pressão baixa",
            "value": 50,
            "math_signal": "lt",
            "status": "active",
        }

        response = self.client.post("/alert_type/", json=data)

        assert response.status_code == HTTP_STATUS_NOT_FOUND
        assert "detail" in response.json()

    # 4. Criação com dados obrigatórios ausentes
    def test_create_alert_type_missing_fields(self, parameter):
        data = {
            # intentionally omitting required fields
            "value": 20,
        }

        response = self.client.post("/alert_type/", json=data)

        assert response.status_code == HTTP_STATUS_UNPROCESSABLE
        assert "detail" in response.json()

    # 5. Lista alertas ativos
    def test_list_active_alert_types(self, type_alert_active):
        response = self.client.get("/alert_type/")

        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        for item in data:
            assert item["is_active"] is True

    # 6. Lista alertas inativos
    def test_list_inactive_alert_types(self, type_alert_inactive):
        response = self.client.get("/alert_type/?is_active=false")

        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        for item in data:
            assert item["is_active"] is False

    # 7. Lista alerta com ID existente
    def test_get_alert_type_by_id(self, type_alert_active):
        response = self.client.get(f"/alert_type/{type_alert_active.id}")

        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        assert data["id"] == type_alert_active.id

    # 8. Lista alerta com ID inexistente
    def test_get_alert_type_by_id_not_found(self):
        response = self.client.get("/alert_type/999999")

        assert response.status_code == HTTP_STATUS_NOT_FOUND
        assert "detail" in response.json()

    # 9. Atualiza com todos os campos None
    def test_update_alert_type_with_none_fields(self, type_alert_active):
        data = {
            "name": None,
            "value": None,
            "math_signal": None,
            "status": None,
            "parameter_id": None,
        }

        response = self.client.patch(f"/alert_type/{type_alert_active.id}", json=data)

        assert response.status_code == HTTP_STATUS_OK
        assert response.json() == {"data": None}

    # 10. Atualiza alerta com ID inexistente
    def test_update_alert_type_invalid_id(self):
        data = {
            "name": "Teste inválido",
            "value": 42,
            "math_signal": "eq",
            "status": "inactive",
        }

        response = self.client.patch("/alert_type/999999", json=data)

        assert response.status_code == HTTP_STATUS_NOT_FOUND
        assert "detail" in response.json()

    # 11. Atualiza com nome já existente (gera conflito)
    def test_update_alert_type_conflict(self, type_alert_active, type_alert_inactive):
        data = {
            "name": "Alerta de pressão",
            "value": 10,
            "math_signal": "lt",
            "status": "inactive",
        }

        response = self.client.patch(f"/alert_type/{type_alert_active.id}", json=data)

        assert response.status_code == HTTP_STATUS_CONFLICT
        assert "detail" in response.json()

    # 12. Atualiza com parâmetro inexistente
    def test_update_alert_type_with_invalid_parameter(
        self, type_alert_active, parameter_not_in_db
    ):
        data = {
            "parameter_id": parameter_not_in_db,
            "name": "Teste parametro inválido",
            "value": 99,
            "math_signal": "lt",
            "status": "active",
        }

        response = self.client.patch(f"/alert_type/{type_alert_active.id}", json=data)

        assert response.status_code == HTTP_STATUS_NOT_FOUND
        assert "detail" in response.json()

    # 13. Atualiza todos os campos
    def test_update_alert_type_all_fields(self, type_alert_active, parameter):
        data = {
            "parameter_id": parameter.id,
            "name": "Nova temperatura",
            "value": 45,
            "math_signal": "gt",
            "status": "inactive",
        }

        response = self.client.patch(f"/alert_type/{type_alert_active.id}", json=data)

        assert response.status_code == HTTP_STATUS_OK
        assert response.json() == {"data": None}

    # 14. Desativa tipo de alerta
    def test_disable_alert_type(self, type_alert_active):
        response = self.client.patch(f"/alert_type/disables/{type_alert_active.id}")

        assert response.status_code == HTTP_STATUS_OK
        assert response.json() == {"data": None}

        # Verifica se ficou inativo
        get_response = self.client.get(f"/alert_type/{type_alert_active.id}")
        assert get_response.status_code == HTTP_STATUS_OK
        assert get_response.json()["data"]["is_active"] is False

    # 15. Desativação com ID inexistente
    def test_disable_alert_type_not_found(self):
        response = self.client.patch("/alert_type/disables/999999")

        assert response.status_code == HTTP_STATUS_NOT_FOUND
        assert "detail" in response.json()
