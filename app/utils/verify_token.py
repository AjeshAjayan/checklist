from fastapi import HTTPException
from settings import settings
from jose import jwt, JWTError

def verify_token(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")