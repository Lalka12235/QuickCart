from fastapi import HTTPException,status
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreateSchema,UserDeleteSchema
from typing import Any
from app.utils.hash import verify_pass
from sqlalchemy.orm import Session


class UserService:

    @staticmethod
    def create_user(db: Session,user: UserCreateSchema) -> dict[str,Any]:
        exist_user = UserRepository.get_user_by_email(db,user.email)

        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User exist'
            )
        
        result = UserRepository.create_user(db,user.email,user.username,user.password)

        return {
        "success": True,
        "detail": "user created",
        "result": 
            {
            "id": str(result.id),
            "email": result.email,
            "username": result.username
            }
        }
    

    @staticmethod
    def delete_user(db: Session,user: UserDeleteSchema) -> dict[str,Any]:
        exist_user = UserRepository.get_user_by_email(db,user.email)

        if not exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User dont exist'
            )
        verify = verify_pass(user.password,exist_user.password)

        if not verify:
            raise HTTPException(
                status_code=400,
                detail='Invalid email or password'
            )


        result = UserRepository.delete_user(db,user.email)

        return {
        "success": True,
        "detail": "user delete",
        }
    

    @staticmethod
    def get_user_by_email(db: Session,email: str) -> dict[str,Any]:
        user = UserRepository.get_user_by_email(db,email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        
        return user
        #return {
        #    'success': True,
        #    'detail': 'user found',
        #    'user':{
        #        'user_id': user.id,
        #        'username': user.username,
        #        'email': user.email,
        #    }
        #}