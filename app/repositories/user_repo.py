from sqlalchemy import select, delete,and_
from app.config.session import Session
from app.models.orm_model import UserModel
from app.utils.hash import make_hash_pass,verify_pass

class UserRepository:

    @staticmethod
    def create_user(email: str, username: str, password: str):
        hash_pass = make_hash_pass(password)
        with Session() as session:
            new_user = UserModel(
                email=email,
                username=username,
                password=hash_pass
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            return new_user


    @staticmethod
    def get_user_by_email(email: str) -> UserModel | None:
        with Session() as session:
            stmt = select(UserModel).where(UserModel.email == email)
            result = session.execute(stmt)
            return result.scalar_one_or_none()


    @staticmethod
    def delete_user(email: str) -> bool:
        with Session() as session:
            stmt = delete(UserModel).where(
                UserModel.email == email,
                )
            session.execute(stmt)
            session.commit()
            return True
        
    