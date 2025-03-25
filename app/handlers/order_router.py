from fastapi import APIRouter, HTTPException, status
from app.db.postgres.orm_work import ManageOrder

order = APIRouter(
    tags=['Order']
)


@order.get('/online-shop/order/get')
async def get_order(username: str):
    exist_order = ManageOrder.select_order(username)

    if  not exist_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order dont exists"
        )
    
    return {'Orders': exist_order}

@order.post('/online-shop/order/create')
async def create_order(username: str,title: str):
    exist_order = ManageOrder.select_order(username)

    if  exist_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order exists"
        )
    
    result = ManageOrder.create_order(username,title)

    return {'Create':  True,'Order': result}

@order.patch('/online-shop/order/update')
async def update_order(username: str, title: str):
    exist_order = ManageOrder.select_order(username)

    if  not exist_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product dont exists"
        )
    
    result = ManageOrder.update_order(username,title)

    return {'Update': True, 'Desc': result}

@order.delete('/online-shop/order/delete')
async def delete_order(username: str, title: str):
    exist_order = ManageOrder.select_order(username)

    if  not exist_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product dont exists"
        )
    
    result = ManageOrder.delete_order(username,title)

    return {'Delete': True, 'Desc': result}