from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order_model import OrderModel
    from app.models.review_model import ReviewModel



class UserModel(Base):  
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]

    orders: Mapped[list['OrderModel']] = relationship(back_populates='user')
    reviews: Mapped[list['ReviewModel']] = relationship(back_populates='user')