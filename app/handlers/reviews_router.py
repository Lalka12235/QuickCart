from fastapi import APIRouter, HTTPException, status,Depends
from app.db.postgres.orm_work import ManageProduct
from app.db.mongoDB.mongo import ManageReview
from app.data.model_pydantic.models import ReviewsModel
from app.auth.auth import get_current_user


review = APIRouter(
    tags=['Review']
)

@review.get('/online-shop/review/get')
async def get_review(title: str,current_user: str = Depends(get_current_user)):
    result = ManageReview.get_review(title)

    return {'Get': True, 'desc': result}

@review.post('/online-shop/review/create')
async def create_review(title:str,review: ReviewsModel,current_user: str = Depends(get_current_user)):
    if review.username != current_user:
        raise HTTPException(status_code=403, detail="")
    try:
        # Получаем продукт по названию
        product = ManageProduct.get_one_product(title)
        
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        # Создаем отзыв
        result = ManageReview.create_review(product, review)

        # Возвращаем сериализованный результат
        return {'status': 'success', 'data': result}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@review.patch('/online-shop/review/update')
async def update_review(review: ReviewsModel, current_user: str = Depends(get_current_user)):
    result = ManageReview.update_review(review)
    if review.username != current_user:
        raise HTTPException(status_code=403, detail="")

    return {'Update': True,'desc': result}

@review.delete('/online-shop/review/delete')
async def delete_review(username: str,title: str, current_user: str = Depends(get_current_user)):
    result = ManageReview.delete_review(username,title)
    if username != current_user:
        raise HTTPException(status_code=403, detail="")

    return {'Delete': True, 'desc': result}