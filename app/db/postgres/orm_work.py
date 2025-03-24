from app.data.model_db.postgres_model.orm_model import UserOrm,OrderOrm,ProductOrm
from app.data.model_pydantic.models import User,Product,Order,UpdateProduct, UpdateOrder
from sqlalchemy import create_engine,select,update,delete,insert
from sqlalchemy.orm import sessionmaker
from app.config import settings


engine = create_engine(
    url=settings.db_url,
    echo=True,
)

Session = sessionmaker(bind=engine)


class Profile:

    @staticmethod
    def register_user(user: User):
        with Session() as session:
            result = session.execute(insert(UserOrm).values(user))
            session.commit()
            return result
        
    @staticmethod
    def delete_account(username: str):
        with Session() as session:
            result = session.execute(delete(UserOrm).where(UserOrm.username == username))
            session.commit()
            return result


class ManegeOrder:

    @staticmethod
    def select_order(username: str):
        with Session() as session:
            stmt = select(UserOrm).where(UserOrm.username == username)
            user = session.execute(stmt).scalar_one_or_none()

            if not user:
                return {'User': 'Does not exist'}
            
            result = session.execute(select(OrderOrm).where(OrderOrm.user_id == user.id)) 
            return result.fetchall()
        
    
    @staticmethod
    def create_order(username: str, order: Order):
        with Session() as session:
            stmt = select(UserOrm).where(UserOrm.username == username)
            user = session.execute(stmt).scalar_one_or_none()

            if not user:
                return {'User': 'Does not exist'}

            product = ManageProduct.get_one_product(order.title)

            if not product:
                return {'Product': 'Does not exist'}

            new_order = OrderOrm(
                title=order.title,
                description=order.description,
                price=order.price,
                delivered=order.delivered,
                user=user,
                product=product
            )

            session.add(new_order)
            session.commit()

            return {'success': True, 'order_id': new_order.id, 'product_title': new_order.product.title}
    

    @staticmethod
    def update_order(username: str, upd_order: UpdateOrder):
        with Session() as session:
            stmt = select(UserOrm).where(UserOrm.username == username)
            user = session.execute(stmt).scalar_one_or_none()

            if not user:
                return {'User': 'Does not exist'}

            order_stmt = select(OrderOrm).where(OrderOrm.user_id == user.id, OrderOrm.title == upd_order.title)
            order = session.execute(order_stmt).scalar_one_or_none()

            if not order:
                return {'Order': 'Does not exist'}

            order.delivered = upd_order.delivered

            session.commit()

            return {'success': True, 'updated_order': order.title}
        
    
    staticmethod
    def delete_order(username: str):
        with Session() as session:
            stmt = select(UserOrm).where(UserOrm.username == username)
            user = session.execute(stmt).scalar_one_or_none()

            if not user:
                return {'User': 'Does not exist'}


            order_stmt = select(OrderOrm).where(OrderOrm.user_id == user.id)
            order = session.execute(order_stmt).scalar_one_or_none()

            if not order:
                return {'Order': 'Does not exist'}

            session.execute(delete(OrderOrm).where(OrderOrm.id == order.id))
            session.commit()

            return {'success': True, 'deleted_order_id': order.id}





class ManageProduct:

    @staticmethod
    def get_all_products():
        with Session() as session:
            result = session.execute(select(ProductOrm))
            return result

    @staticmethod
    def get_one_product(title:str):
        with Session() as session:
            result = session.execute(select(ProductOrm).where(ProductOrm.title == title))
            return result
    
    @staticmethod
    def create_product(product: Product):
        with Session() as session:
            result = session.execute(insert(ProductOrm).values(**product))
            session.commit()
            return result

    @staticmethod
    def update_product(title: str,product: UpdateProduct):
        with Session() as session:
            result = session.execute(update(ProductOrm).where(ProductOrm.title == title).values(product))
            session.commit()
            return result
    
    @staticmethod
    def delete_product(title: str):
        with Session() as session:
            result = session.execute(delete(ProductOrm).where(ProductOrm.title == title))
            session.commit()
            return result
        
