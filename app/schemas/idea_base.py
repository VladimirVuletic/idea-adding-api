from pydantic import BaseModel, Field

from typing import Optional


class IdeaBase(BaseModel):
    name: str = Field(description="Name of the project.")
    short_description: Optional[str] = Field(
        default="", description="Short description of the project."
    )
    long_description: Optional[str] = Field(
        default="",
        description="Long description of the project or the link to the project's README.MD",
    )
