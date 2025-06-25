from pydantic import BaseModel,Field


class ReviewsModel(BaseModel):
    username: str = Field(..., description="Username of the reviewer")
    title: str = Field(..., description="Review title")
    description: str = Field(..., description="Review description")
