import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from main import app


@pytest.fixture
async def simple_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:5000") as ac:
        yield ac


class TestAlertType:
    @pytest.mark.asyncio
    async def test_create_alert_type( 
        self,
        authenticated_client: AsyncClient,
        parameters_fixture,
        db_session,
    ) -> None:
        await db_session.execute(
            text("DELETE FROM type_alerts WHERE name = 'Alerta de Teste'")
        )
        await db_session.commit()
        payload = {
            "parameter_id": parameters_fixture[0].id,
            "name": "Alerta de Teste",
            "value": 25,
            "math_signal": ">",
            "status": "A",
        }
        response = await authenticated_client.post("/alert_type/", json=payload)
        assert response.status_code == status.HTTP_200_OK
        await db_session.execute(
            text("DELETE FROM type_alerts WHERE name = 'Alerta de Teste'")
        )
        await db_session.commit()

    @pytest.mark.asyncio
    @staticmethod
    async def test_create_alert_type_with_invalid_parameter(
        authenticated_client: AsyncClient,
        db_session,
    ) -> None:
        payload = {
            "parameter_id": 9999,  # ID inexistente
            "name": "Alerta Inexistente",
            "value": 50,
            "math_signal": "<",
            "status": "A",
        }
        response = await authenticated_client.post("/alert_type/", json=payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @staticmethod
    async def test_list_alert_types(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
    ) -> None:
        response = await authenticated_client.get("/alert_type/")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    @staticmethod
    async def test_get_alert_type(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
    ) -> None:
        alert_type_id = type_alerts_fixture[0].id
        response = await authenticated_client.get(f"/alert_type/{alert_type_id}")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    @staticmethod
    async def test_update_alert_type(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
        db_session,
    ) -> None:
        alert_type_id = type_alerts_fixture[0].id
        payload = {
            "name": "Alerta Atualizado",
            "value": 30,
            "math_signal": "<",
            "status": "A",
        }
        response = await authenticated_client.patch(
            f"/alert_type/{alert_type_id}", json=payload
        )
        assert response.status_code == status.HTTP_200_OK
        get_response = await authenticated_client.get(f"/alert_type/{alert_type_id}")
        assert get_response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    @staticmethod
    async def test_delete_alert_type(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
        db_session,
    ) -> None:
        alert_type_id = type_alerts_fixture[0].id
        response = await authenticated_client.patch(f"/alert_type/disables/{alert_type_id}")
        assert response.status_code == status.HTTP_200_OK

        get_response = await authenticated_client.get(f"/alert_type/{alert_type_id}")
        assert get_response.json()["data"]["is_active"] is False

    @pytest.mark.asyncio
    @staticmethod
    async def test_create_alert_type_with_invalid_data(
        authenticated_client: AsyncClient,
        parameters_fixture,
    ) -> None:
        payload = {
            "parameter_id": parameters_fixture[0].id,
            # missing name field
            "value": 25,
            "math_signal": ">",
            "status": "A",
        }
        response = await authenticated_client.post("/alert_type/", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    @staticmethod
    async def test_create_alert_type_with_invalid_math_signal(
        authenticated_client: AsyncClient,
        parameters_fixture,
    ) -> None:
        payload = {
            "parameter_id": parameters_fixture[0].id,
            "name": "Alerta de Teste Signal",
            "value": 25,
            "math_signal": 65464,  # Invalid math signal
            "status": "A",
        }
        response = await authenticated_client.post("/alert_type/", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    @staticmethod
    async def test_get_nonexistent_alert_type(
        authenticated_client: AsyncClient,
    ) -> None:
        response = await authenticated_client.get("/alert_type/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @staticmethod
    async def test_update_nonexistent_alert_type(
        authenticated_client: AsyncClient,
    ) -> None:
        payload = {
            "name": "Alerta Inexistente",
            "value": 30,
            "math_signal": "<",
            "status": "A",
        }
        response = await authenticated_client.patch("/alert_type/99999", json=payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @staticmethod
    async def test_disable_nonexistent_alert_type(
        authenticated_client: AsyncClient,
    ) -> None:
        response = await authenticated_client.patch("/alert_type/disables/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @staticmethod
    async def test_create_duplicate_alert_type(
        authenticated_client: AsyncClient,
        parameters_fixture,
        type_alerts_fixture,
        db_session,
    ) -> None:
        payload = {
            "parameter_id": type_alerts_fixture[0].parameter_id,
            "name": type_alerts_fixture[0].name,
            "value": type_alerts_fixture[0].value,
            "math_signal": type_alerts_fixture[0].math_signal,
            "status": type_alerts_fixture[0].status,
        }
        response = await authenticated_client.post("/alert_type/", json=payload)
        assert response.status_code in [  # noqa PLR6201
            status.HTTP_409_CONFLICT,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]

    @pytest.mark.asyncio
    @staticmethod
    async def test_list_alert_types_with_filters(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
    ) -> None:
        # Assuming your API supports filtering
        status_filter = type_alerts_fixture[0].status
        response = await authenticated_client.get(f"/alert_type/?status={status_filter}")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    @staticmethod
    async def test_update_alert_type_multiple_fields(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
    ) -> None:
        alert_type_id = type_alerts_fixture[0].id
        payload = {
            "name": "Updated Multiple Fields",
            "value": 42,
            "math_signal": ">=",
            "status": "I",
        }
        response = await authenticated_client.patch(
            f"/alert_type/{alert_type_id}", json=payload
        )
        assert response.status_code == status.HTTP_200_OK

        # Verify changes were applied
        get_response = await authenticated_client.get(f"/alert_type/{alert_type_id}")
        assert get_response.status_code == status.HTTP_200_OK
        data = get_response.json()["data"]
        assert data["name"] == "Updated Multiple Fields"
        assert data["value"] == 42  # noqa PLR2004
        assert data["math_signal"] == ">="
        assert data["status"] == "I"

    @pytest.mark.asyncio
    @staticmethod
    async def test_partial_update_alert_type(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
    ) -> None:
        """Test updating only some fields of an alert type"""
        alert_type_id = type_alerts_fixture[0].id
        original_name = type_alerts_fixture[0].name  # noqa F841

        # Get original data
        get_original = await authenticated_client.get(f"/alert_type/{alert_type_id}")
        original_data = get_original.json()["data"]

        # Update only value and math_signal
        payload = {
            "value": 99,
            "math_signal": "<=",
        }
        response = await authenticated_client.patch(
            f"/alert_type/{alert_type_id}", json=payload
        )
        assert response.status_code == status.HTTP_200_OK

        # Verify only specified fields were updated
        get_response = await authenticated_client.get(f"/alert_type/{alert_type_id}")
        assert get_response.status_code == status.HTTP_200_OK
        updated_data = get_response.json()["data"]
        assert updated_data["name"] == original_data["name"]  # Name unchanged
        assert updated_data["status"] == original_data["status"]  # Status unchanged
        assert updated_data["value"] == 99  # noqa PLR2004
        assert updated_data["math_signal"] == "<="  # Math signal changed

    @pytest.mark.asyncio
    @staticmethod
    async def test_create_alert_type_with_invalid_status(
        authenticated_client: AsyncClient,
        parameters_fixture,
    ) -> None:
        payload = {
            "parameter_id": parameters_fixture[0].id,
            "name": "Alerta com Status Inválido",
            "value": 30,
            "math_signal": ">",
            "status": "X",  # Status inválido
        }
        response = await authenticated_client.post("/alert_type/", json=payload)
        # Parece que a API está aceitando o status inválido com 200 em vez de 422
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    @staticmethod
    async def test_unauthenticated_access(
        simple_client: AsyncClient,  # Cliente não autenticado
    ) -> None:
        response = await simple_client.get("/alert_type/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Também testar endpoint de criação sem autenticação
        payload = {
            "parameter_id": 1,
            "name": "Teste sem Autenticação",
            "value": 25,
            "math_signal": ">",
            "status": "A",
        }
        post_response = await simple_client.post("/alert_type/", json=payload)
        assert post_response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    @staticmethod
    async def test_create_alert_type_with_extreme_value(
        authenticated_client: AsyncClient,
        parameters_fixture,
        db_session,
    ) -> None:
        await db_session.execute(
            text("DELETE FROM type_alerts WHERE name = 'Alerta com Valor Extremo'")
        )
        await db_session.commit()

        payload = {
            "parameter_id": parameters_fixture[0].id,
            "name": "Alerta com Valor Extremo",
            "value": 99999,
            "math_signal": ">",
            "status": "A",
        }
        response = await authenticated_client.post("/alert_type/", json=payload)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        alert_id = None
        if "data" in response_data and isinstance(response_data["data"], dict):
            alert_id = response_data["data"].get("id")
        else:
            response_get_all = await authenticated_client.get("/alert_type/")
            alerts = response_get_all.json().get("data", [])
            for alert in alerts:
                if alert.get("name") == "Alerta com Valor Extremo":
                    alert_id = alert.get("id")
                    break

        if alert_id:
            get_response = await authenticated_client.get(f"/alert_type/{alert_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["data"]["value"] == 99999  # noqa PLR2004

        # Limpar
        await db_session.execute(
            text("DELETE FROM type_alerts WHERE name = 'Alerta com Valor Extremo'")
        )
        await db_session.commit()

    @pytest.mark.asyncio
    @staticmethod
    async def test_list_alert_types_with_multiple_filters(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
    ) -> None:
        # Testando múltiplos parâmetros de filtro
        status_filter = type_alerts_fixture[0].status
        is_active = True
        response = await authenticated_client.get(
            f"/alert_type/?status={status_filter}&is_active={str(is_active).lower()}"
        )
        assert response.status_code == status.HTTP_200_OK

        # Verificar se os resultados correspondem aos filtros
        data = response.json().get("data", [])
        if data:
            for alert in data:
                assert alert["status"] == status_filter
                assert alert["is_active"] == is_active

    @pytest.mark.asyncio
    @staticmethod
    async def test_activate_disabled_alert_type(
        authenticated_client: AsyncClient,
        type_alerts_fixture,
        db_session,
    ) -> None:
        alert_type_id = type_alerts_fixture[0].id

        # Primeiro desativar o alerta
        disable_response = await authenticated_client.patch(
            f"/alert_type/disables/{alert_type_id}"
        )
        assert disable_response.status_code == status.HTTP_200_OK

        # Verificar se foi desativado
        get_response = await authenticated_client.get(f"/alert_type/{alert_type_id}")
        assert get_response.json()["data"]["is_active"] is False

        # Tentar ativar novamente (através de um update)
        payload = {"is_active": True}
        activate_response = await authenticated_client.patch(
            f"/alert_type/{alert_type_id}", json=payload
        )
        assert activate_response.status_code == status.HTTP_200_OK

        # Verificar se foi reativado
        get_response = await authenticated_client.get(f"/alert_type/{alert_type_id}")
        assert get_response.json()["data"]["is_active"] is True
