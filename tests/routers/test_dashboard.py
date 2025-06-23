import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.core.models.db_model import Alert, Measures, Parameter, TypeAlert, WeatherStation
from main import app


@pytest.fixture
async def simple_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:5000") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_station_history(
    authenticated_client: AsyncClient,
    weather_stations_fixture: list[WeatherStation],
    parameters_fixture: list[Parameter],
    measures_fixture: list[Measures],
):
    """Teste para obter o histórico de uma estação específica."""
    station_id = weather_stations_fixture[0].id

    response = await authenticated_client.get(f"/dashboard/station-history/{station_id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

    response = await authenticated_client.get(
        f"/dashboard/station-history/{station_id}?startDate=2025-01-01&endDate=2025-12-31"
    )
    assert response.status_code == status.HTTP_200_OK

    response = await authenticated_client.get("/dashboard/station-history/9999")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 0


@pytest.mark.asyncio
async def test_get_alert_type_distribution(
    authenticated_client: AsyncClient,
    weather_stations_fixture: list[WeatherStation],
    type_alerts_fixture: list[TypeAlert],
):
    """Teste para obter a distribuição de tipos de alerta."""
    response = await authenticated_client.get("/dashboard/alert-types")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

    station_id = weather_stations_fixture[0].id
    response = await authenticated_client.get(
        f"/dashboard/alert-types?station_id={station_id}"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_alert_types_with_invalid_station(authenticated_client: AsyncClient):
    response = await authenticated_client.get("/dashboard/alert-types?station_id=999999")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_get_alert_counts(
    authenticated_client: AsyncClient,
    weather_stations_fixture: list[WeatherStation],
    alerts_fixture: list[Alert],
):
    """Teste para obter contagem de alertas."""
    response = await authenticated_client.get("/dashboard/alert-counts")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert "G" in data["data"]
    assert "R" in data["data"]
    assert "Y" in data["data"]

    station_id = weather_stations_fixture[0].id
    response = await authenticated_client.get(
        f"/dashboard/alert-counts?station_id={station_id}"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_alert_counts_with_invalid_station(authenticated_client: AsyncClient):
    response = await authenticated_client.get("/dashboard/alert-counts?station_id=999999")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == {"G": 0, "Y": 0, "R": 0}


@pytest.mark.asyncio
async def test_get_station_status(
    authenticated_client: AsyncClient, weather_stations_fixture: list[WeatherStation]
):
    """Teste para obter o status das estações."""
    response = await authenticated_client.get("/dashboard/station-status")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert "total" in data["data"]
    assert "active" in data["data"]


@pytest.mark.asyncio
async def test_get_measures_status(authenticated_client: AsyncClient):
    """Teste para obter o status das medições."""
    response = await authenticated_client.get("/dashboard/measures-status")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

    if data["data"]:
        first_item = data["data"][0]
        assert "label" in first_item
        assert "number" in first_item


@pytest.mark.asyncio
async def test_measures_status_structure(authenticated_client: AsyncClient):
    response = await authenticated_client.get("/dashboard/measures-status")
    assert response.status_code == status.HTTP_200_OK
    for item in response.json()["data"]:
        assert isinstance(item["label"], str)
        assert isinstance(item["number"], int)


@pytest.mark.asyncio
async def test_get_last_measures(
    authenticated_client: AsyncClient,
    weather_stations_fixture: list[WeatherStation],
    measures_fixture: list[Measures],
):
    """Teste para obter as últimas medições de uma estação específica."""
    station_id = weather_stations_fixture[0].id

    response = await authenticated_client.get(f"/dashboard/last-measures/{station_id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

    response = await authenticated_client.get("/dashboard/last-measures/9999")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_dashboard_public_access(
    simple_client: AsyncClient, weather_stations_fixture: list[WeatherStation]
):
    """Teste para verificar que as rotas do dashboard são acessíveis sem autenticação."""
    station_id = weather_stations_fixture[0].id

    endpoints = [
        f"/dashboard/station-history/{station_id}",
        "/dashboard/alert-types",
        "/dashboard/alert-counts",
        "/dashboard/station-status",
        "/dashboard/measures-status",
        f"/dashboard/last-measures/{station_id}",
    ]

    for endpoint in endpoints:
        response = await simple_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert "data" in response.json()
