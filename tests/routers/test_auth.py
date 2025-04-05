# -*- coding: utf-8 -*-
import pytest
from fastapi.testclient import TestClient

from app.core.models.db_model import User


class TestsAuth:
    @pytest.mark.asyncio
    async def test_login(self, authenticated_client: TestClient, fake_user: User) -> None:
        login_data = {"username": "test_user@example.com", "password": "123"}

        response = authenticated_client.post("/auth/login", data=login_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
