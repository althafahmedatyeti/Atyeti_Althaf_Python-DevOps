from fastapi import FastAPI, HTTPException, APIRouter, Depends
from schemas.user_schema import UserCreate, UserLogin
from services.user_service import create_user, user_login
from database import get_db
from sqlalchemy.orm import Session
router = APIRouter()
@router.post("/register")  # Register a new user
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, request)
@router.post("/login")  # User login
def login_user(request:UserLogin, db: Session = Depends(get_db)):
    return user_login(db, request.email, request.password)