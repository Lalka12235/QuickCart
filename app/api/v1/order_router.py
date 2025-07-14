from fastapi import APIRouter,Depends
from app.schemas.order_schema import OrderSchema
from app.services.order_service import OrderService
from app.config.session import get_db
from sqlalchemy.orm import Session
from typing import Annotated

order = APIRouter(
    tags=['Order']
)

db_dependency = Annotated[Session,Depends(get_db)]


@order.get('/orders{order_id}', summary='Get order by order_id')
async def get_order_by_id(email: str, order_id: int, db: db_dependency):
    return OrderService.get_order_by_id(db,email,order_id)


@order.get('/orders/{user_id}',summary='Get all order by user id')
async def get_all_order_by_user_id(email: str, db: db_dependency):
    return OrderService.get_all_order_by_user_id(db,email)


@order.post('/orders',summary='Create order')
async def add_order(email: str, order: OrderSchema, db: db_dependency):
    return OrderService.add_order(db,email, order)


@order.patch('/orders/{order_id}',summary='Update delivery status')
async def update_order_delivery_status(order_id: int, email: str, delivered: bool, db: db_dependency):
    return OrderService.update_order_delivery_status(db,order_id,email,delivered)


@order.delete('/orders',summary='Cancel order')
async def cancel_order(order_id: int, email: str, db: db_dependency):
    return OrderService.cancel_order(db,order_id,email)


@order.get('/orders/count',summary='Count Orders')
async def count_orders(email: str, db: db_dependency):
    return OrderService.count_orders(db,email)