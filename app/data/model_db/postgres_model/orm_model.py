from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey, Table,Column, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid



class Base(DeclarativeBase):
    pass


class UserModel(Base):  
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]

    orders: Mapped[list['OrderModel']] = relationship(back_populates='user')
    reviews: Mapped[list['ReviewModel']] = relationship(back_populates='user')


order_product_association = Table(
    'order_products',
    Base.metadata,
    Column('order_id', ForeignKey('orders.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True)
)


class ProductModel(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]

    orders: Mapped[list['OrderModel']] = relationship(
    secondary=order_product_association,
    back_populates="products"
    )

    reviews: Mapped[list['ReviewModel']] = relationship(back_populates='product')


class OrderModel(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True) 
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    delivered: Mapped[bool]
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))

    user: Mapped['UserModel'] = relationship(back_populates='orders') 
    products: Mapped[list['ProductModel']] = relationship(
    secondary=order_product_association,
    back_populates="orders"
)


class ReviewModel(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    rating: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    product: Mapped['ProductModel'] = relationship(back_populates='reviews')
    user: Mapped['UserModel'] = relationship(back_populates='reviews')