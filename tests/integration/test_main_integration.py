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
        Idea(id='7', name='Name of idea 7', short_description='short desc for idea 7', long_description='long desc for idea 7'),
        Idea(id='\n   X', name='Name of idea X', short_description='short desc for idea X', long_description='long desc for idea X'),
        Idea(id='   9\n', name='Name of idea 9\n', short_description='short desc for idea 9\n', long_description='long desc for idea 9\n'),
    ]


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server is running."

@pytest.mark.parametrize("id, index",[ 
	("7", 0), 
	("X", 1),
    ("9", 2)
]) 
def test_get_idea_found(client: TestClient, id, index, mock_ideas):
    app.dependency_overrides[get_table] = lambda: mock_ideas
    response = client.get(f"/ideas/{id}")

    idea_json = response.json()
    mock_idea = mock_ideas[index]

    assert response.status_code == 200
    assert idea_json["id"] == mock_idea.id
    assert idea_json["name"] == mock_idea.name
    assert idea_json["short_description"] == mock_idea.short_description
    assert idea_json["long_description"] == mock_idea.long_description

    app.dependency_overrides.clear()


@pytest.mark.parametrize("id",[ 
	("  "), 
	("-1"),
    ("7 7")
]) 
def test_get_idea_not_found(client: TestClient, id, mock_ideas):
    app.dependency_overrides[get_table] = lambda: mock_ideas
    response = client.get(f"/ideas/{id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Project with id {id} not found."}

    app.dependency_overrides.clear()