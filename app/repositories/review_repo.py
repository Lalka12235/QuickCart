from sqlalchemy import select,update,delete,func
from app.models.review_model import ReviewModel
from app.schemas.review_schema import ReviewsSchema, UpdateReviewSchema
import uuid
from sqlalchemy.orm import Session


class ReviewRepository:

    @staticmethod
    def get_review_about_product_by_user_id(db: Session,user_id: uuid.UUID,product_id: int) -> ReviewModel | None:
        stmt = select(ReviewModel).where(
            ReviewModel.user_id == user_id,ReviewModel.product_id == product_id
        )
        result = db.execute(stmt)
        return result.scalar_one_or_none()
        
    
    @staticmethod
    def get_all_review_by_user_id(db: Session,user_id: uuid.UUID) -> list:
        stmt = select(ReviewModel).where(ReviewModel.user_id == user_id)
        result = db.execute(stmt)
        return result.scalars().all()
        
    
    @staticmethod
    def add_review(db: Session,review: ReviewsSchema,user_id: uuid.UUID,product_id: int) -> ReviewModel:
        new_review = ReviewModel(
            title=review.title,
            rating=review.rating,
            description=review.description,
            user_id=user_id,
            product_id=product_id,
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
        

    @staticmethod
    def update_review(db: Session,review: UpdateReviewSchema,user_id: uuid.UUID,product_id: int) -> bool:
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
        result = db.execute(stmt)
        db.commit()
        return result.rowcount > 0
        

    @staticmethod
    def delete_review(db: Session,user_id: uuid.UUID,product_id: int) -> bool:
        stmt = delete(ReviewModel).where(
            ReviewModel.user_id == user_id,
            ReviewModel.product_id == product_id,
        )
        result = db.execute(stmt)
        db.commit()
        return result.rowcount > 0
        

    @staticmethod
    def get_all_review_product_by_product_id(db: Session,product_id: int) -> list:
        stmt = select(ReviewModel).where(
            ReviewModel.product_id == product_id
        )
        result = db.execute(stmt)
        return result.scalars().all()
        

    @staticmethod
    def count_total_review(db: Session,product_id: int) -> int:
        stmt = select(func.count(ReviewModel.id)).where(
            ReviewModel.product_id == product_id
        )
        result = db.execute(stmt)
        return result.scalar()
        
    @staticmethod
    def calculating_average_product_rating(db: Session,product_id: int) -> float | None:
        stmt = select(func.avg(ReviewModel.rating)).where(
            ReviewModel.product_id == product_id
        )
        result = db.execute(stmt).scalar_one_or_none()
        return float(result)
        
    @staticmethod
    def pagination_review(db: Session,product_id: int,offset: int = 0,limit: int = 10) -> list:
        stmt = select(ReviewModel).where(
            ReviewModel.product_id == product_id
        ).offset(offset).limit(limit)
        result = db.execute(stmt)
        return result.scalars().all()
        
    