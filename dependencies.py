from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from database import SessionLocal, get_db
import crud

security = HTTPBearer()

SECRET_KEY = "secret"
ALGORITHM = "HS256"



def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):

    token = credentials.credentials
    print("① token:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("② payload:", payload)

        email: str = payload.get("sub")
        print("③ email:", email)

        if email is None:
            raise HTTPException(status_code=401)

    except JWTError:
        raise HTTPException(status_code=401)
    
    user = crud.get_user_by_email(db, email)

    if user is None:
        raise HTTPException(status_code=401)
    
    return user