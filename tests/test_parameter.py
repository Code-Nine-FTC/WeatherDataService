from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

import app
from app.schemas.parameter_type import (
    CreateParameterType,
    UpdateParameterType,
)
from app.service.parameter_type import ParameterTypeService

client = TestClient(app)


@pytest.fixture
def mock_session():
    session = MagicMock(AsyncSession)
    return session


@pytest.fixture
def valid_parameter_data():
    return {
        "id": 1,
        "name": "Temperature",
        "measure_unit": "Celsius",
        "qnt_decimals": 2,
        "offset": 0,
        "factor": 1,
        "is_active": True,
    }


# Teste para criar um novo tipo de parâmetro
@pytest.mark.asyncio
async def test_create_parameter_type(mock_session, valid_parameter_data):
    service = ParameterTypeService(session=mock_session)

    # Simula a criação do parâmetro
    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    data = CreateParameterType(**valid_parameter_data)
    await service.create_parameter_type(data)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para listar tipos de parâmetros
@pytest.mark.asyncio
async def test_list_parameter_types(mock_session, valid_parameter_data):
    # Simula a resposta da consulta de listagem
    mock_session.execute.return_value.fetchall.return_value = [valid_parameter_data]

    service = ParameterTypeService(session=mock_session)
    filters = {}  # Filtros vazios, sem restrições
    response = await service.list_parameter_types(filters)

    assert len(response) > 0
    assert response[0].name == "Temperature"
    assert response[0].measure_unit == "Celsius"


# Teste para obter um tipo de parâmetro específico
@pytest.mark.asyncio
async def test_get_parameter_type(mock_session, valid_parameter_data):
    mock_session.get.return_value = valid_parameter_data

    service = ParameterTypeService(session=mock_session)
    parameter_type = await service.get_parameter_type(1)

    assert parameter_type.name == "Temperature"
    assert parameter_type.measure_unit == "Celsius"
    assert parameter_type.id == 1


# Teste para desativar um tipo de parâmetro
@pytest.mark.asyncio
async def test_delete_parameter_type(mock_session, valid_parameter_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    service = ParameterTypeService(session=mock_session)
    await service.delete_parameter_type(1)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para atualizar um tipo de parâmetro
@pytest.mark.asyncio
async def test_update_parameter_type(mock_session, valid_parameter_data):
    mock_session.get.return_value = valid_parameter_data
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    update_data = UpdateParameterType(name="New Name")
    service = ParameterTypeService(session=mock_session)
    await service.update_parameter_type(1, update_data)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o controlador de criar tipo de parâmetro
@pytest.mark.asyncio
async def test_create_parameter_type_controller(mock_session, valid_parameter_data):
    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    data = CreateParameterType(**valid_parameter_data)
    controller = ParameterTypeController(mock_session)
    response = await controller.create_parameter_type(data)

    assert response.data is None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o controlador de listar tipos de parâmetros
@pytest.mark.asyncio
async def test_list_parameter_types_controller(mock_session, valid_parameter_data):
    mock_session.execute.return_value.fetchall.return_value = [valid_parameter_data]

    controller = ParameterTypeController(mock_session)
    response = await controller.list_parameter_types({})

    assert response.data[0].name == "Temperature"
    assert response.data[0].measure_unit == "Celsius"


# Teste para o controlador de obter um tipo de parâmetro
@pytest.mark.asyncio
async def test_get_parameter_type_controller(mock_session, valid_parameter_data):
    mock_session.get.return_value = valid_parameter_data

    controller = ParameterTypeController(mock_session)
    response = await controller.get_parameter_type(1)

    assert response.data.name == "Temperature"
    assert response.data.measure_unit == "Celsius"
    assert response.data.id == 1


# Teste para o controlador de desativar um tipo de parâmetro
@pytest.mark.asyncio
async def test_delete_parameter_type_controller(mock_session, valid_parameter_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    controller = ParameterTypeController(mock_session)
    await controller.disable_parameter_type(1)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o controlador de atualizar um tipo de parâmetro
@pytest.mark.asyncio
async def test_update_parameter_type_controller(mock_session, valid_parameter_data):
    mock_session.get.return_value = valid_parameter_data
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    update_data = UpdateParameterType(name="Updated Name")
    controller = ParameterTypeController(mock_session)
    await controller.update_parameter_type(1, update_data)

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o endpoint de criar tipo de parâmetro
def test_create_parameter_type_endpoint(mock_session, valid_parameter_data):
    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    mock_session.commit.return_value = None

    response = client.post(
        "/parameter_types/",
        json=valid_parameter_data,
    )

    assert response.status_code == HTTPStatus.OK
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o endpoint de listar tipos de parâmetros
def test_list_parameter_types_endpoint(mock_session, valid_parameter_data):
    mock_session.execute.return_value.fetchall.return_value = [valid_parameter_data]

    response = client.get("/parameter_types/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json().get("data")) > 0


# Teste para o endpoint de obter um tipo de parâmetro
def test_get_parameter_type_endpoint(mock_session, valid_parameter_data):
    mock_session.get.return_value = valid_parameter_data

    response = client.get("/parameter_types/1")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json().get("data")
    assert response_data["name"] == "Temperature"


# Teste para o endpoint de desativar um tipo de parâmetro
def test_delete_parameter_type_endpoint(mock_session, valid_parameter_data):
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    response = client.patch("/parameter_types/1")

    assert response.status_code == HTTPStatus.OK
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Teste para o endpoint de atualizar um tipo de parâmetro
def test_update_parameter_type_endpoint(mock_session, valid_parameter_data):
    mock_session.get.return_value = valid_parameter_data
    mock_session.execute.return_value = None
    mock_session.commit.return_value = None

    update_data = {
        "name": "Updated Parameter",
        "measure_unit": "Fahrenheit",
    }

    response = client.patch("/parameter_types/1/update", json=update_data)

    assert response.status_code == HTTPStatus.OK
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()
