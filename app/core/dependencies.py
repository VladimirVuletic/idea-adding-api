from app.services.idea_service import IdeasRepository


def get_ideas_repo() -> IdeasRepository:
    return IdeasRepository()