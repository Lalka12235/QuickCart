from sqlalchemy import select,insert,update,delete,and_,func
from app.config.session import Session
from app.schemas.order_schema import OrderSchema
from app.models.orm_model import OrderModel, order_product_association
import uuid


class OrderRepostiroy:

    @staticmethod
    def get_order_by_id(order_id: int, user_id: uuid.UUID) -> OrderModel | None:
        with Session() as session:
            stmt = select(OrderModel).where(
                OrderModel.id == order_id,
                OrderModel.user_id == user_id
            )
            result = session.execute(stmt)
            return result.scalar_one_or_none()


    @staticmethod
    def get_all_order_by_id(user_id: int) -> OrderModel:
        with Session() as session:
            stmt = select(OrderModel).where(OrderModel.user_id == user_id)
            result = session.execute(stmt)
            return result.scalars().all()
        
    
    @staticmethod
    def add_order(order_data: OrderSchema, user_id: uuid.UUID) -> OrderModel:
        with Session() as session:
            # 1. Создаём заказ
            new_order = OrderModel(
                address=order_data.address,
                delivered=order_data.delivered,
                user_id=user_id
            )
            session.add(new_order)
            session.flush()  # чтобы получить new_order.id до коммита

            # 2. Добавляем записи в ассоциативную таблицу order_products
            for item in order_data.products:
                stmt = insert(order_product_association).values(
                    order_id=new_order.id,
                    product_id=item.product_id
                )
                session.execute(stmt)

            # 3. Фиксируем транзакцию
            session.commit()

            # 4. Обновляем объект заказа
            session.refresh(new_order)
            return new_order


    @staticmethod
    def update_order_delivery_status(order_id: int, user_id: uuid.UUID, delivered: bool) -> bool:
        with Session() as session:
            stmt = update(OrderModel).where(
                OrderModel.id == order_id,
                OrderModel.user_id == user_id
            ).values(delivered=delivered)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
        
    @staticmethod
    def delete_order(id: int, user_id: uuid.UUID) -> bool:
        with Session() as session:
            stmt = delete(OrderModel).where(
                and_(
                    OrderModel.id == id,OrderModel.user_id == user_id
            ))
            session.execute(stmt)
            session.commit()
            return True
        
    @staticmethod
    def count_orders(user_id: uuid.UUID) -> int:
        with Session() as session:
            stmt = select(func.count(OrderModel.id)).where(OrderModel.user_id == user_id)
            result = session.execute(stmt)
            return result.scalar_one()
        

    @staticmethod
    def get_products_by_order_id(order_id: int) -> list:
        with Session() as session:
            order = session.get(OrderModel, order_id)
            return order.products
