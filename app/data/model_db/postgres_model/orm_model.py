from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class UserOrm(Base):  
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]

    # Один пользователь может иметь много заказов
    orders: Mapped[list['OrderOrm']] = relationship(back_populates='user')


class ProductOrm(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    delivered: Mapped[bool]

    # Один продукт может быть во многих заказах
    orders: Mapped[list['OrderOrm']] = relationship(back_populates='product')


class OrderOrm(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True) 
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    delivered: Mapped[bool]
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    # Каждый заказ принадлежит одному пользователю и одному продукту
    user: Mapped['UserOrm'] = relationship(back_populates='orders') 
    product: Mapped['ProductOrm'] = relationship(back_populates='orders') 