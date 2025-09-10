from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
import pytest


def test_post_ideas(client: TestClient, get_ideas_test_repo):
    json = {
        "name": "Testidea",
        "short_description": "test short",
        "long_description": "test long",
    }

    response = client.post("/ideas", json=json)
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(get_ideas_test_repo.get_ideas()[3])
