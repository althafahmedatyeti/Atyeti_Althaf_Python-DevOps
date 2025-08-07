from fastapi import FastAPI
import logging
from models.admin import Admin
from utils.auth_dependencies import get_current_users
from database import get_db
from sqlalchemy.orm import Session
from utils.jwt_token import create_access_token,pw
from services.user_service import user_login
from schemas.admin import AdminRequest
from fastapi import APIRouter, HTTPException, Depends, status
from schemas.user_schema import UserCreate, UserLogin
from services.user_service import create_user, user_login
from utils.auth_dependencies import admin_required
# Set up logging
logger = logging.getLogger(__name__)




from fastapi import FastAPI, HTTPException, APIRouter, Query, Depends, status
router=APIRouter()
@router.post("/admin/Login")
def login_user(
    request: AdminRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticates user and returns JWT token if valid.
    """
    try:
        logger.info(f"Attempting login for user with email: {request.email}")
        token = user_login(db, request.email, request.password)
        logger.info(f"Login successful for user with email: {request.email}")
        return token
    except HTTPException as he:
        logger.warning(f"Login failed for user {request.email}: {he.detail}")
        raise he  # Re-raise expected HTTPExceptions
    except Exception as e:
        logger.error(f"Unexpected error during login for {request.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login."
        )
