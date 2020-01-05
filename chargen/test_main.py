import pytest
from starlette.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_cod_seeded():
    response = client.get("/cod/helloworld")
    assert response.status_code == 200


def test_get_mtwa2_seeded():
    response = client.get("/mtaw2/helloworld")
    assert response.status_code == 200
