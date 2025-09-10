import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient


@pytest.mark.parametrize("id", [("1"), ("2"), ("3")])
def test_get_idea_found(client: TestClient, id, get_ideas_test_repo):
    response = client.get(f"/ideas/{id}")

    assert response.status_code == 200
    assert response.json() == jsonable_encoder(get_ideas_test_repo.get_idea(id))


@pytest.mark.parametrize(
    "id",
    [
        ("x"),
        ("32"),
        ("."),  # returns 200, should fix
        (""),  # returns 200, should fix
        (" "),
        ("-1"),
        ("7 7"),
        (True),
        (False),
    ],
)
def test_get_idea_not_found(client: TestClient, id):
    response = client.get(f"/ideas/{id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Project with id {id} not found."}


@pytest.mark.parametrize(
    "id",
    [
        ("1"),
        ("X"),
        ("."),  # returns 200, should fix
        (""),  # returns 200, should fix
        ("2 2"),
        (True),
    ],
)
def test_get_idea_from_empty_list(client: TestClient, id, get_ideas_test_repo):
    get_ideas_test_repo._ideas = []

    response = client.get(f"/ideas/{id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Project with id {id} not found."}
