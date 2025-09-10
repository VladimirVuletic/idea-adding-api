import pytest
from fastapi import HTTPException

from app.main import get_idea
from app.schemas.idea import Idea


@pytest.fixture
def mock_ideas() -> list[Idea]:
    return [
        Idea(
            id="7",
            name="Name of idea 7",
            short_description="short desc for idea 7",
            long_description="long desc for idea 7",
        ),
        Idea(
            id="\n   X",
            name="Name of idea X",
            short_description="short desc for idea X",
            long_description="long desc for idea X",
        ),
        Idea(
            id="   9\n",
            name="Name of idea 9\n",
            short_description="short desc for idea 9\n",
            long_description="long desc for idea 9\n",
        ),
    ]


@pytest.mark.parametrize("id, index", [("7", 0), ("X", 1), ("9", 2)])
def test_get_idea_found(id, index, mock_ideas):
    assert get_idea(id, mock_ideas) == mock_ideas[index]


@pytest.mark.parametrize("id", [(""), ("-1"), ("7 7")])
def test_get_idea_not_found(id, mock_ideas):
    with pytest.raises(HTTPException, match=f"Project with id {id} not found."):
        get_idea(id, mock_ideas)
