from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config.config import settings
from jose import jwt, JWTError

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

#---------------------- ACCESS TOKEN ---------------------#
def create_access_token(data: dict):
    """
    Create access token
    """
    to_encode = data.copy()
    # FIX: Use timezone-aware datetime
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire
    })
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


#------------------- CURRENT MP --------------------------------#
def get_current_mp(token: str = Depends(oauth2_schema)) -> dict:
    creds_Exec = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        id = payload.get("id")
        mp_name: Optional[str] = payload.get("mp_name")
        house: Optional[str] = payload.get("house")
        state: Optional[str] = payload.get("state")
        constituency: Optional[str] = payload.get("constituency")
        dist: Optional[str] = payload.get("dist")
        dm_id: Optional[int] = payload.get("dm_id")
        
        if not id or not mp_name:
            raise creds_Exec
    except JWTError:
        raise creds_Exec
    
    return {
        "id": id,
        "mp_name": mp_name,
        "constituency": constituency,
        "house": house,
        "state": state,
        "dist": dist,
        "dm_id": dm_id
    }
    
    
#------------------- CURRENT DM --------------------------------#
def get_current_dm(token: str = Depends(oauth2_schema)) -> dict:
    creds_Exec = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        id = payload.get("id")
        
        if not id:
            raise creds_Exec
    except JWTError:
        raise creds_Exec
    
    return {
        "id": payload.get("id"),
        "dm_name": payload.get("dm_name"),
        "dist": payload.get("dist"),
        "state": payload.get("state"),
    }