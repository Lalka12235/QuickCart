from fastapi import HTTPException,status
from app.repositories.order_repo import OrderRepository
from app.services.user_service import UserService
from app.schemas.order_schema import OrderSchema
from app.services.product_service import ProductService
from typing import Any
from sqlalchemy.orm import Session

class OrderService:

    @staticmethod
    def get_order_by_id(db: Session,email: str, order_id: int) -> dict[str, Any]:
        user = UserService.get_user_by_email(db,email)
        user_id = user.id

        order = OrderRepository.get_order_by_id(db,order_id, user_id)
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
    def get_all_order_by_user_id(db: Session,email: str) -> dict[str, Any]:
        user = UserService.get_user_by_email(db,email)
        user_id = user.id


        orders = OrderRepository.get_all_order_by_user_id(db,user_id)
        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or does not belong to user"
            )
        
        return {
            "status": "success",
            "data": {
                'orders': orders,
            }
        }
    

    @staticmethod
    def add_order(db: Session,email: str,order_data: OrderSchema) -> dict[str, Any]:
        user = UserService.get_user_by_email(db,email)
        user_id = user.id

        for data in order_data.products:
            product = ProductService.get_one_product_by_title(db,data.title_product)
            product_id = product.id
            product_quantity = product.quantity

        if data.quantity > product_quantity:
            raise HTTPException(
                status_code=409,
                detail=f'Product have{product_quantity}'
            )

        order = OrderRepository.add_order(db,order_data,user_id)

        product_to_order = OrderRepository.add_product_to_order(db,order.id,product_id,product_quantity)

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
    def add_order(db: Session,email: str, order_data: OrderSchema) -> dict:
        user = UserService.get_user_by_email(db,email)
        user_id = user.id

        if not order_data.products:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Products list cannot be empty")

        # Создаём заказ один раз
        new_order = OrderRepository.add_order(db,order_data, user_id)

        # Добавляем продукты в заказ
        for item in order_data.products:
            product = ProductService.get_one_product_by_title(db,item.title_product)

            if item.quantity > product.quantity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Not enough quantity for product '{item.title_product}'. Available: {product.quantity}"
                )

            OrderRepository.add_product_to_order(db,new_order.id, product.id, item.quantity)
            ProductService.update_quantity(item.title_product, -item.quantity)

        return {
            "status": "success",
            "data": {
                "id": new_order.id,
                "address": new_order.address,
                "delivered": new_order.delivered,
                "created_at": new_order.created_at.isoformat(),
            }
        }

    @staticmethod
    def update_order_delivery_status(db: Session,order_id: int, email: str, delivered: bool) -> dict[str,Any]:
        user = UserService.get_user_by_email(db,email)
        user_id = user.id

        order = OrderRepository.get_order_by_id(db,order_id,user_id)

        if not order:
            raise HTTPException(
                status_code=404,
                detail='Order not found'
            )
        
        update_order = OrderRepository.update_order_delivery_status(db,order_id,user_id,delivered)

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
    def cancel_order(db: Session,order_id: int, email: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(email)
        user_id = user.id

        order = OrderRepository.get_order_by_id(db,order_id,user_id)

        if not order:
            raise HTTPException(
                status_code=404,
                detail='Order not found'
            )
        
        delete_order = OrderRepository.cancel_order(db,order_id,user_id)

        return {
            "status": "success",
            'detail': f'Delete order with id: {order.id}'
        }
    

    @staticmethod
    def count_orders(db: Session,email: str) -> dict[str,Any]:
        user = UserService.get_user_by_email(db,email)
        user_id = user.id

        total = OrderRepository.count_orders(db,user_id)

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