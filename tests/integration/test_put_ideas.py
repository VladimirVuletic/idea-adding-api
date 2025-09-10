import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient


def test_put_ideas(client: TestClient, get_ideas_test_repo):
    id = "1"
    json = {"name": "Name of idea 1 UPDATED"}

    response = client.put(f"/ideas/{id}", json=json)
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(get_ideas_test_repo.get_ideas()[0])
