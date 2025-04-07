import pytest
from fastapi.testclient import TestClient


class TestAlert:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient):
        self.client = authenticated_client

    def test_get_filtered_alerts(self):
        filters = {"alert_type_id": 1, "station_id": 1}

        response = self.client.get("/alert/all", params=filters)

        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "measure_value" in data[0]
            assert "station_name" in data[0]
            assert "type_alert_name" in data[0]
            assert "create_date" in data[0]

    def test_get_alert_by_id(self):
        alert_id = 1
        response = self.client.get(f"/alert/{alert_id}")

        assert response.status_code == 200
        data = response.json()["data"]
        assert "id" in data
        assert "measure_value" in data
        assert "station_name" in data
        assert "type_alert_name" in data
        assert "create_date" in data

    def test_delete_alert(self):
        alert_id = 1
        response = self.client.delete(f"/alert/{alert_id}")

        assert response.status_code == 200
        assert response.json() == {"data": None}

    def test_get_filtered_alerts_no_filters(self):
        response = self.client.get("/alert/all")

        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "measure_value" in data[0]
            assert "station_name" in data[0]
            assert "type_alert_name" in data[0]
            assert "create_date" in data[0]

    def test_get_alert_by_id_not_found(self):
        alert_id = 999
        response = self.client.get(f"/alert/{alert_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == f"Alerta com a ID {alert_id} não encontrado."

    def test_delete_alert_not_found(self):
        alert_id = 999
        response = self.client.delete(f"/alert/{alert_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == f"Alerta com a ID {alert_id} não encontrado."
