from fastapi import FastAPI

api = FastAPI()

# Pseudo-DB - list of dicts
all_todos = [
    {"todo_id": 1, "todo_name": "Sports", "todo_description": "Go to the gym"},
    {"todo_id": 2, "todo_name": "Read", "todo_description": "Read ten pages"},
    {"todo_id": 3, "todo_name": "Shop", "todo_description": "Go shopping"},
    {"todo_id": 4, "todo_name": "Study", "todo_description": "Study for exam"},
    {"todo_id": 5, "todo_name": "Meditate", "todo_description": "Meditate 20 minutes"},
]

# GET, POST, PUT, DELETE
# SIMPLE GET
@api.get('/')
def index():
    return {"message": "Hello World!"}

@api.get('/todos/{todo_id}') # path parameter - i provide the parameter in the path
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return {'result': todo}
        
@api.get('/todos') # query parameter - for example todos/?first_n=3
def get_todos(first_n: int = None): # default value of none
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos

# SIMPLE POST
@api.post('/todos')
def create_todo(todo: dict):
    new_todo_id = max(todo['todo_id'] for todo in all_todos) + 1

    new_todo = {
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }

    all_todos.append(new_todo)

    return new_todo

# SIMPLE PUT
@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            todo['todo_name'] = update_todo['todo_name']
            todo['todo_description'] = update_todo['todo_description']
            return todo
    return "Error, not found"