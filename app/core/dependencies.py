from app.services.ideas_repository import IdeasRepository

def get_ideas_repo() -> IdeasRepository:
    return IdeasRepository()