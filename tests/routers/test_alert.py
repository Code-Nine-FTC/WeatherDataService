import pytest
from fastapi.testclient import TestClient

# Códigos HTTP usados nos testes
HTTP_STATUS_OK = 200
HTTP_STATUS_NOT_FOUND = 404


class TestAlert:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient):
        self.client = authenticated_client

    # 1. Lista todos os alertas
    def test_get_all_alerts(self, alert):
        response = self.client.get("/alert/all")

        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        assert isinstance(data, list)
        assert any(a["id"] == alert.id for a in data)

    # 2. Lista alertas filtrando por station_id
    def test_get_alerts_by_station_id(self, alert):
        response = self.client.get("/alert/all", params={"station_id": alert.station_id})

        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        assert all(a["station_name"] == "Estação 1" for a in data)

    # 3. Lista alertas filtrando por alert_type_id
    def test_get_alerts_by_alert_type_id(self, alert):
        response = self.client.get("/alert/all", params={"alert_type_id": alert.alert_type_id})

        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        assert all(a["type_alert_name"] == "Temperatura Alta" for a in data)

    # 4. Recupera alerta por ID
    def test_get_alert_by_id(self, alert):
        response = self.client.get(f"/alert/{alert.id}")

        assert response.status_code == HTTP_STATUS_OK
        data = response.json()["data"]
        assert data["id"] == alert.id
        assert data["measure_value"] == "35"
        assert data["type_alert_name"] == "Temperatura Alta"
        assert data["station_name"] == "Estação 1"

    # 5. Recupera alerta com ID inexistente
    def test_get_alert_by_id_not_found(self):
        alert_id = 99999
        response = self.client.get(f"/alert/{alert_id}")

        assert response.status_code == HTTP_STATUS_NOT_FOUND
        assert response.json()["detail"] == f"Alerta com a ID {alert_id} não encontrado."

    # 6. Deleta alerta por ID
    def test_delete_alert(self, alert):
        response = self.client.delete(f"/alert/{alert.id}")

        assert response.status_code == HTTP_STATUS_OK
        assert response.json() == {"data": None}

    # 7. Tenta deletar alerta com ID inexistente
    def test_delete_alert_not_found(self):
        alert_id = 99999
        response = self.client.delete(f"/alert/{alert_id}")

        assert response.status_code == HTTP_STATUS_NOT_FOUND
        assert response.json()["detail"] == f"Alerta com a ID {alert_id} não encontrado."
