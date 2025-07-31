from fastapi import FastAPI, HTTPException, APIRouter, Query, Depends
from schemas.booking_schema import BookingRequest
from services.booking_service import book_ticket , get_all_bookings,get_available_seats ,cancel_booking, get_booking_by_user
from database import get_db
from sqlalchemy.orm import Session
from utils.auth_dependencies import get_current_users
router = APIRouter()

@router.post("/booking")
def book_ticket_(request: BookingRequest, db: Session = Depends(get_db),current_user: dict = Depends(get_current_users)):
    user_id = current_user["user_id"]
    return book_ticket(db, request,user_id)

@router.get("/health")
def health_check():
    return {"status": "ok"}
@router.get("/my_bookings")
def get_bookings(db: Session = Depends(get_db),):
    return get_all_bookings(db)
@router.get("/available-seats")
def get_available_seats(bus_id: int, travel_date: str, db: Session = Depends(get_db)):
    """
    Retrieves all available seats for a given bus and travel date.
    """
    return get_available_seats(db, bus_id, travel_date)
@router.delete("/cancel/{booking_id}")
def cancel_booking_(booking_id:int, db:Session=Depends(get_db)):
    """
    Cancel a booking by its ID.
    """
    return cancel_booking(db, booking_id)
router.get("/user-bookings/{user_id}")
def get_booking_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Gets all bookings made by a specific user.
    """
    return get_booking_by_user(db, user_id)