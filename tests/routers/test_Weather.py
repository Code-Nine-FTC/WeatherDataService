from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from main import app  # Certifique-se de importar a instância correta do seu app

# Inicializando o TestClient com a instância app importada do arquivo main
client = TestClient(app)


# Fixture para fornecer dados de payload para criação de uma estação
@pytest.fixture
def valid_station_payload():
    return {
        "name": "Estação A",
        "uid": "unique-uid-1234",
        "latitude": 10.12345,
        "longitude": -20.12345,
        "address": {"city": "Cidade A", "state": "Estado A", "country": "Brasil"},
        "parameter_types": [1, 2],
    }


@pytest.fixture
def valid_update_station_payload():
    return {
        "name": "Estação Atualizada",
        "uid": "updated-uid-1234",
        "latitude": 12.34567,
        "longitude": -22.34567,
        "address": {
            "city": "Cidade Atualizada",
            "state": "Estado Atualizado",
            "country": "Brasil",
        },
        "parameter_types": [2],
    }


# Fixture para realizar o login e obter um token de autenticação
@pytest.fixture
def auth_token():
    # Dados de login do usuário
    login_data = {
        "username": "admcodenine@gmail.com",  # Substitua com o e-mail de teste
        "password": "adm2025",  # Substitua com a senha de teste
    }

    # Fazer a requisição de login
    response = client.post(
        "/auth/login", data=login_data
    )  # Supondo que o login usa x-www-form-urlencoded
    assert response.status_code == HTTPStatus.OK

    # Retornar o token de autenticação
    return response.json().get("access_token")


# Teste para criar uma estação
def test_create_station(valid_station_payload, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}"  # Incluindo o token JWT nos cabeçalhos
    }

    response = client.post("/stations/", json=valid_station_payload, headers=headers)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"data": None}


# Teste para obter estações com filtros
def test_get_filtered_stations(auth_token):
    params = {"name": "Estação A", "status": True}
    headers = {
        "Authorization": f"Bearer {auth_token}"  # Incluindo o token JWT nos cabeçalhos
    }

    response = client.get("/stations/filters", params=params, headers=headers)
    assert response.status_code == HTTPStatus.OK
    stations = response.json().get("data", [])
    assert isinstance(stations, list)
    assert len(stations) > 0
    assert stations[0]["name_station"] == "Estação A"


# Teste para obter uma estação por ID
def test_get_station_by_id(auth_token):
    # Aqui você deve substituir '1' pelo ID válido da estação
    station_id = 1
    headers = {
        "Authorization": f"Bearer {auth_token}"  # Incluindo o token JWT nos cabeçalhos
    }

    response = client.get(f"/stations/{station_id}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    station = response.json().get("data", {})
    assert station["id"] == station_id
    assert station["name_station"] == "Estação A"


# Teste para atualizar os dados de uma estação
def test_update_station(valid_update_station_payload, auth_token):
    # Substitua '1' pelo ID da estação que você quer testar
    station_id = 1
    headers = {
        "Authorization": f"Bearer {auth_token}"  # Incluindo o token JWT nos cabeçalhos
    }

    response = client.patch(
        f"/stations/{station_id}", json=valid_update_station_payload, headers=headers
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"data": None}


# Teste para remover um parâmetro de uma estação
def test_remove_parameter(auth_token):
    # Substitua pelos IDs válidos
    station_id = 1
    parameter_id = 1
    headers = {
        "Authorization": f"Bearer {auth_token}"  # Incluindo o token JWT nos cabeçalhos
    }

    response = client.patch(
        f"/stations/{station_id}/parameter/{parameter_id}", headers=headers
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"data": None}


# Teste para desabilitar uma estação
def test_disable_station(auth_token):
    # Substitua '1' pelo ID da estação que você deseja desabilitar
    station_id = 1
    headers = {
        "Authorization": f"Bearer {auth_token}"  # Incluindo o token JWT nos cabeçalhos
    }

    response = client.patch(f"/stations/disable/{station_id}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"data": None}


# Teste para obter parâmetros de uma estação
def test_get_parameters_by_station(auth_token):
    # Substitua '1' pelo ID do parâmetro que deseja consultar
    type_parameter_id = 1
    headers = {
        "Authorization": f"Bearer {auth_token}"  # Incluindo o token JWT nos cabeçalhos
    }

    response = client.get(f"/stations/parameters/{type_parameter_id}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    parameters = response.json().get("data", [])
    assert isinstance(parameters, list)
    assert len(parameters) > 0
