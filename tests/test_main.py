from http import HTTPStatus

from fastapi.testclient import TestClient

import main

client = TestClient(main)  # arrange  ( organização)

response = client.get("/rotaquevcvaitestar")  # act (ação)

assert response.status_code == HTTPStatus.OK  # Assert
