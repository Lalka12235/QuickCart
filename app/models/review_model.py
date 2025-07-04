from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Text,ForeignKey
import uuid
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product_model import ProductModel
    from app.models.user_model import UserModel

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