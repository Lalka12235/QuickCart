from fastapi import APIRouter,Depends
from app.schemas.product_schema import ProductSchema,UpdateProductSchema
from app.services.product_service import ProductService
from app.config.session import get_db
from sqlalchemy.orm import Session
from typing import Annotated

product = APIRouter(
    tags=['Product']
)

db_dependency = Annotated[Session,Depends(get_db)]

@product.get('/products/{title}',summary='Get one product by title')
async def get_one_product_by_title(title: str, db: db_dependency):
    return ProductService.get_one_product_by_title(db,title)


#@product.get('/products',summary='Get all product')
#async def get_all_product():
#    return ProductService.get_all_product()


@product.post('/products',summary='Create product')
async def add_product(product: ProductSchema, db: db_dependency):
    return ProductService.add_product(db,product)


@product.put('/products/{title}',summary='Update field for product')
async def update_product(title: str, product: UpdateProductSchema, db: db_dependency):
    return ProductService.update_product(db,title,product)


@product.delete('/products/{title}',summary='Delete Product')
async def delete_product(title: str, db: db_dependency):
    return ProductService.delete_product(db,title)


@product.get('/products',summary='Get paginate product')
async def get_products_paginated(db: db_dependency,offset: int = 0,limit:int = 10, ):
    return ProductService.get_products_paginated(db,offset,limit)


@product.patch('/products/{title}',summary='Update quantity for product')
async def update_quantity(db: db_dependency,title: str, delta: int):
    return ProductService.update_quantity(db,title,delta)


@product.get('/products/count',summary='Count product')
async def get_total_products_count(db: db_dependency):
    return ProductService.get_total_products_count(db)