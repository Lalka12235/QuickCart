from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey
import uuid
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_model import UserModel
    from app.models.product_model import ProductModel

class PaymentModel(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int]
    user_id: Mapped[uuid.UUID] = ForeignKey('users.id')
    product_id: Mapped[int] = ForeignKey('products.id')

    user: Mapped['UserModel'] = relationship(back_populates='payments')
    product: Mapped['ProductModel'] = relationship(back_populates='payments')