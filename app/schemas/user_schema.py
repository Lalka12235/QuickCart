from pydantic import BaseModel, UUID4, EmailStr

class UserCreateSchema(BaseModel):
    email: str
    username: str
    password: str

class UserOutSchema(BaseModel):
    id: UUID4
    email: str
    username: str


class UserDeleteSchema(BaseModel):
    email: str
    password: str