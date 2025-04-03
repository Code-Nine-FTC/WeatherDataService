from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

import app  # Importando o app FastAPI
from app.schemas.user import UserResponse
from app.service.user import UserService

client = TestClient(app)


@pytest.fixture
def mock_session():
    session = MagicMock(AsyncSession)
    return session


@pytest.fixture
def valid_user_data():
    return {
        "id": 1,
        "name": "John Doe",
        "email": "johndoe@example.com",
        "password": "hashedpassword",
        "last_update": "2025-04-01T12:00:00",
    }


# Teste para o serviço de obter usuário por email
@pytest.mark.asyncio
async def test_get_user_by_email(mock_session, valid_user_data):
    # Cria um resultado falso
    mock_session.execute.return_value.fetchone.return_value = valid_user_data

    service = UserService(session=mock_session)
    user = await service.get_user_by_email("johndoe@example.com")

    assert user.email == "johndoe@example.com"
    assert user.name == "John Doe"
    assert user.id == 1


# Teste para o serviço de obter usuário por ID
@pytest.mark.asyncio
async def test_get_user_by_id(mock_session, valid_user_data):
    # Cria um resultado falso
    mock_session.execute.return_value.fetchone.return_value = valid_user_data

    service = UserService(session=mock_session)
    user = await service.get_user_by_id(1)

    assert user.email == "johndoe@example.com"
    assert user.name == "John Doe"
    assert user.id == 1


# Teste para o controlador de obter usuário
@pytest.mark.asyncio
async def test_get_user_controller(mock_session, valid_user_data):
    # Mock do controlador para retornar usuário válido
    mock_session.execute.return_value.fetchone.return_value = valid_user_data
    fake_user = UserResponse(**valid_user_data)

    # Supondo que o controlador chame o serviço para buscar o usuário
    user_controller = UserController(session=mock_session, user=fake_user)
    response = await user_controller.get_user()

    assert response.data.email == "johndoe@example.com"
    assert response.data.name == "John Doe"
    assert response.data.id == 1


# Teste para o endpoint de obter usuário
@pytest.mark.asyncio
async def test_get_user_endpoint(mock_session, valid_user_data):
    # Mock do usuário no formato esperado
    mock_session.execute.return_value.fetchone.return_value = valid_user_data
    fake_user = UserResponse(**valid_user_data)

    # Supondo que o teste esteja autenticando o usuário
    response = client.get("/user/", headers={"Authorization": "Bearer fake_token"})

    assert response.status_code == HTTPStatus.OK
    response_data = response.json().get("data")
    assert response_data["email"] == "johndoe@example.com"
    assert response_data["name"] == "John Doe"
    assert response_data["id"] == 1


# Teste para o erro quando o usuário não é encontrado pelo email
@pytest.mark.asyncio
async def test_get_user_by_email_not_found(mock_session):
    mock_session.execute.return_value.fetchone.return_value = None

    service = UserService(session=mock_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_by_email("nonexistentuser@example.com")

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == "Usuário não encontrado"
