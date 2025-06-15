import pytest
from fastapi import status
from httpx import AsyncClient


class TestAlerts:
    @pytest.mark.asyncio
    async def test_list_all_alerts(
        self,
        authenticated_client: AsyncClient,
        alerts_fixture,
    ) -> None:
        response = await authenticated_client.get("/alerts/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert isinstance(data, list)
        assert len(data) >= len(alerts_fixture)

    @pytest.mark.asyncio
    async def test_filter_alerts_by_type(
        self,
        authenticated_client: AsyncClient,
        alerts_fixture,
    ) -> None:
        response = await authenticated_client.get(
            "/alerts/", params={"type_alert_name": "Alerta de Temperatura"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert all("Alerta de Temperatura" in alert["type_alert"]["name"] for alert in data)

    @pytest.mark.asyncio
    async def test_filter_alerts_by_station_name(
        self,
        authenticated_client: AsyncClient,
        alerts_fixture,
    ) -> None:
        response = await authenticated_client.get(
            "/alerts/", params={"station_name": "Estação 1"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert all("Estação 1" in alert["station"]["name_station"] for alert in data)

    @pytest.mark.asyncio
    async def test_get_nonexistent_alert_by_id(
        self,
        authenticated_client: AsyncClient,
    ) -> None:
        response = await authenticated_client.get("/alerts/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
