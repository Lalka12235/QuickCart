from fastapi import APIRouter, Depends
from app.services.review_service import ReviewService
from app.schemas.review_schema import ReviewsSchema,UpdateReviewSchema
from app.config.session import get_db
from sqlalchemy.orm import Session
from typing import Annotated


review = APIRouter(
    tags=['Review']
)

db_dependency = Annotated[Session,Depends(get_db)]

@review.get('/reviews/{user_id}/{title}',summary='Get review about product by user_id')
async def get_review_about_by_user_id(email: str, title_product: str, db: db_dependency):
    return ReviewService.get_review_about_by_user_id(db,email,title_product)


@review.get('/reviews',summary='Get all review by user_id')
async def get_all_review_by_user_id(email: str, db: db_dependency):
    return ReviewService.get_all_review_by_user_id(db,email)


@review.post('/reviews',summary='Create review for product')
async def add_review(review: ReviewsSchema,email: str, title_product: str, db: db_dependency):
    return ReviewService.add_review(db,review,email,title_product)


@review.put('/reviews/{user_id}/{title}',summary='Update review')
async def update_review(review: UpdateReviewSchema,email: str, title_product: str, db: db_dependency):
    return ReviewService.update_review(db,review,email,title_product)


@review.delete('/reviews/{user_id}/{title}',summary='Delete Review')
async def delete_review(email: str, title_product: str, db: db_dependency):
    return ReviewService.delete_review(db,email,title_product)


@review.get('/reviews/{title_product}',summary='Get all review product by product_id')
async def get_all_review_product_by_product_id(title_product: str, db: db_dependency):
    return ReviewService.get_all_review_product_by_product_id(db,title_product)


@review.get('/reviews/count',summary='Total review product')
async def count_total_review(title_product: str, db: db_dependency):
    return ReviewService.count_total_review(db,title_product)

@review.get('/reviews/avg/{title_product}',summary='Calculating avg product rating')
async def calculating_average_product_rating(title_product: str, db: db_dependency):
    return ReviewService.calculating_average_product_rating(db,title_product)


@review.get('/reviews/pagination{title_product}',summary='Get pagination review')
async def pagination_review(db: db_dependency,title_product: str, offset: int = 0, limit: int = 10, ):
    return ReviewService.pagination_review(db,title_product,offset,limit)
