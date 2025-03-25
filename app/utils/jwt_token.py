import jwt
from fastapi import HTTPException
from datetime import datetime,timedelta

SECRET_KEY = ''
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRED_MINUTES = 15

def encode_jwt(payload,secret_key,algorithm,expire_minutes=ACCESS_TOKEN_EXPIRED_MINUTES):
    expired = datetime.utcnow()+ timedelta(minutes=expire_minutes)
    payload.update({'exp':expired})
    token = jwt.encode(payload,secret_key,algorithm=algorithm)
    return token
    

def decode_jwt(token,secret_key,alghorithm):
    try:
        decoded = jwt.decode(token,secret_key,algorithms=[alghorithm])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")