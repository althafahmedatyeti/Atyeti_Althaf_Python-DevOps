from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_token import verify_token
import logging
import os, sys
print("Python path:", sys.path)
print("Current directory:", os.getcwd())


# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Use HTTPBearer to parse the Authorization header
bearer_scheme = HTTPBearer()

def get_current_users(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Dependency function to authenticate users using JWT token.
    Extracts and verifies token from Authorization header.
    Returns the payload (usually contains user info) if valid.
    """
    token = credentials.credentials  # Extract the actual token string
    logger.debug(f"Token received: {token}")

    # Verify the JWT token
    payload = verify_token(token)

    if payload is None:
        logger.warning("Token verification failed.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"User authenticated successfully. Payload: {payload}")
    return payload
def admin_required(current_user=Depends(get_current_users)):
    if current_user.get("role")!="admin":
        raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only"
        )
    return current_user
def user_required(current_user=Depends(get_current_users)):
    if current_user.get("role")!="user":
        raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: users only"
        )
    return current_user