import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
    client.close()


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server is running."
