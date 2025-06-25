from pydantic import BaseModel, UUID4, EmailStr, Field

class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=6, description="User password")


class UserOutSchema(BaseModel):
    id: UUID4 = Field(..., description="User unique identifier")
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., description="Username")


class UserDeleteSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")