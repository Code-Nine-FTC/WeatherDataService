import pytest
from fastapi.testclient import TestClient

from app.core.models.db_model import ParameterType
from app.dependency.database import Database

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_UNPROCESSABLE_ENTITY = 422


class TestParameterType:
    # Fixture de setup para o cliente autenticado
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_client: TestClient):
        self.client = authenticated_client

    # Testa a criação de um tipo de parâmetro com dados válidos (sem fixture)
    def test_create_parameter_type(self):
        response = self.client.post(
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

    # Testa a criação de tipo de parâmetro que já existe (inserido manualmente no banco)
    def test_create_parameter_type_conflict(self):
        # Inserção direta no banco (sem usar fixture para evitar conflitos de limpeza)
        param_type = ParameterType(
            name="Duplicado",
            detect_type="climate",
            measure_unit="m",
            qnt_decimals=2,
            offset=0.0,
            factor=1.0,
            is_active=True,
        )
        Database.session.add(param_type)
        Database.session.commit()

        response = self.client.post(
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
        assert "Tipo de parâmetro já existe" in response.json()["detail"]

        Database.session.delete(param_type)
        Database.session.commit()

    # Testa criação com corpo vazio (inválido)
    def test_create_parameter_type_invalid(self):
        response = self.client.post("/parameter_types/", json={})
        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    # Lista todos os tipos de parâmetro (precisa de dados no banco)
    def test_list_all_parameter_types(self, parameter_type_ativo):
        response = self.client.get("/parameter_types/")
        assert response.status_code == HTTP_OK
        assert isinstance(response.json()["data"], list)
        assert any(pt["id"] == parameter_type_ativo.id for pt in response.json()["data"])

    # Lista apenas os ativos (com is_active=True)
    def test_list_only_active_parameter_types(self, parameter_type_ativo):
        response = self.client.get("/parameter_types/", params={"is_active": True})
        assert response.status_code == HTTP_OK
        for item in response.json()["data"]:
            assert item["is_active"] is True

    # Filtro por nome
    def test_filter_by_name(self, parameter_type_ativo):
        response = self.client.get(
            "/parameter_types/", params={"name": parameter_type_ativo.name}
        )
        assert response.status_code == HTTP_OK
        for item in response.json()["data"]:
            assert item["name"] == parameter_type_ativo.name

    # Filtro por unidade de medida
    def test_filter_by_measure_unit(self, parameter_type_ativo):
        response = self.client.get(
            "/parameter_types/", params={"measure_unit": parameter_type_ativo.measure_unit}
        )
        assert response.status_code == HTTP_OK
        for item in response.json()["data"]:
            assert item["measure_unit"] == parameter_type_ativo.measure_unit

    # Desativar tipo de parâmetro
    def test_disable_parameter_type(self, parameter_type_ativo):
        response = self.client.patch(f"/parameter_types/{parameter_type_ativo.id}")
        assert response.status_code == HTTP_OK

        # Verifica se foi desativado mesmo
        verify = self.client.get(f"/parameter_types/{parameter_type_ativo.id}")
        assert verify.status_code == HTTP_OK
        assert verify.json()["data"]["is_active"] is False

    # Desativar parâmetro que não existe
    def test_disable_nonexistent_parameter_type(self, parameter_type_nao_existente_id):
        response = self.client.patch(f"/parameter_types/{parameter_type_nao_existente_id}")
        assert response.status_code == HTTP_NOT_FOUND

    # Buscar tipo de parâmetro por ID válido
    def test_get_parameter_type_by_id(self, parameter_type_ativo):
        response = self.client.get(f"/parameter_types/{parameter_type_ativo.id}")
        assert response.status_code == HTTP_OK
        data = response.json()["data"]
        assert data["id"] == parameter_type_ativo.id
        assert data["name"] == parameter_type_ativo.name

    # Buscar por ID inexistente
    def test_get_nonexistent_parameter_type(self, parameter_type_nao_existente_id):
        response = self.client.get(f"/parameter_types/{parameter_type_nao_existente_id}")
        assert response.status_code == HTTP_NOT_FOUND

    # Atualização de tipo de parâmetro existente
    def test_update_parameter_type(self, parameter_type_ativo):
        response = self.client.patch(
            f"/parameter_types/{parameter_type_ativo.id}/update",
            json={
                "name": "Temperatura Atualizada",
                "measure_unit": "K",
                "qnt_decimals": 3,
                "offset": 1.0,
                "factor": 2.0,
            },
        )
        assert response.status_code == HTTP_OK

        verify = self.client.get(f"/parameter_types/{parameter_type_ativo.id}")
        assert verify.status_code == HTTP_OK
        data = verify.json()["data"]
        assert data["name"] == "Temperatura Atualizada"
        assert data["measure_unit"] == "K"
        assert data["qnt_decimals"] == 3

    # Atualizar parâmetro inexistente
    def test_update_nonexistent_parameter_type(self, parameter_type_nao_existente_id):
        response = self.client.patch(
            f"/parameter_types/{parameter_type_nao_existente_id}/update",
            json={"name": "Novo nome"},
        )
        assert response.status_code == HTTP_NOT_FOUND
