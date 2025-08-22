from fastapi import Depends, FastAPI, HTTPException

from typing import Optional

from app.core.dependencies import get_ideas_repo
from app.schemas.idea import Idea
from app.schemas.idea_create import IdeaCreate
from app.schemas.idea_update import IdeaUpdate
from app.services.ideas_repository import IdeasRepository
from app.services.idea_service import get_table, change_file, push_changes, find_idea_by_id

app = FastAPI()

@app.get('/')
def read_root():
    return "Server is running."

@app.get('/ideas/{id}', response_model=Idea)
def get_idea(id: str, ideas_repo: IdeasRepository = Depends(get_ideas_repo)) -> Idea:
    idea = ideas_repo.get_idea(id)

    if idea is None:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")
 
    return idea
        
@app.get('/ideas', response_model=list[Idea])
def get_ideas(first_n: Optional[int] = None, ideas_repo: IdeasRepository = Depends(get_ideas_repo)) -> list[Idea]:
    ideas = ideas_repo.get_ideas()

    if first_n is None:
        first_n = len(ideas)
    
    if first_n < 0:
        raise HTTPException(status_code=400, detail=f"Invalid query parameter: {first_n}.")

    return ideas[:first_n]

@app.post('/ideas', response_model=Idea)
def create_idea(new_idea: IdeaCreate, ideas_repo: IdeasRepository = Depends(get_ideas_repo)) -> Idea:
    idea = ideas_repo.add_idea(new_idea)
    
    # We'll see how we'll inject this
    push_changes(f"add idea '{idea.name}' | id: {idea.id}")

    return idea

@app.put('/ideas/{id}', response_model=Idea)
def update_idea(id: str, updated_idea: IdeaUpdate, ideas_repo: IdeasRepository = Depends(get_ideas_repo)) -> Idea:
    idea = ideas_repo.update_idea(id, updated_idea)

    if idea is None:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")

    # We'll see how we'll inject this
    push_changes(f"update idea '{idea.name}' | id: {idea.name}")

    return idea


@app.delete('/ideas/{id}', response_model=Idea)
def delete_idea(id: str, ideas_repo: IdeasRepository = Depends(get_ideas_repo)) -> Idea:
    deleted_idea = ideas_repo.delete_idea(id)

    if deleted_idea is None:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")

    push_changes(f"delete idea '{deleted_idea.name}' | id: {deleted_idea.id}")

    return deleted_idea