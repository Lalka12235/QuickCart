from sqlalchemy import select,insert,update,delete,and_,func
from app.schemas.order_schema import OrderSchema
from app.models.order_model import OrderModel, order_product_association
import uuid
from sqlalchemy.orm import Sessio


class OrderRepository:

    @staticmethod
    def get_order_by_id(db: Session,order_id: int, user_id: uuid.UUID) -> OrderModel | None:
        stmt = select(OrderModel).where(
            OrderModel.id == order_id,
            OrderModel.user_id == user_id
        )
        result = db.execute(stmt)
        return result.scalar_one_or_none()


    @staticmethod
    def get_all_order_by_user_id(db: Session,user_id: int) -> OrderModel:
            stmt = select(OrderModel).where(OrderModel.user_id == user_id)
            result = db.execute(stmt)
            return result.scalars().all()
        
    
    @staticmethod
    def add_order(db: Session,order_data: OrderSchema, 
                  user_id: uuid.UUID,
    ) -> OrderModel:
            # 1. Создаём заказ
            new_order = OrderModel(
                address=order_data.address,
                user_id=user_id,
            )
            db.add(new_order)
            db.flush()  # чтобы получить new_order.id до коммита

            #2. Добавляем записи в ассоциативную таблицу order_products
            #stmt = insert(order_product_association).values(
            #    order_id=new_order.id,
            #    product_id=product_id,
            #    quantity=quantity
            #)
            #db.execute(stmt)
            #3. Фиксируем транзакцию
            db.commit()
            # 4. Обновляем объект заказа
            db.refresh(new_order)
            return new_order
        
    @staticmethod
    def add_product_to_order(db: Session,order_id: int, product_id: int, quantity: int):
         stmt = insert(order_product_association).values(
             order_id=order_id,
             product_id=product_id,
             quantity=quantity
         )
         db.execute(stmt)
         db.commit()


    @staticmethod
    def update_order_delivery_status(db: Session,order_id: int, user_id: uuid.UUID, delivered: bool) -> bool:
        stmt = update(OrderModel).where(
            OrderModel.id == order_id,
            OrderModel.user_id == user_id
        ).values(delivered=delivered)
        result = db.execute(stmt)
        db.commit()
        return result.rowcount > 0
        
    staticmethod
    def cancel_order(db: Session,order_id: int, user_id: uuid.UUID) -> bool:
        stmt = delete(order_product_association).where(
            order_product_association.c.order_id == order_id,
        )
        db.execute(stmt)
        stmt = delete(OrderModel).where(
            and_(
                OrderModel.id == order_id,
                OrderModel.user_id == user_id
            )
        )
        db.execute(stmt)

        db.commit()
        return True
        
    @staticmethod
    def count_orders(db: Session,user_id: uuid.UUID) -> int:
        stmt = select(func.count(OrderModel.id)).where(OrderModel.user_id == user_id)
        result = db.execute(stmt)
        return result.scalar_one()