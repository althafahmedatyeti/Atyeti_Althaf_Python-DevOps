from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
import logging
from fastapi import HTTPException, status

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for JWT token
SECRET_KEY = "supersecretkey"  # Should be stored in environment variables in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """
    Create a JWT token with an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("JWT token created successfully.")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error while creating JWT token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token generation failed."
        )

def verify_token(token: str) -> dict:
    """
    Decode and verify a JWT token.

    Raises:
        HTTPException: If token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info("JWT token verified successfully.")
        return payload

    except ExpiredSignatureError:
        logger.warning("JWT token has expired.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except JWTError:
        logger.warning("Invalid JWT token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed."
        )

