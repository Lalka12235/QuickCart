from fastapi import HTTPException,status
from app.repositories.order_repo import OrderRepostiroy
from app.services.user_service import UserService
from app.schemas.order_schema import OrderSchema
from typing import Any


class OrderService:

    @staticmethod
    def get_order_by_id(email: str, order_id: int) -> dict[str, Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        order = OrderRepostiroy.get_order_by_id(order_id, user_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or does not belong to user"
            )

        return {
            "status": "success",
            "data": {
                "id": order.id,
                "address": order.address,
                "delivered": order.delivered,
                "created_at": order.created_at.isoformat(),
                "products": [
                    {
                        "id": product.id,
                        "title": product.title,
                        "price": product.price,
                        "quantity": product.quantity,
                    }
                    for product in order.products
                ]
            }
        }
    

    @staticmethod
    def get_all_order_by_user_id(email: str) -> dict[str, Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id


        order = OrderRepostiroy.get_all_order_by_user_id(user_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or does not belong to user"
            )

        return {
            "status": "success",
            "data": {
                "id": order.id,
                "address": order.address,
                "delivered": order.delivered,
                "created_at": order.created_at.isoformat(),
                "products": [
                    {
                        "id": product.id,
                        "title": product.title,
                        "price": product.price,
                        "quantity": product.quantity,
                    }
                    for product in order.products
                ]
            }
        }
    

    @staticmethod
    def add_order(email: str,order_data: OrderSchema) -> dict[str, Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        order = OrderRepostiroy.add_order(order_data,user_id)

        return {
            "status": "success",
            "data": {
                "id": order.id,
                "address": order.address,
                "delivered": order.delivered,
                "created_at": order.created_at.isoformat(),
            }
        }
    

    @staticmethod
    def update_order_delivery_status(order_id: int, email: str, delivered: bool) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        order = OrderRepostiroy.get_order_by_id(order_id,user_id)

        if not order:
            raise HTTPException(
                status_code=404,
                detail='Order not found'
            )
        
        update_order = OrderRepostiroy.update_order_delivery_status(order_id,user_id,delivered)

        return {
            "status": "success",
            "data": {
                "id": order.id,
                "address": order.address,
                "delivered": update_order,
                "created_at": order.created_at.isoformat(),
            }
        }
    

    @staticmethod
    def delete_order(order_id: int, email: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        order = OrderRepostiroy.get_order_by_id(order_id,user_id)

        if not order:
            raise HTTPException(
                status_code=404,
                detail='Order not found'
            )
        
        delete_order = OrderRepostiroy.delete_order(order_id,user_id)

        return {
            "status": "success",
            'detail': f'Delete order with id: {order.id}'
        }
    

    @staticmethod
    def count_orders(email: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        total = OrderRepostiroy.count_orders(user_id)

        if total > 0:
            return {
            "status": "success",
            'data':{
                'user_id': user_id,
                'count order': total
            }
        }
        else:
            return {
            "status": "success",
            'data':{
                'user_id': user_id,
                'count order': 'You have 0 order. place your order soon'
            }
        }