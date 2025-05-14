import pytest
from fastapi.testclient import TestClient

from app.core.models.db_model import ParameterType

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_UNPROCESSABLE_ENTITY = 422
QNT_DECIMALS_UPDATED = 3


# 1. POST - Criação de tipo de parâmetro
def test_create_parameter_type(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/parameter_types/",
        json={
            "name": "Umidade",
            "detect_type": "climate",
            "measure_unit": "%",
            "qnt_decimals": 1,
            "offset": 0.0,
            "factor": 1.0,
        },
    )
    assert response.status_code == HTTP_OK
    assert response.json() == {"data": None}


# 2. POST - Tipo de parâmetro duplicado
@pytest.mark.asyncio
async def test_create_parameter_type_conflict(authenticated_client: TestClient, db_session):
    param_type = ParameterType(
        name="Duplicado",
        detect_type="climate",
        measure_unit="m",
        qnt_decimals=2,
        offset=0.0,
        factor=1.0,
        is_active=True,
    )
    db_session.add(param_type)
    await db_session.commit()

    response = authenticated_client.post(
        "/parameter_types/",
        json={
            "name": "Duplicado",
            "detect_type": "climate",
            "measure_unit": "m",
            "qnt_decimals": 2,
            "offset": 0.0,
            "factor": 1.0,
        },
    )

    assert response.status_code == HTTP_CONFLICT
    assert "Tipo de parâmetro já existe" in response.json().get("detail", "")

    await db_session.delete(param_type)
    await db_session.commit()


# 3. POST - Corpo vazio
def test_create_parameter_type_invalid(authenticated_client: TestClient):
    response = authenticated_client.post("/parameter_types/", json={})
    assert response.status_code == HTTP_UNPROCESSABLE_ENTITY


# 4. GET - Lista todos os tipos de parâmetro
def test_list_all_parameter_types(authenticated_client: TestClient):
    response = authenticated_client.get("/parameter_types/")
    assert response.status_code == HTTP_OK
    assert isinstance(response.json()["data"], list)


# 5. GET - Filtra tipos de parâmetro ativos
def test_list_only_active_parameter_types(authenticated_client: TestClient):
    response = authenticated_client.get("/parameter_types/", params={"is_active": True})
    assert response.status_code == HTTP_OK
    for item in response.json()["data"]:
        assert item["is_active"] is True


# 6. GET - Filtra tipos de parâmetro por nome
def test_filter_by_name(authenticated_client: TestClient):
    response = authenticated_client.get("/parameter_types/", params={"name": "Umidade"})
    assert response.status_code == HTTP_OK
    for item in response.json()["data"]:
        assert item["name"] == "Umidade"


# 7. PATCH - Atualizar tipo de parâmetro existente
def test_update_parameter_type(authenticated_client: TestClient, db_session):
    param_type = ParameterType(
        name="Temperatura",
        detect_type="climate",
        measure_unit="C",
        qnt_decimals=2,
        offset=0.0,
        factor=1.0,
        is_active=True,
    )
    db_session.add(param_type)
    db_session.commit()

    response = authenticated_client.patch(
        f"/parameter_types/{param_type.id}/update",
        json={
            "name": "Temperatura Atualizada",
            "measure_unit": "K",
            "qnt_decimals": QNT_DECIMALS_UPDATED,
            "offset": 1.0,
            "factor": 2.0,
        },
    )

    assert response.status_code == HTTP_OK

    updated_param_type = db_session.query(ParameterType).get(param_type.id)
    assert updated_param_type.name == "Temperatura Atualizada"
    assert updated_param_type.measure_unit == "K"
    assert updated_param_type.qnt_decimals == QNT_DECIMALS_UPDATED

    db_session.delete(updated_param_type)
    db_session.commit()


# 8. PATCH - Atualizar tipo de parâmetro inexistente
def test_update_nonexistent_parameter_type(authenticated_client: TestClient):
    response = authenticated_client.patch(
        "/parameter_types/999999/update", json={"name": "Novo nome"}
    )
    assert response.status_code == HTTP_NOT_FOUND
