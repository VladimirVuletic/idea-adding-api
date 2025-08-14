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
        Idea(id='7', name='Name of idea 7', short_description='short desc for idea 7', long_description='long desc for idea 7'),
        Idea(id='\n   X', name='Name of idea X', short_description='short desc for idea X', long_description='long desc for idea X'),
        Idea(id='   9\n', name='Name of idea 9\n', short_description='short desc for idea 9\n', long_description='long desc for idea 9\n'),
    ]

@pytest.fixture(autouse=True)
def override_get_table(mock_ideas):
    app.dependency_overrides[get_table] = lambda: mock_ideas
    yield
    app.dependency_overrides.clear()


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
    response = client.get(f"/ideas/{id}")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_ideas[index])

@pytest.mark.parametrize("id",[ 
	("  "), 
	("-1"),
    ("7 7"),
    ("1")
]) 
def test_get_idea_not_found(client: TestClient, id):    
    response = client.get(f"/ideas/{id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Project with id {id} not found."}

@pytest.mark.parametrize("id",[ 
	("7"), 
	("X"),
    ("7 7")
]) 
def test_get_idea_from_empty_list(client: TestClient, id):
    app.dependency_overrides[get_table] = lambda: []
    try:
        response = client.get(f"/ideas/{id}")
        assert response.status_code == 404
        assert response.json() == {"detail": f"Project with id {id} not found."}
    finally:
        app.dependency_overrides.clear()

def test_get_all_ideas_no_query_parameter(client: TestClient, mock_ideas):
    response = client.get("/ideas")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_ideas)

def test_get_all_ideas_exact_query_parameter(client: TestClient, mock_ideas):
    query_parameter = len(mock_ideas)
    response = client.get(f"/ideas?first_n={query_parameter}")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_ideas)

def test_get_all_ideas_query_parameter_larger_than_list_len(client: TestClient, mock_ideas):
    query_parameter = len(mock_ideas) + 5
    response = client.get(f"/ideas?first_n={query_parameter}")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_ideas)

def test_get_no_ideas_query_parameter_zero(client: TestClient):
    response = client.get(f"/ideas?first_n=0")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder([])

def test_get_ideas_negative_parameter(client: TestClient):
    query_parameter = -1
    response = client.get(f"/ideas?first_n={query_parameter}")
    assert response.status_code == 400
    assert response.json() == {"detail": f"Invalid query parameter: {query_parameter}."}

@pytest.mark.parametrize("query_parameter",[ 
	("  "), 
	("s"),
    ("!"),
    ("..")
]) 
def test_get_ideas_non_int_parameter(client: TestClient, query_parameter):
    response = client.get(f"/ideas?first_n={query_parameter}")
    assert response.status_code == 422
