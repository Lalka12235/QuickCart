from fastapi import HTTPException,status
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreateSchema,UserDeleteSchema,UserOutSchema

class UserService:

    @staticmethod
    def create_user(user: UserCreateSchema) -> dict:
        exist_user = UserRepository.get_user_by_email(user.email)

        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User exist'
            )
        
        result = UserRepository.create_user(user.email,user.username,user.password)

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
    def delete_user(user: UserDeleteSchema) -> dict:
        exist_user = UserRepository.get_user_by_email(user.email)

        if not exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User dont exist'
            )
        
        result = UserRepository.delete_user(user.email,user.password)

        return {
        "success": True,
        "detail": "user delete",
        }
    

    @staticmethod
    def get_user_by_email(email: str) -> UserOutSchema:
        user = UserRepository.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        
        return {
            'success': True,
            'derail': 'user found',
            'user':{
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }