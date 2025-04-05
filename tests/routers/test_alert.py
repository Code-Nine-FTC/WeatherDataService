from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

import app
from app.routers.controller.alert import AlertController
from app.schemas.alert import AlertFilterSchema, AlertResponse
from app.service.alert import AlertService

client = TestClient(app)


@pytest.fixture
def mock_session():
    session = MagicMock(AsyncSession)
    return session


@pytest.fixture
def valid_alert_data():
    return {
        "id": 1,
        "measure_value": "25.5",
        "type_alert_name": "Temperature Alert",
        "station_name": "Station 1",
        "create_date": "2025-04-01T00:00:00",
    }


# Teste para criar um alerta
@pytest.mark.asyncio
async def test_create_alert(mock_session, valid_alert_data):
    service = AlertService(session=mock_session)

    # Simula a criação do alerta
    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    alert_data = AlertResponse(**valid_alert_data)
    await service.create_alert(alert_data)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para listar alertas filtrados
@pytest.mark.asyncio
async def test_list_alerts(mock_session, valid_alert_data):
    # Simula a resposta da consulta de listagem
    mock_session.execute.return_value.fetchall.return_value = [valid_alert_data]

    service = AlertService(session=mock_session)
    filters = AlertFilterSchema()  # Filtros vazios, sem restrições
    response = await service.get_alerts(filters)

    assert len(response) > 0
    assert response[0].measure_value == "25.5"
    assert response[0].type_alert_name == "Temperature Alert"
    assert response[0].station_name == "Station 1"


# Teste para obter um alerta específico
@pytest.mark.asyncio
async def test_get_alert(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data

    service = AlertService(session=mock_session)
    alert = await service.get_alert_by_id(1)

    assert alert.measure_value == "25.5"
    assert alert.type_alert_name == "Temperature Alert"
    assert alert.station_name == "Station 1"


# Teste para deletar um alerta
@pytest.mark.asyncio
async def test_delete_alert(mock_session, valid_alert_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    service = AlertService(session=mock_session)
    await service.delete_alert(1)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o controlador de criar alerta
@pytest.mark.asyncio
async def test_create_alert_controller(mock_session, valid_alert_data):
    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    alert_data = AlertResponse(**valid_alert_data)
    controller = AlertController(mock_session)
    response = await controller.create_alert(alert_data)

    assert response.data is None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o controlador de listar alertas
@pytest.mark.asyncio
async def test_list_alerts_controller(mock_session, valid_alert_data):
    mock_session.execute.return_value.fetchall.return_value = [valid_alert_data]

    controller = AlertController(mock_session)
    response = await controller.get_filtered_alerts(AlertFilterSchema())

    assert response.data[0].measure_value == "25.5"
    assert response.data[0].type_alert_name == "Temperature Alert"
    assert response.data[0].station_name == "Station 1"


# Teste para o controlador de obter um alerta específico
@pytest.mark.asyncio
async def test_get_alert_controller(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data

    controller = AlertController(mock_session)
    response = await controller.get_alert_by_id(1)

    assert response.data.measure_value == "25.5"
    assert response.data.type_alert_name == "Temperature Alert"
    assert response.data.station_name == "Station 1"


# Teste para o controlador de deletar um alerta
@pytest.mark.asyncio
async def test_delete_alert_controller(mock_session, valid_alert_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    controller = AlertController(mock_session)
    await controller.delete_alert(1)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o endpoint de criar alerta
def test_create_alert_endpoint(mock_session, valid_alert_data):
    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    response = client.post(
        "/alert/",
        json=valid_alert_data,
    )

    assert response.status_code == HTTPStatus.OK
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o endpoint de listar alertas
def test_list_alerts_endpoint(mock_session, valid_alert_data):
    mock_session.execute.return_value.fetchall.return_value = [valid_alert_data]

    response = client.get("/alert/all")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json().get("data")) > 0


# Teste para o endpoint de obter um alerta específico
def test_get_alert_endpoint(mock_session, valid_alert_data):
    mock_session.get.return_value = valid_alert_data

    response = client.get("/alert/1")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json().get("data")
    assert response_data["measure_value"] == "25.5"


# Teste para o endpoint de deletar um alerta
def test_delete_alert_endpoint(mock_session, valid_alert_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    response = client.delete("/alert/1")

    assert response.status_code == HTTPStatus.OK
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()
