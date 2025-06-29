from fastapi import APIRouter
from app.schemas.product_schema import ProductSchema,UpdateProductSchema
from app.services.product_service import ProductService

product = APIRouter(
    tags=['Product']
)

@product.get('/products/{title}',summary='Get one product by title')
async def get_one_product_by_title(title: str):
    return ProductService.get_one_product_by_title(title)


#@product.get('/products',summary='Get all product')
#async def get_all_product():
#    return ProductService.get_all_product()


@product.post('/products',summary='Create product')
async def add_product(product: ProductSchema):
    return ProductService.add_product(product)


@product.put('/products/{title}',summary='Update field for product')
async def update_product(title: str, product: UpdateProductSchema):
    return ProductService.update_product(title,product)


@product.delete('/products/{title}',summary='Delete Product')
async def delete_product(title: str):
    return ProductService.delete_product(title)


@product.get('/products',summary='Get paginate product')
async def get_products_paginated(offset: int = 0,limit:int = 10):
    return ProductService.get_products_paginated(offset,limit)


@product.patch('/products/{title}',summary='Update quantity for product')
async def update_quantity(title: str, delta: int):
    return ProductService.update_quantity(title,delta)


@product.get('/products/count',summary='Count product')
async def get_total_products_count():
    return ProductService.get_total_products_count()