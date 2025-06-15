import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import text


class TestWeatherStations:
    @pytest.mark.asyncio
    async def test_create_weather_station_with_parameters(
        self,
        authenticated_client: AsyncClient,
        parameter_types_fixture,
        db_session,
    ) -> None:
        await db_session.execute(text("""
    DELETE FROM parameters WHERE station_id IN (
        SELECT id FROM weather_stations WHERE uid = 'station-999'
    )
"""))
        await db_session.execute(text("DELETE FROM weather_stations WHERE uid = 'station-999'"))
        await db_session.commit()
        payload = {
            "name": "Estação Teste",
            "uid": "station-999",
            "latitude": -10.1234,
            "longitude": -50.5678,
            "address": {
            "city": "Cidade Teste",
            "state": "Estado Teste",
            "country": "Brasil"
            },
            "parameter_types": [pt.id for pt in parameter_types_fixture],
        }
        response = await authenticated_client.post("/stations/", json=payload)
        assert response.status_code == status.HTTP_200_OK
        await db_session.execute(text("""
    DELETE FROM parameters WHERE station_id IN (
        SELECT id FROM weather_stations WHERE uid = 'station-999'
    )
"""))
        await db_session.execute(text("DELETE FROM weather_stations WHERE uid = 'station-999'"))
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_list_all_weather_stations(
        self,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        response = await authenticated_client.get("/weather_stations/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json()["data"], list)

    @pytest.mark.asyncio
    async def test_filter_weather_station_by_uid(
        self,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        station = weather_stations_fixture[0]
        response = await authenticated_client.get(
            "/weather_stations/", params={"uid": station.uid}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert all(d["uid"] == station.uid for d in data)

    @pytest.mark.asyncio
    async def test_filter_weather_station_by_name(
        self,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        station = weather_stations_fixture[1]
        response = await authenticated_client.get(
            "/weather_stations/", params={"name": station.name}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert all(d["name_station"] == station.name for d in data)

    @pytest.mark.asyncio
    async def test_filter_weather_station_by_active_status(
        self,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        response = await authenticated_client.get(
            "/weather_stations/", params={"is_active": True}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert all(d["is_active"] is True for d in data)

    @pytest.mark.asyncio
    async def test_update_weather_station_partial(
        self,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        station = weather_stations_fixture[0]
        payload = {
            "name": "Novo Nome da Estação",
            "address": {
                "city": "Cidade Nova"
            }
        }
        response = await authenticated_client.patch(
            f"/weather_stations/{station.id}/update", json=payload
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["name_station"] == "Novo Nome da Estação"
        assert data["address"]["city"] == "Cidade Nova"

    @pytest.mark.asyncio
    async def test_deactivate_weather_station(
        self,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        station = weather_stations_fixture[1]
        response = await authenticated_client.patch(
            f"/weather_stations/{station.id}/update", json={"is_active": False}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["is_active"] is False

    @pytest.mark.asyncio
    async def test_get_nonexistent_weather_station(
        self,
        authenticated_client: AsyncClient,
    ) -> None:
        response = await authenticated_client.get("/weather_stations/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND