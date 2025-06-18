import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import text


class TestAlertType:
    @pytest.mark.asyncio
    @staticmethod
    async def test_create_alert_type(
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
