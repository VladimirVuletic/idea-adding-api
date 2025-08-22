from app.services.ideas_repository import IdeasFileRepository

def get_ideas_file_repo() -> IdeasFileRepository:
    return IdeasFileRepository()