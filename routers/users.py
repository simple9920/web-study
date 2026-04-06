from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas
from auth import verify_password, create_access_token
from dependencies import get_current_user
from models import User

router = APIRouter()


@router.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)

    if new_user is None:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def read_users_me(current_user = Depends(get_current_user)):
    return current_user