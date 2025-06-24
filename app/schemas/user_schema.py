from pydantic import BaseModel, UUID4, EmailStr

class User(BaseModel):
    email: EmailStr
    username: str
    password: str
