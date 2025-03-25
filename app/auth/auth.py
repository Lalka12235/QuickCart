from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils.jwt_token import encode_jwt, decode_jwt, SECRET_KEY, ALGORITHM
from app.utils.hash import verify_pass
from app.db.postgres.orm_work import Profile

auth = APIRouter(
    tags=['Auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token or expired")
    

@auth.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = Profile.login_user(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_pass(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = encode_jwt({"sub": form_data.username}, SECRET_KEY, ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}