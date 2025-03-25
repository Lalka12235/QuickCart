from fastapi import APIRouter, HTTPException, status
from app.db.postgres.orm_work import ManageProduct
from app.data.model_pydantic.models import Product

product = APIRouter(
    tags=['Product']
)

@product.get('/online-shop/product/get-all')
async def get_all_product():
    result = ManageProduct.get_all_products()

    return {'Product': result}

@product.get('/online-shop/product/get-one')
async def get_one_product(title: str):
    result = ManageProduct.get_one_product(title)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {'One product': result}

@product.post('/online-shop/product/create')
async def create_product(product: Product):
    exist_product = ManageProduct.get_one_product(product.title)

    if exist_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists"
        )
    
    result = ManageProduct.create_product(product)

    return {'Create': True, 'Desc': result}

@product.patch('/online-shop/product/update')
async def update_product(product: Product):
    exist_product = ManageProduct.get_one_product(product.title)

    if  not exist_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product dont exists"
        )
    

    result = ManageProduct.update_product(product.title,product)

    return {'Update': True, 'Desc': result}

@product.delete('/online-shop/product/delete')
async def delete_product(title: str):
    exist_product = ManageProduct.get_one_product(title)

    if  not exist_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product dont exists"
        )
    
    result = ManageProduct.delete_product(title)
    
    return {'Delete': True,'desc': result}