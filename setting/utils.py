from datetime import datetime, timedelta, timezone
import math
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from setting.config import settings
from db.models import User
from db import database

# python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 1440 

security = HTTPBearer()

def create_token(data: dict, expire_minutes: int):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_access_token(data: dict, expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES):
    return create_token(data, expire_minutes)
    
def create_refresh_token(data: dict, expire_minutes = REFRESH_TOKEN_EXPIRE_MINUTES):
    return create_token(data, expire_minutes)

def get_current_user(db: Session = Depends(database.get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=404, detail="Invalid token payload")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return (db, {"user_id": user.id, "username": user.username}, token) 

def get_offset_limit(page_size: int = 10, page_index: int = 0):
    if page_size <= 0:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Incorrect page size {page_size}. Page size must be greater than 0"
        )
    if page_index < 0:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Incorrect page index {page_index}. Page index must be a positive number"
        )
    
    offset = page_index * page_size

    return offset, page_size

def get_pages_records(data, offset_limit):
    offset, limit = offset_limit
    records, total = data
    return {
        "total_pages": math.ceil(total / limit),
        "total_elements": total,
        "has_next": offset + len(records) < total,
        "data": records,
    }

