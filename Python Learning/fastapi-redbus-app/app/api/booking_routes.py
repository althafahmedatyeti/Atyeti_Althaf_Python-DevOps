import logging
from fastapi import FastAPI, HTTPException, APIRouter, Query, Depends, status
from schemas.booking_schema import BookingRequest
from services.booking_service import (
    book_ticket,
    get_all_bookings,
    get_available_seats,
    cancel_booking,
    get_booking_by_user
)
from database import get_db
from sqlalchemy.orm import Session
from utils.auth_dependencies import get_current_users

# Initialize router and logger
router = APIRouter()
logger = logging.getLogger(__name__)

# Endpoint to book a ticket (protected by JWT token)
@router.post("/booking", status_code=status.HTTP_201_CREATED)
def book_ticket_(
    request: BookingRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_users)
):
    """
    Book a seat on a bus. Requires valid JWT token.
    """
    try:
        user_id = current_user["user_id"]  # Extract user ID from JWT
        return book_ticket(db, request, user_id)
    except Exception as e:
        logger.exception("Booking failed.")  # Logs full traceback
        raise HTTPException(status_code=500, detail="Internal server error during booking.")


# Health check endpoint to verify API is running
@router.get("/health")
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}


# Get current logged-in user's bookings
@router.get("/my_bookings")
def get_bookings(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_users)
):
    """
    Retrieve all bookings for the authenticated user.
    """
    try:
        user_id = current_user["user_id"]
        return get_booking_by_user(db, user_id)
    except Exception as e:
        logger.exception("Failed to fetch user bookings.")
        raise HTTPException(status_code=500, detail="Could not retrieve bookings.")


# Get available seats for a bus on a particular travel date
@router.get("/available-seats")
def get_available_seats_route(
    bus_id: int,
    travel_date: str,
    db: Session = Depends(get_db)
):
    """
    Get all available seats for a given bus and travel date.
    """
    try:
        return get_available_seats(db, bus_id, travel_date)
    except Exception as e:
        logger.exception("Error fetching available seats.")
        raise HTTPException(status_code=500, detail="Failed to fetch available seats.")


# Cancel a specific booking
@router.delete("/cancel/{booking_id}")
def cancel_booking_(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Cancel a booking by its booking ID.
    """
    try:
        return cancel_booking(db, booking_id)
    except Exception as e:
        logger.exception(f"Cancellation failed for booking_id: {booking_id}")
        raise HTTPException(status_code=500, detail="Could not cancel booking.")


# Get bookings for a specific user (admin or support use-case)
@router.get("/user-bookings/{user_id}")
def get_booking_by_user_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve all bookings made by a specific user (used for admin/support dashboards).
    """
    try:
        return get_booking_by_user(db, user_id)
    except Exception as e:
        logger.exception(f"Failed to fetch bookings for user_id: {user_id}")
        raise HTTPException(status_code=500, detail="Could not retrieve user bookings.")
