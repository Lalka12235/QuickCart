from pydantic import BaseModel,Field


class ReviewsSchema(BaseModel):
    title: str = Field(..., description="Review title")
    rating: int = Field(...,description='Rating for product')
    description: str = Field(..., description="Review description")


class UpdateReviewSchema(BaseModel):
    title: str | None = Field(None, description="Review title")
    rating: int | None = Field(None,description='Rating for product')
    description: str | None = Field(None, description="Review description")