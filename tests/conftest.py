# -*- coding: utf-8 -*-


import pytest
from fastapi.testclient import TestClient

from app.modules.security import TokenManager
from main import app
from tests.fixtures.fixture_user import fake_user  # noqa: F401


@pytest.fixture(scope="function")  # noqa: PT003
def authenticated_client(fake_user) -> TestClient:  # noqa: F811  # type: ignore[no-untyped-def]
    client = TestClient(app, base_url="http://localhost:5000")
    token = TokenManager().create_access_token(fake_user)
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
