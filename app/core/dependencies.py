from app.services.ideas_file_repository import IdeasFileRepository
from app.utils.git_client import GitClient


def get_ideas_file_repo() -> IdeasFileRepository:
    return IdeasFileRepository()


def get_git_client() -> GitClient:
    return GitClient()
