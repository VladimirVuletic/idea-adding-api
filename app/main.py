from fastapi import Depends, FastAPI, HTTPException

from app.schemas.idea import Idea
from app.schemas.idea_create import IdeaCreate
from app.schemas.idea_update import IdeaUpdate
from app.services.idea_service import get_table, change_file, push_changes, find_idea_by_id

app = FastAPI()

@app.get('/')
def read_root():
    return "Server is running."

@app.get('/ideas/{id}', response_model=Idea)
def get_idea(id: str, ideas: list[Idea] = Depends(get_table)) -> Idea:
    idea = find_idea_by_id(id, ideas)

    if idea is None:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")
 
    return idea
        
@app.get('/ideas', response_model=list[Idea])
def get_ideas(first_n: int = None, ideas: list[Idea] = Depends(get_table)) -> list[Idea]:
    if first_n:
        return ideas[:first_n]
    else:
        return ideas

@app.post('/ideas', response_model=Idea)
def create_idea(idea: IdeaCreate):
    ideas = get_table()
    new_idea_id = max(int(idea.id.strip()) for idea in ideas) + 1

    new_idea = Idea(id=str(new_idea_id),
                    name=idea.name,
                    short_description=idea.short_description,
                    long_description=idea.long_description)

    ideas.append(new_idea)

    change_file(ideas)
    push_changes(f"add idea '{idea.name}' | id: {new_idea_id}")

    return new_idea

@app.put('/ideas/{id}', response_model=Idea)
def update_idea(id: str, updated_idea: IdeaUpdate, ideas: list[Idea] = Depends(get_table)) -> Idea:
    idea = find_idea_by_id(id, ideas)

    if idea is None:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")

    if updated_idea.name is not None:
        idea.name = updated_idea.name
    if updated_idea.short_description is not None:
        idea.short_description = updated_idea.short_description
    if updated_idea.long_description is not None:
        idea.long_description = updated_idea.long_description

    change_file(ideas)
    push_changes(f"update idea '{idea.name}' | id: {idea.name}")

    return idea


@app.delete('/ideas/{id}', response_model=Idea)
def delete_idea(id: str, ideas: list[Idea] = Depends(get_table)) -> Idea:
    idea = find_idea_by_id(id, ideas)

    if idea is None:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")

    deleted_idea = idea
    ideas.remove(idea)

    change_file(ideas)
    push_changes(f"delete idea '{deleted_idea.name}' | id: {deleted_idea.id}")

    return deleted_idea
