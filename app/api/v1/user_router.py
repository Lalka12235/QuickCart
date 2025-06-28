from app.schemas.user_schema import UserCreateSchema,UserDeleteSchema
from app.services.user_service import UserService
from fastapi import APIRouter

user = APIRouter(
    tags=['User'],
)

@user.get('/users/{email}')
async def get_user_by_email(email: str):
    return UserService.get_user_by_email(email)


@user.post('/users')
async def create_user(user: UserCreateSchema):
    return UserService.create_user(user)


@user.delete('/users')
async def delete_user(user: UserDeleteSchema):
    return UserService.delete_user(user)