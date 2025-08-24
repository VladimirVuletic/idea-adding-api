from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
import pytest

from typing import Optional

from app.core.dependencies import get_ideas_file_repo
from app.main import app
from app.services.ideas_repository import IdeasRepository
from app.schemas.idea import Idea
from app.schemas.idea_create import IdeaCreate
from app.schemas.idea_update import IdeaUpdate


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
    client.close()

class IdeasTestRepository(IdeasRepository):
    def __init__(self, ideas: list[Idea] = None):
        self._ideas = [
            Idea(id='1', name='Name of idea 1', short_description='short desc for idea 1', long_description='long desc for idea 1'),
            Idea(id='\n   2', name='Name of idea 2', short_description='short desc for idea 2', long_description='long desc for idea 2'),
            Idea(id='   3\n', name='Name of idea 3\n', short_description='short desc for idea 3\n', long_description='long desc for idea 3\n'),
        ]
        
    def get_ideas(self) -> list[Idea]:
        return self._ideas
    
    def get_idea(self, id: str) -> Optional[Idea]:
        id = id.strip()
        return next((i for i in self._ideas if i.id.strip() == id), None)

    
    def add_idea(self, new_idea: IdeaCreate) -> Optional[Idea]:
        ...
    
    def update_idea(self, id: str, updated_idea: IdeaUpdate) -> Optional[Idea]:
        ...
    
    def delete_idea(self, id: str) -> Optional[Idea]:
        ...

@pytest.fixture
def get_ideas_test_repo() -> IdeasTestRepository:
    return IdeasTestRepository()

@pytest.fixture(autouse=True)
def override_get_ideas_file_repo(get_ideas_test_repo):
    app.dependency_overrides[get_ideas_file_repo] = lambda: get_ideas_test_repo
    yield
    app.dependency_overrides.clear()

@pytest.mark.parametrize("id", [
    ("1"), 
    ("2"), 
    ("3")
])
def test_get_idea_found(client: TestClient, id, get_ideas_test_repo):
    response = client.get(f"/ideas/{id}")

    assert response.status_code == 200
    assert response.json() == jsonable_encoder(get_ideas_test_repo.get_idea(id))

@pytest.mark.parametrize("id", [
    ("x"), 
    ("32"),
    ("."), # returns 200, should fix
    (""), # returns 200, should fix
    (" "),
    ("-1"),
    ("7 7"),
    (True),
    (False)
])
def test_get_idea_not_found(client: TestClient, id, get_ideas_test_repo):
    response = client.get(f"/ideas/{id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Project with id {id} not found."}

"""
@pytest.mark.parametrize("id",[ 
	("7"), 
	("X"),
    ("7 7"),
    (True)
]) 
def test_get_idea_from_empty_list(client: TestClient, id):
    app.dependency_overrides[get_table] = lambda: []
    try:
        response = client.get(f"/ideas/{id}")
        assert response.status_code == 404
        assert response.json() == {"detail": f"Project with id {id} not found."}
    finally:
        app.dependency_overrides.clear()
"""