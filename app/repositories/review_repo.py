from sqlalchemy import select,update,delete,func
from app.config.session import Session
from app.models.orm_model import ReviewModel
from app.schemas.review_schema import ReviewsSchema, UpdateReviewSchema
import uuid


class ReviewRepository:

    @staticmethod
    def get_review_about_product_by_user_id(user_id: uuid.UUID,product_id: int) -> ReviewModel | None:
        with Session() as session:
            stmt = select(ReviewModel).where(
                ReviewModel.user_id == user_id,ReviewModel.product_id == product_id
            )
            result = session.execute(stmt)
            return result.scalar_one_or_none()
        
    
    @staticmethod
    def get_all_review_by_user_id(user_id: uuid.UUID) -> list:
        with Session() as session:
            stmt = select(ReviewModel).where(ReviewModel.user_id == user_id)
            result = session.execute(stmt)
            return result.scalars().all()
        
    
    @staticmethod
    def add_review(review: ReviewsSchema,user_id: uuid.UUID,product_id: int) -> ReviewModel:
        with Session() as session:
            new_review = ReviewModel(
                title=review.title,
                rating=review.rating,
                description=review.description,
                user_id=user_id,
                product_id=product_id,
            )
            session.add(new_review)
            session.commit()
            session.refresh(new_review)
            return new_review
        

    @staticmethod
    def update_review(review: UpdateReviewSchema,user_id: uuid.UUID,product_id: int) -> bool:
        with Session() as session:
            stmt = update(ReviewModel).where(
                ReviewModel.user_id == user_id,
                ReviewModel.product_id == product_id,
            ).values(
                title=review.title,
                rating=review.rating,
                description=review.description,
                #user_id=user_id,
                #product_id=product_id
            )
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
        

    @staticmethod
    def delete_review(user_id: uuid.UUID,product_id: int) -> bool:
        with Session() as session:
            stmt = delete(ReviewModel).where(
                ReviewModel.user_id == user_id,
                ReviewModel.product_id == product_id,
            )
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
        

    @staticmethod
    def get_all_review_product_by_product_id(product_id: int) -> list:
        with Session() as session:
            stmt = select(ReviewModel).where(
                ReviewModel.product_id == product_id
            )
            result = session.execute(stmt)
            return result.scalars().all()
        

    @staticmethod
    def count_total_review(product_id: int) -> int:
        with Session() as session:
            stmt = select(func.count(ReviewModel.id)).where(
                ReviewModel.product_id == product_id
            )
            result = session.execute(stmt)
            return result.scalar()
        
    @staticmethod
    def calculating_average_product_rating(product_id: int) -> float | None:
        with Session() as session:
            stmt = select(func.avg(ReviewModel.rating)).where(
                ReviewModel.product_id == product_id
            )
            result = session.execute(stmt).scalar_one_or_none()
            return float(result)
        
    @staticmethod
    def pagination_review(product_id: int,offset: int = 0,limit: int = 10) -> list:
        with Session() as session:
            stmt = select(ReviewModel).where(
                ReviewModel.product_id == product_id
            ).offset(offset).limit(limit)
            result = session.execute(stmt)
            return result.scalars().all()
        
    