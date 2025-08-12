from fastapi import FastAPI, HTTPException

from typing import List

from app.schemas.idea import Idea
from app.schemas.idea_create import IdeaCreate
from app.schemas.idea_update import IdeaUpdate
from app.services.idea_service import get_table, change_file, push_changes, find_idea_by_id

app = FastAPI()

@app.get('/')
def read_root():
    return "Server is running."

@app.get('/ideas/{id}', response_model=Idea)
def get_idea(id):
    ideas_table = get_table()               # This is not done
    idea = find_idea_by_id(ideas_table, id) # These two should be injected
    if idea:
        return idea
    raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")
        
@app.get('/ideas', response_model=List[Idea])
def get_ideas(first_n: int = None):
    ideas_table = get_table()

    if first_n:
        return ideas_table[:first_n]
    else:
        return ideas_table

@app.post('/ideas', response_model=Idea)
def create_idea(idea: IdeaCreate):
    ideas_table = get_table()
    new_idea_id = max(int(idea.id.strip()) for idea in ideas_table) + 1

    new_idea = Idea(id=str(new_idea_id),
                    name=idea.name,
                    short_description=idea.short_description,
                    long_description=idea.long_description)

    ideas_table.append(new_idea)

    change_file(ideas_table)
    push_changes(f"add idea '{idea.name}' | id: {new_idea_id}")

    return new_idea

@app.put('/ideas/{id}', response_model=Idea)
def update_idea(id: str, updated_idea: IdeaUpdate):
    ideas_table = get_table()
    for idea in ideas_table:
        if idea.id.strip() == id:
            if updated_idea.name is not None:
                idea.name = updated_idea.name
            if updated_idea.short_description is not None:
                idea.short_description = updated_idea.short_description
            if updated_idea.long_description is not None:
                idea.long_description = updated_idea.long_description

            change_file(ideas_table)
            push_changes(f"update idea '{idea.name}' | id: {idea.name}")

            return idea
        
    raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")


@app.delete('/ideas/{id}', response_model=Idea)
def delete_idea(id: str):
    ideas_table = get_table()

    for index, idea in enumerate(ideas_table):
        if idea.id.strip() == id:
            deleted_idea = ideas_table.pop(index)

            change_file(ideas_table)
            push_changes(f"delete idea '{deleted_idea.name}' | id: {deleted_idea.id}")

            return deleted_idea
    
    raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")