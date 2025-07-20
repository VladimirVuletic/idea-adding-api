from fastapi import FastAPI

api = FastAPI()

# GET, POST, PUT, DELETE

# SIMPLE GET
@api.get('/')
def index():
    return {"message": "Hello World!"}