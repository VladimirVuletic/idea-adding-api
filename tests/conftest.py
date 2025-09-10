from typing import Optional

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import get_git_client, get_ideas_file_repo
from app.main import app
from app.schemas.idea import Idea
from app.schemas.idea_create import IdeaCreate
from app.schemas.idea_update import IdeaUpdate
from app.services.ideas_repository import IdeasRepository


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
    client.close()


class IdeasTestRepository(IdeasRepository):
    def __init__(self, ideas: list[Idea] = None):
        self._ideas = [
            Idea(
                id="1",
                name="Name of idea 1",
                short_description="short desc for idea 1",
                long_description="long desc for idea 1",
            ),
            Idea(
                id="\n   2",
                name="Name of idea 2",
                short_description="short desc for idea 2",
                long_description="long desc for idea 2",
            ),
            Idea(
                id="   3\n",
                name="Name of idea 3\n",
                short_description="short desc for idea 3\n",
                long_description="long desc for idea 3\n",
            ),
        ]

    def get_ideas(self) -> list[Idea]:
        return self._ideas

    def get_idea(self, id: str) -> Optional[Idea]:
        id = id.strip()
        return next((i for i in self._ideas if i.id.strip() == id), None)

    def add_idea(self, new_idea: IdeaCreate) -> Optional[Idea]:
        ideas = self.get_ideas()

        idea_id = max(int(idea.id.strip()) for idea in ideas) + 1
        idea = Idea(
            id=str(idea_id),
            name=new_idea.name,
            short_description=new_idea.short_description,
            long_description=new_idea.long_description,
        )

        ideas.append(idea)

        return idea

    def update_idea(self, id: str, updated_idea: IdeaUpdate) -> Optional[Idea]:
        idea = self.get_idea(id)

        if updated_idea.name is not None:
            idea.name = updated_idea.name
        if updated_idea.short_description is not None:
            idea.short_description = updated_idea.short_description
        if updated_idea.long_description is not None:
            idea.long_description = updated_idea.long_description

        return idea

    def delete_idea(self, id: str) -> Optional[Idea]: ...


class GitTestClient:
    def push_changes(self, commit_message):
        print(f"Fake commit: {commit_message}")


@pytest.fixture
def get_ideas_test_repo() -> IdeasTestRepository:
    return IdeasTestRepository()


@pytest.fixture(autouse=True)
def override_get_ideas_file_repo(get_ideas_test_repo):
    app.dependency_overrides[get_ideas_file_repo] = lambda: get_ideas_test_repo
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def get_git_test_client() -> GitTestClient:
    return GitTestClient()


@pytest.fixture(autouse=True)
def override_get_git_client(get_git_test_client):
    app.dependency_overrides[get_git_client] = lambda: get_git_test_client
    yield
    app.dependency_overrides.clear()
