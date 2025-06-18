# -- coding: utf-8 --
import pytest
from fastapi import status
from httpx import AsyncClient


class TestAlerts:
    @pytest.mark.asyncio
    @staticmethod
    async def test_list_all_alerts(
        authenticated_client: AsyncClient,
        alerts_fixture,
        type_alerts_fixture,
        measures_fixture,
    ) -> None:
        response = await authenticated_client.get("/alert/all")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert isinstance(data, list)
        if data:
            assert "id" in data[0]
            assert "type_alert_name" in data[0]
            assert "station_name" in data[0]
            assert "measure_value" in data[0]
            assert "create_date" in data[0]

    @pytest.mark.asyncio
    @staticmethod
    async def test_filter_by_type_alert_name(
        authenticated_client: AsyncClient, alerts_fixture
    ) -> None:
        response = await authenticated_client.get("/alert/all?type_alert_name=Temperatura")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        for alert in data:
            assert "Temperatura" in alert["type_alert_name"]

    @pytest.mark.asyncio
    @staticmethod
    async def test_filter_by_station_name(
        authenticated_client: AsyncClient, alerts_fixture
    ) -> None:
        response = await authenticated_client.get("/alert/all?station_name=Estação 1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        for alert in data:
            assert "Estação 1" in alert["station_name"]

    @pytest.mark.asyncio
    @staticmethod
    async def test_get_alert_by_invalid_id(authenticated_client: AsyncClient) -> None:
        response = await authenticated_client.get("/alert/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "não encontrado" in response.json()["detail"]

    @pytest.mark.asyncio
    @staticmethod
    async def test_mark_alert_as_read(
        authenticated_client: AsyncClient, alerts_fixture
    ) -> None:
        alert_id = alerts_fixture[0].id
        response = await authenticated_client.patch(f"/alert/{alert_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"] is None

    @pytest.mark.asyncio
    @staticmethod
    async def test_filter_with_no_results(authenticated_client: AsyncClient) -> None:
        response = await authenticated_client.get(
            "/alert/all?station_name=Estação Inexistente"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"] == []

    @pytest.mark.asyncio
    @staticmethod
    async def test_filter_with_invalid_param(authenticated_client: AsyncClient) -> None:
        response = await authenticated_client.get("/alert/all?type_alert_name=1234")
        assert response.status_code == status.HTTP_200_OK
        # Pode retornar vazio ou lista com nomes parcialmente semelhantes
        assert "data" in response.json()
