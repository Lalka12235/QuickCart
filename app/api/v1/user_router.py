from app.schemas.user_schema import UserCreateSchema,UserDeleteSchema
from app.services.user_service import UserService
from fastapi import APIRouter

user = APIRouter(
    tags=['User'],
)

@user.get('/users/{email}',summary='Get user by email')
async def get_user_by_email(email: str):
    return UserService.get_user_by_email(email)


@user.post('/users',summary='Create a new user',)
async def create_user(user: UserCreateSchema):
    return UserService.create_user(user)


@user.delete('/users',summary='Delete a user',)
async def delete_user(user: UserDeleteSchema):
    return UserService.delete_user(user)