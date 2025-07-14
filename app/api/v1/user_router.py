from app.schemas.user_schema import UserCreateSchema,UserDeleteSchema
from app.services.user_service import UserService
from fastapi import APIRouter,Depends
from app.config.session import get_db
from sqlalchemy.orm import Session
from typing import Annotated

user = APIRouter(
    tags=['User'],
)

db_dependency = Annotated[Session,Depends(get_db)]

@user.get('/users/{email}',summary='Get user by email')
async def get_user_by_email(email: str, db: db_dependency):
    return UserService.get_user_by_email(db,email)


@user.post('/users',summary='Create a new user',)
async def create_user(user: UserCreateSchema, db: db_dependency):
    return UserService.create_user(db,user)


@user.delete('/users',summary='Delete a user',)
async def delete_user(user: UserDeleteSchema, db: db_dependency):
    return UserService.delete_user(db,user)