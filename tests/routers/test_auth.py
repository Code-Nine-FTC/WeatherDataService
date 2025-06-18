# # -*- coding: utf-8 -*-
import pytest
from fastapi import status
from httpx import AsyncClient

from app.core.models.db_model import User


class TestsAuth:
    @pytest.mark.asyncio
    @staticmethod
    async def test_login(authenticated_client: AsyncClient, fake_user: User) -> None:
        login_data = {"username": "test_user@example.com", "password": "123"}

        response = await authenticated_client.post("/auth/login", data=login_data)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
