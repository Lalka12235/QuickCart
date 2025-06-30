from fastapi import APIRouter
from app.schemas.order_schema import OrderProductItem, OrderSchema
from app.services.order_service import OrderService

order = APIRouter(
    tags=['Order']
)


@order.get('/orders{order_id}', summary='Get order by order_id')
async def get_order_by_id(email: str, order_id: int):
    return OrderService.get_order_by_id(email,order_id)


@order.get('/orders/{user_id}',summary='Get all order by user id')
async def get_all_order_by_user_id(email: str):
    return OrderService.get_all_order_by_user_id(email)


@order.post('/orders',summary='Create order')
async def add_order(email: str, order: OrderSchema):
    return OrderService.add_order(email, order)


@order.patch('/orders/{order_id}',summary='Update delivery status')
async def update_order_delivery_status(order_id: int, email: str, delivered: bool):
    return OrderService.update_order_delivery_status(order_id,email,delivered)


@order.delete('/orders',summary='Cancel order')
async def cancel_order(order_id: int, email: str):
    return OrderService.cancel_order(order_id,email)


@order.get('/orders/count',summary='Count Orders')
async def count_orders(email: str):
    return OrderService.count_orders(email)