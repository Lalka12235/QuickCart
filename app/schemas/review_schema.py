from pydantic import BaseModel


class ReviewsModel(BaseModel):
    username: str
    title: str
    description: str
