from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
import pytest


def test_get_all_ideas_no_query_parameter(client: TestClient, get_ideas_test_repo):
    response = client.get("/ideas")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(get_ideas_test_repo.get_ideas())

"""
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
    (".."),
    (True),
    (False)
]) 
def test_get_ideas_non_int_parameter(client: TestClient, query_parameter):
    response = client.get(f"/ideas?first_n={query_parameter}")
    assert response.status_code == 422
"""