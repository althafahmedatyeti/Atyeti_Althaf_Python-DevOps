import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate
from passlib.context import CryptContext
from utils.jwt_token import create_access_token
from models.admin import Admin

logger = logging.getLogger(__name__)
#Create a password hashing context
pwd_creator = CryptContext(schemes=["bcrypt"], deprecated="auto")

def admin_login(db: Session, user_name: str, password: str):
    """
    Authenticate admin by verifying user_name and password. Returns JWT token if successful.
    """
    try:
        admin = db.query(Admin).filter(Admin.user_name == user_name).first()
        if not admin:
            logger.warning(f"Login attempt with unregistered admin: {user_name}")
            return {
                "success": False,
                "message": "Admin not found."
            }

        if not pwd_creator.verify(password, admin.password):
            logger.warning(f"Incorrect password attempt for admin: {user_name}")
            return {
                "success": False,
                "message": "Incorrect password."
            }

        token = create_access_token(data={
            "admin_id": admin.id,
            "user_name": admin.user_name,
            "role": admin.role
        })

        logger.info(f"Login successful for admin: {user_name}")

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        logger.error(f"Admin login failed due to error: {str(e)}")
        raise HTTPException(status_code=500, detail="Admin login failed due to server error.")
    


