from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
import pytest

from app.main import app, get_table
from app.schemas.idea import Idea


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
    client.close()

@pytest.fixture
def mock_ideas() -> list[Idea]:
    return [
        Idea(id='1', name='Name of idea 1', short_description='short desc for idea 1', long_description='long desc for idea 1'),
        Idea(id='\n   2', name='Name of idea 2', short_description='short desc for idea 2', long_description='long desc for idea 2'),
        Idea(id='   3\n', name='Name of idea 3\n', short_description='short desc for idea 3\n', long_description='long desc for idea 3\n'),
    ]

@pytest.fixture(autouse=True)
def override_get_table(mock_ideas):
    app.dependency_overrides[get_table] = lambda: mock_ideas
    yield
    app.dependency_overrides.clear()

# Can't use because it pushes!
"""
def test_post_idea(client: TestClient, mock_ideas):
    json = {
        "name": "Testidea",
        "short_description": "test short",
        "long_description": "test long"
    }
    
    response = client.post("/ideas", json=json)
    assert response.status_code == 200
    print(response.json())
    assert response.json() == jsonable_encoder(mock_ideas[3])
"""