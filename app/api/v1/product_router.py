from fastapi import APIRouter, HTTPException, status,Depends
from app.orm_work import ManageProduct
from app.schemas.models import Product
from app.auth.auth import get_current_user

product = APIRouter(
    tags=['Product']
)

@product.get('/online-shop/product/get-all')
async def get_all_product():
    result = ManageProduct.get_all_products()


    return {'Product': result}

@product.get('/online-shop/product/get-one')
async def get_one_product(username: str,title: str):
    result = ManageProduct.get_one_product(title)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {'One product': result}

@product.post('/online-shop/product/create')
async def create_product(username: str,product: Product, current_user: str = Depends(get_current_user)):
    exist_product = ManageProduct.get_one_product(product.title)

    if username != current_user:
        raise HTTPException(status_code=403, detail="")

    if exist_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists"
        )
    
    result = ManageProduct.create_product(product)

    return {'Create': True, 'Desc': result}

@product.patch('/online-shop/product/update')
async def update_product(username: str,product: Product, current_user: str = Depends(get_current_user)):
    exist_product = ManageProduct.get_one_product(product.title)

    if username != current_user:
        raise HTTPException(status_code=403, detail="")

    if  not exist_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product dont exists"
        )
    

    result = ManageProduct.update_product(product.title,product)

    return {'Update': True, 'Desc': result}

@product.delete('/online-shop/product/delete')
async def delete_product(username: str,title: str, current_user: str = Depends(get_current_user)):
    exist_product = ManageProduct.get_one_product(title)

    if username != current_user:
        raise HTTPException(status_code=403, detail="")

    if  not exist_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product dont exists"
        )
    
    result = ManageProduct.delete_product(title)
    
    return {'Delete': True,'desc': result}