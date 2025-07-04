from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.models.base import Base
from sqlalchemy import DateTime,ForeignKey
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.order_product_model import order_product_association

if TYPE_CHECKING:
    from app.models.user_model import UserModel
    from app.models.product_model import ProductModel

class OrderModel(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    address: Mapped[str]
    delivered: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))


    user: Mapped['UserModel'] = relationship(back_populates='orders') 
    products: Mapped[list['ProductModel']] = relationship(
    secondary=order_product_association,
    back_populates="orders"
)