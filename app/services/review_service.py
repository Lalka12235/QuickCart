from fastapi import HTTPException,status
from app.repositories.review_repo import ReviewRepository
from app.schemas.review_schema import ReviewsSchema,UpdateReviewSchema
from app.services.user_service import UserService
from app.services.product_service import ProductService
import uuid
from typing import Any

class ReviewService:

    @staticmethod
    def get_review_about_by_user_id(email: str,title: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        product = ProductService.get_one_product_by_title(title)
        product_id = product.id

        review = ReviewRepository.get_review_about_product_by_user_id(user_id,product_id)

        if not review:
            raise HTTPException(
                status_code=404,
                detail='Review not found'
            )
        
        return {
            'status': 'found',
            'data':{
                'id': review.id,
                'title': review.title,
                'rating': review.rating,
                'description': review.description,
                'user_id': user_id,
                'product_id': product_id,
            }
        }
    

    @staticmethod
    def get_all_review_by_user_id(email: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        reviews = ReviewRepository.get_all_review_by_user_id(user_id)

        if not reviews:
            raise HTTPException(
                status_code=404,
                detail='Reviews not found'
            )
        
        return {
            'status': 'found',
            'data':[{
                'id': review.id,
                'title': review.title,
                'rating': review.rating,
                'description': review.description,
                'user_id': user_id,
                'product_id': review.product_id,
            } for review in reviews
            ]
        }
    

    @staticmethod
    def add_review(review: ReviewsSchema,email: str, title: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        product = ProductService.get_one_product_by_title(title)
        product_id = product.id

        reviews = ReviewRepository.get_review_about_product_by_user_id(user_id,product_id)
        if reviews:
            raise HTTPException(
                status_code=409,
                detail='Maybe should delete review or change'
            )
        
        add_review = ReviewRepository.add_review(review,user_id,product_id)

        return {
            'status': 'found',
            'data':{
                'id': add_review.id,
                'title': add_review.title,
                'rating': add_review.rating,
                'description': add_review.description,
                'user_id': add_review.user_id,
                'product_id': add_review.product_id,
            }
        }
    

    @staticmethod
    def update_review(review: UpdateReviewSchema,email: str, title: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        product = ProductService.get_one_product_by_title(title)
        product_id = product.id

        reviews = ReviewRepository.get_review_about_product_by_user_id(user_id,product_id)

        if not reviews:
            raise HTTPException(
                status_code=404,
                detail='Review not found'
            )
        
        update_review = ReviewRepository.update_review(review,user_id,product_id)

        return {
            'status': 'found',
            'detail': update_review
        }
    
    @staticmethod
    def delete_review(email: str, title: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        product = ProductService.get_one_product_by_title(title)
        product_id = product.id

        review = ReviewRepository.get_review_about_product_by_user_id(user_id,product_id)

        if not review:
            raise HTTPException(
                status_code=404,
                detail='Review not found'
            )
        
        delete_review = ReviewRepository.delete_review(user_id,product_id)

        return {
            'status': 'found',
            'detail': delete_review
        }
    

    @staticmethod
    def get_all_review_product_by_product_id(title: str) -> dict[str,Any]:
        product = ProductService.get_one_product_by_title(title)
        product_id = product.id

        reviews = ReviewRepository.get_all_review_product_by_product_id(product_id)

        return {
            'status': 'found',
            'data':[{
                'id': review.id,
                'title': review.title,
                'rating': review.rating,
                'description': review.description,
                'user_id': review.user_id,
                'product_id': review.product_id,
            } for review in reviews
            ]
        }
    
    @staticmethod
    def count_total_review(title: str) -> dict[str,Any]:
        product = ProductService.get_one_product_by_title(title)
        product_id = product.id

        total = ReviewRepository.count_total_review(product_id)

        return {
            'status': 'found',
            'total review': total
        }
    

    @staticmethod
    def calculating_average_product_rating(title: str) -> dict[str,Any]:
        product = ProductService.get_one_product_by_title(title)
        product_id = product.id

        avg_rating = ReviewRepository.calculating_average_product_rating(product_id)

        return {
            'status': 'found',
            'avg rating': avg_rating
        }
    

    @staticmethod
    def pagination_review(title: str, offset: int = 0, limit: int = 10) -> dict[str,Any]:
        product = ProductService.get_one_product_by_title(title)
        product_id = product.id

        total_review = ReviewRepository.count_total_review(product_id)

        # 2. Получаем список продуктов с применением offset и limit
        reviews = ReviewRepository.pagination_review(product_id,offset=offset, limit=limit)

        # 3. Вычисляем текущую страницу
        # Нумерация страниц обычно начинается с 1, поэтому добавляем 1
        current_page = (offset // limit) + 1 if limit else 1

        # 4. Вычисляем общее количество страниц
        # Используем формулу округления вверх для целого числа страниц
        total_pages = (total_review + limit - 1) // limit if limit else 1

        # 5. Формируем ответ с данными и метаинформацией
        return {
            "status": "success",
            "total": total_review,         # Общее число отзывов
            "page": current_page,           # Текущая страница
            "limit": limit,                 # Размер страницы (сколько элементов на странице)
            "total_pages": total_pages,     # Общее количество страниц
            "data": [                       # Список продуктов на текущей странице
                {
                    "id": review.id,
                    "title": review.title,
                    "rating": review.rating,
                    "description": review.description,
                }
                for review in reviews
            ],
        }