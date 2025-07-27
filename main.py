from fastapi import FastAPI

api = FastAPI()



# Pseudo-DB - list of dicts # From a README.md FILE 
# This is just a test, we shouldn't duplicate logic from another script
from bs4 import BeautifulSoup

file_path = r"C:/Python projects/future-projects/README.md"

with open(file_path, 'r', encoding='utf-8') as file:
    md_file = file.read()

soup = BeautifulSoup(md_file, 'html.parser')
table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

json_table = []
for row in table_rows:
    json_row = {
        "ID": row.find_all('td')[0].text,
        "Project name": row.find_all('td')[1].text,
        "Short description": row.find_all('td')[2].text,
        "Long description": row.find_all('td')[3].text
    }
    json_table.append(json_row)



# GET, POST, PUT, DELETE
# SIMPLE GET
@api.get('/')
def index():
    return {"message": "Hello World!"}

@api.get('/ideas/{id}') # path parameter - i provide the parameter in the path
def get_idea(id):
    for idea in json_table:
        if idea['ID'] == id:
            return {'result': idea}
        
@api.get('/ideas') # query parameter - for example ideas/?first_n=3
def get_ideas(first_n: int = None): # default value of none
    if first_n:
        return json_table[:first_n]
    else:
        return json_table

# SIMPLE POST
"""
@api.post('/ideas')
def create_idea(idea: dict):
    new_idea_id = max(idea['idea_id'] for idea in json_table) + 1

    new_idea = {
        'idea_id': new_idea_id,
        'idea_name': idea['idea_name'],
        'idea_description': idea['idea_description']
    }

    json_table.append(new_idea)

    return new_idea

# SIMPLE PUT
@api.put('/ideas/{idea_id}')
def update_idea(idea_id: int, updated_idea: dict):
    for idea in json_table:
        if idea['idea_id'] == idea_id:
            idea['idea_name'] = updated_idea['idea_name']
            idea['idea_description'] = updated_idea['idea_description']
            return idea
    return "Error, not found"


# SIMPLE DELETE
@api.delete('/ideas/{idea_id}')
def delete_idea(idea_id: int):
    for index, idea in enumerate(json_table):
        if idea['idea_id'] == idea_id:
            deleted_idea = json_table.pop(index)
            return deleted_idea
    return "Error, not found"
"""