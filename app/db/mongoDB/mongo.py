from pymongo import MongoClient
from app.db.postgres.orm_work import ManageProduct, Profile
from app.data.model_pydantic.models import ReviewsModel, Product

client = MongoClient('localhost',27017)


db_shop = client['shop-reviews']

db_col = db_shop['reviews-col']


class ManageReview:

    @staticmethod
    def get_review(product: str):
        exist_product = ManageProduct.get_one_product(product)

        if not exist_product:
            return {'Product': 'Not find'}
        
        result = list(db_col.find({'title': product}))

        return {'Find': True,'Product': result}


    @staticmethod
    def create_review(product: Product,review: ReviewsModel):
        exist_product = ManageProduct.get_one_product(product)
        user_review = ManageReview.get_review(product.title)
        exist_user = Profile.select_user(review.username)

        if not exist_user:
            return {'User': 'Not exist'}

        if not exist_product:
            return {'Product': 'Not find'}
        
        for r in user_review.get('Product', []):
            if review.username in r['reviews']:
                return {'Review for user': 'Юзер с таким отзывом уже есть'}

        stmt = db_col.insert_one({
            product.title:{
                'title': product.title,
                'description': product.description,
                'reviews':{
                    review.username:{
                        'username': review.username,
                        'title': review.title,
                        'description': review.description
                    }
                } 
            } 
        })

        return {'Review': True,'Review': stmt}    

        

    @staticmethod
    def delete_review(username: str, product: str):
        exist_product = ManageProduct.get_one_product(product)
        user_review = ManageReview.get_review(username)

        if not exist_product:
            return {'Product': 'Not find'}
        
        if not user_review:
            return {'Review for user': 'Юзера с таким отзывом нету'}
        
        result = db_col.update_one(
            {'title': product},  
            {'$unset': {f'reviews.{username}': ""}}  
        )

        if result.modified_count > 0:
            return {'Delete': True}

        return {'Delete': 'Not found'}


    @staticmethod
    def update_review(review: ReviewsModel):
        exist_product = ManageProduct.get_one_product(review.title)
        user_review = ManageReview.get_review(review.username)
        exist_user = Profile.select_user(review.username)

        if not exist_user:
            return {'User': 'Not exist'}

        if not exist_product:
            return {'Product': 'Not find'}
        
        if user_review:
            result = db_col.update_one(
                {'title': review.title, f'reviews.{review.username}.username': review.username},
                {'$set': {
                    f'reviews.{review.username}.title': review.title,
                    f'reviews.{review.username}.description': review.description
                }}
            )

            return {'Update': True, 'Review': result}

        return {'Review': 'Not found'}