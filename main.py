from fastapi import FastAPI
from bs4 import BeautifulSoup

api = FastAPI()

def get_table():
    file_path = r"C:/Python projects/future-projects/README.md"

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
    file_path = r"C:/Python projects/future-projects/README.md"
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
        file.write(str(soup))

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

    return new_idea

"""
# SIMPLE PUT
@api.put('/ideas/{idea_id}')
def update_idea(idea_id: int, updated_idea: dict):
    for idea in json_table:
        if idea['idea_id'] == idea_id:
            idea['idea_name'] = updated_idea['idea_name']
            idea['idea_description'] = updated_idea['idea_description']
            return idea
    return "Error, not found"
"""

# SIMPLE DELETE
@api.delete('/ideas/{idea_id}')
def delete_idea(idea_id: int):
    json_table = get_table()

    for index, idea in enumerate(json_table):
        if idea['ID'] == str(idea_id):
            deleted_idea = json_table.pop(index)

            change_file(json_table)

            return deleted_idea
    return "Error, not found"
