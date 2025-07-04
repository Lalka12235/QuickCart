from sqlalchemy import Table,Column,ForeignKey,Integer
from app.models.base import Base


order_product_association = Table(
    'order_products',
    Base.metadata,
    Column('order_id', ForeignKey('orders.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, nullable=False, default=1),
)