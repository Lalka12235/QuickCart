from app.data.model_db.postgres_model.orm_model import UserOrm,OrderOrm,ProductOrm
from app.data.model_pydantic.models import User,Product,Order,UpdateProduct, UpdateOrder
from sqlalchemy import create_engine,select,update,delete,insert
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.utils.hash import verify_pass,make_hash_pass
from app.session import Session

class Profile:

    @staticmethod
    def select_user(username):
        with Session() as session:
            stmt = select(UserOrm.username).where(UserOrm.username == username)
            result = session.execute(stmt)
            return result.scalar_one_or_none()
            


    @staticmethod
    def register_user(username: str, password: str):
        with Session() as session:
            users = Profile.select_user(username)

            if users:
                return {'User': 'Exist'}
            
            hash_pass = make_hash_pass(password)
            result = session.execute(insert(UserOrm).values(username=username,password=hash_pass)).scalar()
            session.commit()
            return {'Status': 'success'}
        
    @staticmethod
    def login_user(username: str):
        with Session() as session:
            user = session.execute(select(UserOrm).where(UserOrm.username == username)).scalars().first()
            return user
        
    @staticmethod
    def delete_account(username: str):
        with Session() as session:
            result = session.execute(delete(UserOrm).where(UserOrm.username == username))
            session.commit()
            return result


class ManageOrder:

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
    def create_order(username: str, title: str):
        with Session() as session:
            stmt = select(UserOrm).where(UserOrm.username == username)
            user = session.execute(stmt).scalar_one_or_none()

            if not user:
                return {'User': 'Does not exist'}

            product = ManageProduct.get_one_product(title)

            if not product:
                return {'Product': 'Does not exist'}

            new_order = OrderOrm(
                title=product.title,
                description=product.description,
                price=product.price,
                delivered=False,
                user=user,
                product=product
            )

            session.add(new_order)
            session.commit()

            return {'success': True, 'order_id': new_order.id, 'product_info': {'title': new_order.title,'description': new_order.description,'price': new_order.price}}
    

    @staticmethod
    def update_order(username: str,title: str):
        with Session() as session:
            stmt = select(UserOrm).where(UserOrm.username == username)
            user = session.execute(stmt).scalar_one_or_none()

            if not user:
                return {'User': 'Does not exist'}

            order_stmt = select(OrderOrm).where(OrderOrm.user_id == user.id, OrderOrm.title == title)
            order = session.execute(order_stmt).scalar_one_or_none()

            if not order:
                return {'Order': 'Does not exist'}

            order.delivered = True

            session.commit()

            return {'success': True, 'updated_order': order.title}
        
    
    @staticmethod
    def delete_order(username: str,title: str):
        with Session() as session:
            stmt = select(UserOrm).where(UserOrm.username == username)
            user = session.execute(stmt).scalar_one_or_none()

            if not user:
                return {'User': 'Does not exist'}


            order_stmt = select(OrderOrm).where(OrderOrm.user_id == user.id, OrderOrm.title == title)
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
            result = session.execute(select(ProductOrm)).fetchall()
            return result

    @staticmethod
    def get_one_product(title:str):
        with Session() as session:
            result = session.execute(select(ProductOrm).where(ProductOrm.title == title)).scalar_one_or_none()
            return result
    
    @staticmethod
    def create_product(product: Product):
        with Session() as session:
            stmt = insert(ProductOrm).values(title=product.title,description=product.description,price=product.price)
            result = session.execute(stmt).scalar()
            session.commit()
            return {'Result': product}

    @staticmethod
    def update_product(title: str,product: UpdateProduct):
        with Session() as session:
            result = session.execute(update(ProductOrm).where(ProductOrm.title == title).values(title=product.title,description=product.description,price=product.price))
            session.commit()
            return {'Result': product}
    
    @staticmethod
    def delete_product(title: str):
        with Session() as session:
            result = session.execute(delete(ProductOrm).where(ProductOrm.title == title))
            session.commit()
            return result        