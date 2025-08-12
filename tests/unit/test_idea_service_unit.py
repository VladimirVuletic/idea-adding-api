from app.services.idea_service import run_cmd, find_idea_by_id
from app.schemas.idea import Idea


def test_run_cmd():
    cmd = ["cmd", "/c", "echo", "Something"]
    cwd = f"C:\\Python projects\\idea-adding-api"

    assert run_cmd(cmd, cwd) == "Something\n"


def test_find_idea_by_id_found():
    # TODO: We should use parametrization here though
    mock_ideas = [
        Idea(id='7', name='Name of idea 7', short_description='short desc for idea 7', long_description='long desc for idea 7'),
        Idea(id='X', name='Name of idea X', short_description='short desc for idea X', long_description='long desc for idea X'),
        Idea(id='   9\n', name='Name of idea 9\n', short_description='short desc for idea 9\n', long_description='long desc for idea 9\n'),
    ]
    result = find_idea_by_id("7", mock_ideas)

    # TODO: I should probably assert an Idea object, not its fields
    assert result.id == "7"
    assert result.name == "Name of idea 7"
    assert result.short_description == "short desc for idea 7"
    assert result.long_description == "long desc for idea 7"


def test_find_idea_by_id_not_found():
    result = find_idea_by_id("7", ideas=[])

    assert result == None
