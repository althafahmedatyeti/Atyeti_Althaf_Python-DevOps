import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate
from passlib.context import CryptContext
from utils.jwt_token import create_access_token

# Configure logger
logger = logging.getLogger(__name__)


# Create a password hashing context
pwd_creator = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database after validating uniqueness and hashing the password.
    """
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            logger.warning(f"Attempt to register with existing email: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered.")

        hashed_password = pwd_creator.hash(user.password)
        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User created successfully: {user.email}")
        return {
            "message": "User created successfully",
            "name": new_user.name,
            "email": new_user.email
        }

    except Exception as e:
        logger.error(f"Error while creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

def user_login(db: Session, email: str, password: str):
    """
    Authenticate user by verifying email and password. Returns JWT token if successful.
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.warning(f"Login attempt with unregistered email: {email}")
            return {
                "success": False,
                "message": "User not found."
            }

        if not pwd_creator.verify(password, user.password):
            logger.warning(f"Incorrect password attempt for user: {email}")
            return {
                "success": False,
                "message": "Incorrect password."
            }

        token = create_access_token(data={"user_id": user.user_id})
        logger.info(f"Login successful for user: {email}")

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        logger.error(f"Login failed due to error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed due to server error.")
