# -- coding: utf-8 --
import pytest
from fastapi import status
from httpx import AsyncClient


class TestParameterType:
    @pytest.mark.asyncio
    @staticmethod
    async def test_create_parameter_type_invalid(authenticated_client: AsyncClient) -> None:
        response = await authenticated_client.post("/parameter_types/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    @staticmethod
    async def test_list_all_parameter_types(authenticated_client: AsyncClient) -> None:
        response = await authenticated_client.get("/parameter_types/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json()["data"], list)

    @pytest.mark.asyncio
    @staticmethod
    async def test_list_only_active_parameter_types(authenticated_client: AsyncClient) -> None:
        response = await authenticated_client.get(
            "/parameter_types/", params={"is_active": True}
        )
        assert response.status_code == status.HTTP_200_OK
        for item in response.json()["data"]:
            assert item["is_active"] is True

    @pytest.mark.asyncio
    @staticmethod
    async def test_filter_by_name(authenticated_client: AsyncClient) -> None:
        response = await authenticated_client.get(
            "/parameter_types/", params={"name": "Umidade"}
        )
        assert response.status_code == status.HTTP_200_OK
        for item in response.json()["data"]:
            assert item["name"] == "Umidade"

    @pytest.mark.asyncio
    @staticmethod
    async def test_update_nonexistent_parameter_type(
        authenticated_client: AsyncClient,
    ) -> None:
        response = await authenticated_client.patch(
            "/parameter_types/999999/update", json={"name": "Novo nome"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
