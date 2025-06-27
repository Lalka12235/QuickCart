from fastapi import HTTPException,status
from app.repositories.product_repo import ProductRepository
from app.schemas.product_schema import ProductSchema,UpdateProductSchema
from typing import Any

class ProductService:

    @staticmethod
    def get_one_product_by_title(title: str) -> dict[str, Any]:
        product = ProductRepository.get_one_product_by_title(title)

        if not product:
            raise HTTPException(
                status_code=404,
                detail='Product dont found'
            )
        
        return {'status': 'found','detail':{
            'id':product.id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'quantiy': product.quantity
        }}
    

    @staticmethod
    def get_all_product() -> dict[str, Any]:
        products  = ProductRepository.get_all_product()

        if not products :
            raise HTTPException(
                status_code=404,
                detail='No products available'
            )
        
        return {
            'status': 'success',
            'count': len(products),
            'data': [
                {
                    'id': product.id,
                    'title': product.title,
                    'description': product.description,
                    'price': product.price,
                    'quantity': product.quantity
                } 
                for product in products
            ]
        }
    

    @staticmethod
    def add_product(product: ProductSchema) -> dict[str, Any]:
        product_exist = ProductRepository.get_one_product_by_title(product.title)

        if product_exist:
            raise HTTPException(
                status_code=409,
                detail='Product with this title already exists'
            )
        
        new_product = ProductRepository.add_product(product)

        return {
            'status': 'success',
            'data': {
                'id': new_product.id,
                'title': new_product.title,
                'description': new_product.description,
                'price': new_product.price,
                'quantity': new_product.quantity
            }
        }
    

    @staticmethod
    def update_product(title: str, product_update: UpdateProductSchema) -> dict[str, Any]:
        product_exist = ProductRepository.get_one_product_by_title(title)

        if not product_exist:
            raise HTTPException(
                status_code=404,
                detail='Product with this title does not exist'
            )
        
        update_data = product_update.dict(exclude_unset=True)

        new_title = update_data.get('title')
        if new_title and new_title != title:
            conflict_product = ProductRepository.get_one_product_by_title(new_title)
            if conflict_product:
                raise HTTPException(
                    status_code=409,
                    detail='Another product with the new title already exists'
                )
        
        updated_product = ProductRepository.update_product(title, update_data)

        if not updated_product:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to update product'
            )

        return {
            'status': 'success',
            'data': {
                'id': updated_product.id,
                'title': updated_product.title,
                'description': updated_product.description,
                'price': updated_product.price,
                'quantity': updated_product.quantity
            }
        }
    

    @staticmethod
    def delete_product(title: str) -> dict[str, Any]:
        exist_product = ProductRepository.get_one_product_by_title(title)

        if not exist_product:
            raise HTTPException(
                status_code=404,
                detail='Not found product'
            )
        
        delete_product = ProductRepository.delete_product(title)

        return {
            'status': 'success',
            'detail': delete_product
        }
    

    @staticmethod
    def get_products_paginated(offset: int = 0, limit: int = 10) -> dict[str, Any]:
        # 1. Получаем общее количество продуктов в базе
        total_product = ProductRepository.get_total_products_count()

        # 2. Получаем список продуктов с применением offset и limit
        products = ProductRepository.get_products_paginated(offset=offset, limit=limit)

        # 3. Вычисляем текущую страницу
        # Нумерация страниц обычно начинается с 1, поэтому добавляем 1
        current_page = (offset // limit) + 1 if limit else 1

        # 4. Вычисляем общее количество страниц
        # Используем формулу округления вверх для целого числа страниц
        total_pages = (total_product + limit - 1) // limit if limit else 1

        # 5. Формируем ответ с данными и метаинформацией
        return {
            "status": "success",
            "total": total_product,         # Общее число продуктов
            "page": current_page,           # Текущая страница
            "limit": limit,                 # Размер страницы (сколько элементов на странице)
            "total_pages": total_pages,     # Общее количество страниц
            "data": [                       # Список продуктов на текущей странице
                {
                    "id": product.id,
                    "title": product.title,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity,
                }
                for product in products
            ],
        }


    @staticmethod
    def update_quantity(title: str, delta: int) -> dict[str,Any]:
        product = ProductRepository.get_one_product_by_title(title)

        if not product:
            raise HTTPException(
                status_code=404,
                detail='Not found product'
            )
        
        result = ProductRepository.update_quantity(product.id,delta)

        return {
            'status': 'success',
            'detail':{
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'quantity': product.quantity + delta
            }
        }


    @staticmethod
    def get_total_products_count() -> dict[str, Any]:
        total = ProductRepository.get_total_products_count()
        return {
            "status": "success",
            "total_products": total
        }