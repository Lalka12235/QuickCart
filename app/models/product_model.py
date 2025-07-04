from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.models.base import Base

from app.models.order_product_model import order_product_association
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order_model import OrderModel
    from app.models.review_model import ReviewModel
    from app.models.payment_model import PaymentModel

    
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
    payments: Mapped['PaymentModel'] = relationship('PaymentModel', back_populates='product')