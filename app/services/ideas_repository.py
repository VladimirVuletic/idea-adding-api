from typing import Optional

from app.schemas.idea import Idea
from app.schemas.idea_create import IdeaCreate
from app.schemas.idea_update import IdeaUpdate

class IdeasRepository():
    def get_idea(self, id: str) -> Optional[Idea]:
        raise NotImplementedError
    
    def get_ideas(self) -> list[Idea]:
        raise NotImplementedError
    
    def add_idea(self, new_idea: IdeaCreate) -> Optional[Idea]:
        raise NotImplementedError
    
    def update_idea(self, id: str, updated_idea: IdeaUpdate) -> Optional[Idea]:
        raise NotImplementedError
    
    def delete_idea(self, id: str) -> Optional[Idea]:
        raise NotImplementedError