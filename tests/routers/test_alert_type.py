from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

import app
from app.routers.controller.alert_type import AlertTypeController
from app.schemas.alert_type_schema import AlertTypeCreate, AlertTypeUpdate
from app.service.alert_type import AlertTypeService

client = TestClient(app)


@pytest.fixture
def mock_session():
    session = MagicMock(AsyncSession)
    return session


@pytest.fixture
def valid_alert_data():
    return {
        "parameter_id": 1,
        "name": "High Temperature",
        "value": 50,
        "math_signal": "greater_than",
        "status": "active",
    }


# Teste para criar um novo tipo de alerta
@pytest.mark.asyncio
async def test_create_alert_type(mock_session, valid_alert_data):
    service = AlertTypeService(session=mock_session)

    # Simula a criação do tipo de alerta
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    data = AlertTypeCreate(**valid_alert_data)
    await service.create_alert_type(data)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para listar tipos de alerta
@pytest.mark.asyncio
async def test_list_alert_types(mock_session, valid_alert_data):
    # Simula a resposta da consulta de listagem
    mock_session.execute.return_value.fetchall.return_value = [valid_alert_data]

    service = AlertTypeService(session=mock_session)
    filters = True  # Filtro ativo
    response = await service.list_alert_types(filters)

    assert len(response) > 0
    assert response[0].name == "High Temperature"
    assert response[0].math_signal == "greater_than"


# Teste para obter um tipo de alerta específico
@pytest.mark.asyncio
async def test_get_alert_type(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data

    service = AlertTypeService(session=mock_session)
    alert_type = await service.get_alert_type(1)

    assert alert_type.name == "High Temperature"
    assert alert_type.math_signal == "greater_than"
    assert alert_type.id == 1


# Teste para desativar um tipo de alerta
@pytest.mark.asyncio
async def test_delete_alert_type(mock_session, valid_alert_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    service = AlertTypeService(session=mock_session)
    await service.delete_alert_type(1)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para atualizar um tipo de alerta
@pytest.mark.asyncio
async def test_update_alert_type(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    update_data = AlertTypeUpdate(name="Critical Temperature")
    service = AlertTypeService(session=mock_session)
    await service.update_alert_type(1, update_data)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o controlador de criar tipo de alerta
@pytest.mark.asyncio
async def test_create_alert_type_controller(mock_session, valid_alert_data):
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    data = AlertTypeCreate(**valid_alert_data)
    controller = AlertTypeController(mock_session)
    response = await controller.create_alert_type(data)

    assert response.data is None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o controlador de listar tipos de alerta
@pytest.mark.asyncio
async def test_list_alert_types_controller(mock_session, valid_alert_data):
    mock_session.execute.return_value.fetchall.return_value = [valid_alert_data]

    controller = AlertTypeController(mock_session)
    response = await controller.list_alert_types(True)

    assert response.data[0].name == "High Temperature"
    assert response.data[0].math_signal == "greater_than"


# Teste para o controlador de obter um tipo de alerta
@pytest.mark.asyncio
async def test_get_alert_type_controller(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data

    controller = AlertTypeController(mock_session)
    response = await controller.get_alert_type(1)

    assert response.data.name == "High Temperature"
    assert response.data.math_signal == "greater_than"
    assert response.data.id == 1


# Teste para o controlador de desativar um tipo de alerta
@pytest.mark.asyncio
async def test_delete_alert_type_controller(mock_session, valid_alert_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    controller = AlertTypeController(mock_session)
    await controller.delete_alert_type(1)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o controlador de atualizar um tipo de alerta
@pytest.mark.asyncio
async def test_update_alert_type_controller(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    update_data = AlertTypeUpdate(name="Critical Temperature")
    controller = AlertTypeController(mock_session)
    await controller.update_alert_type(1, update_data)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o endpoint de criar tipo de alerta
def test_create_alert_type_endpoint(mock_session, valid_alert_data):
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    response = client.post(
        "/alert_type/",
        json=valid_alert_data,
    )

    assert response.status_code == HTTPStatus.OK
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o endpoint de listar tipos de alerta
def test_list_alert_types_endpoint(mock_session, valid_alert_data):
    mock_session.execute.return_value.fetchall.return_value = [valid_alert_data]

    response = client.get("/alert_type/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json().get("data")) > 0


# Teste para o endpoint de obter um tipo de alerta
def test_get_alert_type_endpoint(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data

    response = client.get("/alert_type/1")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json().get("data")
    assert response_data["name"] == "High Temperature"


# Teste para o endpoint de desativar um tipo de alerta
def test_delete_alert_type_endpoint(mock_session, valid_alert_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    response = client.patch("/alert_type/disables/1")

    assert response.status_code == HTTPStatus.OK
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o endpoint de atualizar um tipo de alerta
def test_update_alert_type_endpoint(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    update_data = {
        "name": "Critical Temperature",
        "value": 100,
        "math_signal": "greater_than",
    }

    response = client.patch("/alert_type/1", json=update_data)

    assert response.status_code == HTTPStatus.OK
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()
