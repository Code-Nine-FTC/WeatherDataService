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
        await db_session.execute(
            text("""
            DELETE FROM parameters WHERE station_id IN (
                SELECT id FROM weather_stations WHERE uid = 'station-999'
            )
        """)
        )
        await db_session.execute(
            text("DELETE FROM weather_stations WHERE uid = 'station-999'")
        )
        await db_session.commit()
        payload = {
            "name": "Estação Teste",
            "uid": "station-999",
            "latitude": -10.1234,
            "longitude": -50.5678,
            "address": {"city": "Cidade Teste", "state": "Estado Teste", "country": "Brasil"},
            "parameter_types": [pt.id for pt in parameter_types_fixture],
        }
        response = await authenticated_client.post("/stations/", json=payload)
        assert response.status_code == status.HTTP_200_OK
        await db_session.execute(
            text("""
    DELETE FROM parameters WHERE station_id IN (
        SELECT id FROM weather_stations WHERE uid = 'station-999'
    )
""")
        )
        await db_session.execute(
            text("DELETE FROM weather_stations WHERE uid = 'station-999'")
        )
        await db_session.commit()

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "name": "Estação Meteorológica Central",
            },
            {
                "uid": "station-0001",
            },
        ],
    )
    async def test_list_all_weather_stations(
        self,
        payload,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        response = await authenticated_client.get("/stations/filters", params=payload)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json()["data"], list)

    @pytest.mark.asyncio
    async def test_update_weather_station_partial(
        self,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        station = weather_stations_fixture[0]
        payload = {"name": "Novo Nome da Estação", "address": {"city": "Cidade Nova"}}
        response = await authenticated_client.patch(f"/stations/{station.id}", json=payload)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_deactivate_weather_station(
        self,
        authenticated_client: AsyncClient,
        weather_stations_fixture,
    ) -> None:
        station = weather_stations_fixture[1]
        response = await authenticated_client.patch(
            f"/stations/disable/{station.id}", json={"is_active": False}
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_get_nonexistent_weather_station(
        self,
        authenticated_client: AsyncClient,
    ) -> None:
        response = await authenticated_client.get("/stations/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
