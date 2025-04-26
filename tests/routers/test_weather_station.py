from fastapi.testclient import TestClient
from fastapi import status


class TestStation:
    # 1. POST - Criação de estação não precisa de fixture
    def test_create_station(self, authenticated_client: TestClient, parameter_types_fixture):
        data = {
            "name": "Estação Nova",
            "uid": "nova-uid-123",
            "latitude": -10.0,
            "longitude": -50.0,
            "address": {"city": "Cuiabá", "state": "MT", "country": "Brasil"},
            "parameter_types": [1 for pt in parameter_types_fixture],
        }
        response = authenticated_client.post("/stations/", json=data)
        assert response.status_code == status.HTTP_200_OK

    # 2. POST - UID existente precisa de uma fixture com uma estação cadastrada
    def test_create_station_with_existing_uid(
        self, authenticated_client: TestClient, station_with_existing_uid_fixture
    ):
        station = station_with_existing_uid_fixture["station"]
        param_types = station_with_existing_uid_fixture["parameter_types"]
        data = {
            "name": "Duplicada",
            "uid": station.uid,
            "latitude": -22.0,
            "longitude": -44.0,
            "address": {"city": "São Paulo", "state": "SP", "country": "Brasil"},
            "parameter_types": [pt.id for pt in param_types],
        }
        response = authenticated_client.post("/stations/", json=data)
        assert response.status_code == status.HTTP_409_CONFLICT

    # 3. POST - Campos ausentes não precisa de fixture
    def test_create_station_with_missing_fields(self, authenticated_client: TestClient):
        data = {"name": "Incompleta"}
        response = authenticated_client.post("/stations/", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # 4. POST - Com tipos de parâmetros e checagem de vínculo
    def test_create_station_with_parameters_and_verify_link(
        self, authenticated_client: TestClient, parameter_types_fixture
    ):
        data = {
            "name": "Vinculada",
            "uid": "com-parametro",
            "latitude": -25.0,
            "longitude": -45.0,
            "address": {"city": "Joinville", "state": "SC", "country": "Brasil"},
            "parameter_types": [pt.id for pt in parameter_types_fixture],
        }
        response = authenticated_client.post("/stations/", json=data)
        assert response.status_code == status.HTTP_200_OK

        response = authenticated_client.get(
            "/stations/filters", params={"uid": "com-parametro"}
        )
        data = response.json()["data"][0]
        assert len(data["parameters"]) == len(parameter_types_fixture)

    # 5. GET - Lista estações precisa de fixture
    def test_list_stations(self, authenticated_client: TestClient, full_station_fixture):
        response = authenticated_client.get("/stations/filters")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json()["data"], list)

    # 6. GET - Lista com filtros precisa de fixture
    def test_list_stations_with_filters(
        self, authenticated_client: TestClient, full_station_fixture
    ):
        station = full_station_fixture["station"]
        response = authenticated_client.get(
            "/stations/filters",
            params={"uid": station.uid, "name": station.name, "status": True},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data) > 0

    # 7. GET - Parâmetro por ID precisa de fixture
    def test_get_parameter_by_valid_type_id(
        self, authenticated_client: TestClient, parameter_types_fixture
    ):
        param_id = parameter_types_fixture[0].id
        response = authenticated_client.get(f"/stations/parameters/{param_id}")
        assert response.status_code == status.HTTP_200_OK

    # 8. GET - Parâmetro inexistente
    def test_get_parameter_by_invalid_type_id(self, authenticated_client: TestClient):
        response = authenticated_client.get("/stations/parameters/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    # 9. GET - Estação por ID precisa de fixture
    def test_get_station_by_id(self, authenticated_client: TestClient, full_station_fixture):
        station = full_station_fixture["station"]
        response = authenticated_client.get(f"/stations/{station.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["uid"] == station.uid

    # 10. GET - Estação inexistente
    def test_get_station_by_invalid_id(self, authenticated_client: TestClient):
        response = authenticated_client.get("/stations/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    # 11. PATCH - Atualizar estação com parâmetros
    def test_update_station_with_new_parameters(
        self, authenticated_client: TestClient, full_station_fixture
    ):
        station = full_station_fixture["station"]
        param_types = full_station_fixture["parameter_types"]
        data = {
            "name": "Estação Atualizada",
            "parameter_types": [param_types[1].id],
            "latitude": -20.0,
            "longitude": -50.0,
            "address": {"city": "Floripa", "state": "SC", "country": "Brasil"},
        }
        response = authenticated_client.patch(f"/stations/{station.id}", json=data)
        assert response.status_code == status.HTTP_200_OK

    # 12. PATCH - Atualizar com ID inválido
    def test_update_station_invalid_id(self, authenticated_client: TestClient):
        data = {"name": "Falha"}
        response = authenticated_client.patch("/stations/99999", json=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    # 13. PATCH - Remover parâmetros precisa de fixture
    def test_remove_parameter_from_station_and_check_cleanup(
        self, authenticated_client: TestClient, full_station_fixture
    ):
        station = full_station_fixture["station"]
        param_id = full_station_fixture["parameter_types"][1].id
        response = authenticated_client.patch(f"/stations/{station.id}/parameter/{param_id}")
        assert response.status_code == status.HTTP_200_OK

        response = authenticated_client.get(f"/stations/{station.id}")
        data = response.json()["data"]
        param_ids = [p["id"] for p in data["parameters"]]
        assert param_id not in param_ids
