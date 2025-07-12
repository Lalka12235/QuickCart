from sqlalchemy import select, delete
from app.models.user_model import UserModel
from app.utils.hash import make_hash_pass
from sqlalchemy.orm import Session

class UserRepository:

    @staticmethod
    def create_user(db: Session,email: str, username: str, password: str):
        hash_pass = make_hash_pass(password)
        new_user = UserModel(
            email=email,
            username=username,
            password=hash_pass
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user


    @staticmethod
    def get_user_by_email(db: Session,email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = db.execute(stmt)
        return result.scalar_one_or_none()


    @staticmethod
    def delete_user(db: Session,email: str) -> bool:
        stmt = delete(UserModel).where(
            UserModel.email == email,
            )
        db.execute(stmt)
        db.commit()
        return True
        
    