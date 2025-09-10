from typing import Optional

from pydantic import BaseModel, Field


class IdeaUpdate(BaseModel):
    name: Optional[str] = Field(None, description="(Optional) Name of the project.")
    short_description: Optional[str] = Field(
        None, description="(Optional) Short description."
    )
    long_description: Optional[str] = Field(
        None, description="(Optional) Long description or link."
    )
