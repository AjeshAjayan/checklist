from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from app.utils.verify_token import verify_token as verify_token_util
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return verify_token_util(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
