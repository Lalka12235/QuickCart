from fastapi import APIRouter,HTTPException,status, Depends
from app.orm_work import Profile
from app.schemas.models import User
from app.auth.auth import get_current_user

user = APIRouter(
    tags=['Proifle']
)

@user.post('/online-shop/user/register')
async def register_user(user: User):
    users = Profile.select_user(user.username)

    if users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    result = Profile.register_user(user.username,user.password)

    return {'Create': True,'Desc': result}

@user.get('/online-shop/user/select')
async def select_user(username: str):
    user = Profile.select_user(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {'user': user}

@user.delete('/online-shop/user/delete')
async def delete_user(username: str, current_user: str = Depends(get_current_user)):
    user = Profile.select_user(username)

    if username != current_user:
        raise HTTPException(status_code=403, detail="")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    delete = Profile.delete_account(username)

    return {'Delete': True, 'Desc': delete}
