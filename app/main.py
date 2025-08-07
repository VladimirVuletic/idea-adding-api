import subprocess
from typing import List, Optional

from bs4 import BeautifulSoup
from decouple import config
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from schemas.idea import Idea
from schemas.idea_create import IdeaCreate

api = FastAPI()

REPO_PATH = config("REPO_PATH")
FILE_NAME = config("FILE_NAME")


class IdeaUpdate(BaseModel):
    name: Optional[str] = Field(None, description="(Optional) Name of the project.")
    short_description: Optional[str] = Field(None, description="(Optional) Short description.")
    long_description: Optional[str] = Field(None, description="(Optional) Long description or link.")


def get_table():
    file_path = REPO_PATH + FILE_NAME

    with open(file_path, 'r', encoding='utf-8') as file:
        md_file = file.read()

    soup = BeautifulSoup(md_file, 'html.parser')
    table_body = soup.find('tbody')
    table_rows = table_body.find_all('tr')

    ideas_table = []
    for row in table_rows:
        idea = Idea(id=row.find_all('td')[0].decode_contents(),
                        name=row.find_all('td')[1].decode_contents(),
                        short_description=row.find_all('td')[2].decode_contents(),
                        long_description=row.find_all('td')[3].decode_contents())
        ideas_table.append(idea)
    return ideas_table

def change_file(ideas_table):
    file_path = REPO_PATH + FILE_NAME

    with open(file_path, 'r', encoding='utf-8') as file:
        md_file = file.read()
    soup = BeautifulSoup(md_file, 'html.parser')

    table_body = soup.find('tbody')

    new_tbody = soup.new_tag('tbody')

    id = 1
    for row in ideas_table:
        new_tr = soup.new_tag('tr')
        for field in ("id", "name", "short_description", "long_description"):
            new_td = soup.new_tag('td')
            if field == "id":
                new_td.append(str(id))
                id = id + 1
            else:
                new_td.append(getattr(row, field))
            new_tr.append(new_td)
        new_tbody.append(new_tr)
    table_body.replace_with(new_tbody)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify(formatter=None))

def run_cmd(cmd, cwd):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)

def push_changes(commit_message):
    repo_path = REPO_PATH

    run_cmd(['git', 'add', '.'], repo_path)
    run_cmd(['git', 'commit', '-m', commit_message], repo_path)
    run_cmd(['git', 'push'], repo_path)


@api.get('/ideas/{id}', response_model=Idea)
def get_idea(id):
    ideas_table = get_table()
    for idea in ideas_table:
        if idea.id.strip() == id:
            return idea
    
    raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")
        
@api.get('/ideas', response_model=List[Idea])
def get_ideas(first_n: int = None):
    ideas_table = get_table()

    if first_n:
        return ideas_table[:first_n]
    else:
        return ideas_table

@api.post('/ideas', response_model=Idea)
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

@api.put('/ideas/{id}', response_model=Idea)
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


@api.delete('/ideas/{id}', response_model=Idea)
def delete_idea(id: str):
    ideas_table = get_table()

    for index, idea in enumerate(ideas_table):
        if idea.id.strip() == id:
            deleted_idea = ideas_table.pop(index)

            change_file(ideas_table)
            push_changes(f"delete idea '{deleted_idea.name}' | id: {deleted_idea.id}")

            return deleted_idea
    
    raise HTTPException(status_code=404, detail=f"Project with id {id} not found.")