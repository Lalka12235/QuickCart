from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase,relationship
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass

#User model
class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]

    products: Mapped[list['ProductOrm']]= relationship(back_populates='users')

#Product model
class ProductOrm(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    users: Mapped[list['UsersOrm']] = relationship(back_populates='products')