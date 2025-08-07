from fastapi import APIRouter, HTTPException, Depends, status
from schemas.user_schema import UserCreate, UserLogin
from services.user_service import create_user, user_login
from database import get_db
from sqlalchemy.orm import Session
import logging

# Set up logging
logger = logging.getLogger(__name__)


# Initialize FastAPI router
router = APIRouter()

# User Registration Endpoint
@router.post("/register")
def register_user(
    request: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registers a new user with email and password.
    """
    try:
        logger.info(f"Attempting to register user with email: {request.email}")
        response = create_user(db, request)
        logger.info(f"User registered successfully with email: {request.email}")
        return response
    except Exception as e:
        logger.error(f"User registration failed for email {request.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while registering the user."
        )

# User Login Endpoint
@router.post("/login")
def login_user(
    request: UserLogin,
    db: Session = Depends(get_db)
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
