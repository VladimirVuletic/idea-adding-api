from fastapi import FastAPI
from bs4 import BeautifulSoup
from decouple import config

import subprocess

api = FastAPI()

REPO_PATH = config("REPO_PATH")
FILE_NAME = config("FILE_NAME")

def get_table():
    file_path = REPO_PATH + FILE_NAME

    with open(file_path, 'r', encoding='utf-8') as file:
        md_file = file.read()

    soup = BeautifulSoup(md_file, 'html.parser')
    table_body = soup.find('tbody')
    table_rows = table_body.find_all('tr')

    json_table = []
    for row in table_rows:
        json_row = {
            "ID": row.find_all('td')[0].decode_contents(),
            "Project name": row.find_all('td')[1].decode_contents(),
            "Short description": row.find_all('td')[2].decode_contents(),
            "Long description": row.find_all('td')[3].decode_contents()
        }
        json_table.append(json_row)

    return json_table

def change_file(json_table):
    file_path = REPO_PATH + FILE_NAME

    with open(file_path, 'r', encoding='utf-8') as file:
        md_file = file.read()
    soup = BeautifulSoup(md_file, 'html.parser')

    table_body = soup.find('tbody')

    new_tbody = soup.new_tag('tbody')

    id = 1
    for row in json_table:
        new_tr = soup.new_tag('tr')
        for field in ("ID", "Project name", "Short description", "Long description"):
            new_td = soup.new_tag('td')
            if field == "ID":
                new_td.append(str(id))
                id = id + 1
            else:
                new_td.append(row[field])
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

# GET, POST, PUT, DELETE
# SIMPLE GET
@api.get('/')
def index():
    return {"message": "Hello World!"}

@api.get('/ideas/{id}') # path parameter - i provide the parameter in the path
def get_idea(id):
    json_table = get_table()

    for idea in json_table:
        if idea['ID'] == id:
            return {'result': idea}
        
@api.get('/ideas') # query parameter - for example ideas/?first_n=3
def get_ideas(first_n: int = None): # default value of none
    json_table = get_table()

    if first_n:
        return json_table[:first_n]
    else:
        return json_table

# SIMPLE POST

@api.post('/ideas')
def create_idea(idea: dict):
    json_table = get_table()
    new_idea_id = max(int(idea['ID']) for idea in json_table) + 1

    new_idea = {
        'ID': str(new_idea_id),
        'Project name': idea['Project name'],
        'Short description': idea['Short description'],
        'Long description': idea['Long description']
    }

    json_table.append(new_idea)

    change_file(json_table)
    push_changes(f"add idea '{idea['Project name']}' | ID: {new_idea_id}")

    return new_idea

# SIMPLE PUT
@api.put('/ideas/{idea_id}')
def update_idea(idea_id: int, updated_idea: dict):
    json_table = get_table()
    for idea in json_table:
        if idea['ID'].strip() == str(idea_id):
            idea['Project name'] = updated_idea['Project name']
            idea['Short description'] = updated_idea['Short description']
            idea['Long description'] = updated_idea['Long description']

            change_file(json_table)
            push_changes(f"update idea '{idea['Project name']}' | ID: {idea['ID']}")

            return idea
    return "Error, not found"


# SIMPLE DELETE
@api.delete('/ideas/{idea_id}')
def delete_idea(idea_id: int):
    json_table = get_table()

    for index, idea in enumerate(json_table):
        if idea['ID'].strip() == str(idea_id):
            deleted_idea = json_table.pop(index)

            change_file(json_table)
            push_changes(f"delete idea '{deleted_idea['Project name']}' | ID: {deleted_idea['ID']}")

            return deleted_idea
    return "Error, not found"
