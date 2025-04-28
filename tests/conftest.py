# -*- coding: utf-8 -*-


from typing import AsyncGenerator  # noqa: F401

import pytest
import pytest_asyncio  # noqa: F401
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401

from app.dependency.database import Database  # noqa: F401
from app.modules.security import TokenManager
from main import app
from tests.fixtures.fixture_insert import (
    alert_fixture,  # noqa: F401
    alert_station_fixture,  # noqa: F401
    alert_type_fixture,  # noqa: F401
    db_session,  # noqa: F401
    full_station_fixture,  # noqa: F401
    parameter_type_ativo,  # noqa: F401
    parameter_types_fixture,  # noqa: F401
    station_with_existing_uid_fixture,  # noqa: F401
)  # noqa: F401

# Importa as fixtures necessárias
from tests.fixtures.fixture_user import fake_user  # noqa: F401

# Importa as fixtures necessárias


@pytest.fixture(scope="function")  # noqa: PT003
def authenticated_client(fake_user) -> TestClient:  # noqa: F811  # type: ignore[no-untyped-def]
    client = TestClient(app, base_url="http://localhost:5000")
    token = TokenManager().create_access_token(fake_user)
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
