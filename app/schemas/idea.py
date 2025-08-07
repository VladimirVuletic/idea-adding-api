from pydantic import Field

from schemas.idea_base import IdeaBase

class Idea(IdeaBase):
    id: str = Field(..., description="Unique identifier of the project.")
