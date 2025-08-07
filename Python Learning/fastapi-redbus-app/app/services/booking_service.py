import logging
from datetime import datetime
from typing import List
from sqlalchemy import func

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.booking import Bookings
from models.bus import Bus
from schemas.booking_schema import BookingRequest

# Setup logger
logger = logging.getLogger(__name__)
total_seats=40


# You can configure logging output to file/console if needed.

def book_ticket(db: Session, request: BookingRequest, user_id: int):
    """
    Books a seat for the user on a specific bus and travel date.

    Raises:
        HTTPException: if the seat is already booked.
    """
    logger.info(f"Attempting to book seat {request.seat_number} on bus {request.bus_id} for user {user_id}")

    try:
        existing_booking = db.query(Bookings).filter(
            Bookings.bus_id == request.bus_id,
            Bookings.travel_date == request.travel_date,
            Bookings.seat_number == request.seat_number
        ).first()

        if existing_booking:
            logger.warning(f"Seat {request.seat_number} already booked for bus {request.bus_id} on {request.travel_date}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Seat already booked for this bus on the selected date."
            )

        bookings = Bookings(
            user_id=user_id,
            bus_id=request.bus_id,
            seat_number=request.seat_number,
            travel_date=request.travel_date
        )
        db.add(bookings)
        db.commit()
        db.refresh(bookings)

        logger.info(f"Booking successful: {bookings.booking_id}")
        return {
            "success": True,
            "message": "Booking successful",
            "booking_id": bookings.booking_id,
            "bus_id": bookings.bus_id,
            "seat_number": bookings.seat_number,
            "user_id": bookings.user_id
        }

    except Exception as e:
        logger.exception("Failed to book ticket")
        raise HTTPException(status_code=500, detail="Booking failed due to internal error")


def get_all_bookings(db: Session) -> List[dict]:
    """
    Returns all bookings from the database.
    """
    logger.info("Fetching all bookings")
    try:
        bookings = db.query(Bookings).all()
        return [
            {
                "id": b.booking_id,
                "user_id": b.user_id,
                "bus_id": b.bus_id,
                "seat_number": b.seat_number,
                "travel_date": str(b.travel_date)
            }
            for b in bookings
        ]
    except Exception as e:
        logger.exception("Failed to fetch all bookings")
        raise HTTPException(status_code=500, detail="Could not retrieve bookings")


def get_available_seats(db: Session, bus_id: int, travel_date: str) -> List[int]:
    """
    Returns all booked seat numbers for a given bus on a travel date.
    """
    logger.info(f"Checking available seats for bus {bus_id} on {travel_date}")
    try:
        booked_seats = db.query(func.count(Bookings.bus_id)).filter(
            Bookings.bus_id == bus_id,
            Bookings.travel_date == travel_date
        ).scalar()
        return total_seats-booked_seats
    except Exception as e:
        logger.exception("Failed to get available seats")
        raise HTTPException(status_code=500, detail="Could not fetch seat availability")


def cancel_booking(db: Session, booking_id: int):
    """
    Cancels a booking based on its ID.
    """
    logger.info(f"Attempting to cancel booking ID {booking_id}")
    try:
        booking = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
        if not booking:
            logger.warning(f"Booking ID {booking_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found."
            )

        db.delete(booking)
        db.commit()
        logger.info(f"Booking ID {booking_id} cancelled successfully")

        return {
            "status": True,
            "message": "Booking cancelled successfully."
        }
    except Exception as e:
        logger.exception("Failed to cancel booking")
        raise HTTPException(status_code=500, detail="Cancellation failed")


def get_booking_by_user(db: Session, user_id: int) -> List[dict]:
    """
    Fetches all bookings for a specific user.
    """
    logger.info(f"Fetching bookings for user ID {user_id}")
    try:
        bookings = db.query(Bookings).filter(Bookings.user_id == user_id).all()
        if not bookings:
            logger.warning(f"No bookings found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No bookings found for this user."
            )
        return [
            {
                "booking_id": b.booking_id,
                "user_id": b.user_id,
                "bus_id": b.bus_id,
                "seat_number": b.seat_number,
                "travel_date": str(b.travel_date)
            } 
            for b in bookings
        ]
    except Exception as e:
        logger.exception("Failed to fetch user's bookings")
        raise HTTPException(status_code=500, detail="Could not retrieve user bookings")


def get_available_seats_count(db: Session, bus_id: int, travel_date: str) -> int:
    """
    Returns the number of seats booked for a bus on a specific travel date.
    """
    logger.info(f"Getting booked seat count for bus {bus_id} on {travel_date}")
    try:
        booked_seats = get_available_seats(db, bus_id, travel_date)
        return len(booked_seats)
    except Exception as e:
        logger.exception("Failed to get booked seat count")
        raise HTTPException(status_code=500, detail="Could not fetch seat count")












# from typing import List, Dict
# class BookingService:
#     def __init__(self):
#         # In-memory storage to hold all bookings (used like a fake database)
#         self.bookings_db: List[Dict] = []
#         # Total number of seats available on the bus
#         self.Total_Seats: int = 40

#     def book_ticket(self, user_id: int, bus_id: int, seat_number: int, travel_date: str):
#         #Books a ticket for a user if they haven't already booked one on the same bus and date.
        
#         for booking in self.bookings_db:
#             if booking['bus_id'] == bus_id  and booking['travel_date'] == travel_date and booking['seat_number'] == seat_number:
#                 return {"error": "Seat already booked on this bus."}

#         new_booking = {
#             "user_id": user_id,
#             "bus_id": bus_id,
#             "seat_number": seat_number,
#             "travel_date": travel_date
#         }
#         self.bookings_db.append(new_booking)
#         return {"message": "Booking successful",
#                 "booking":  new_booking
#                }

#     def get_user_bookings(self, user_id: int):
#         #Returns all bookings made by a specific user.
    
#         return [booking for booking in self.bookings_db if booking['user_id'] == user_id]

#     def get_all_bookings(self):
        
#         #Returns a list of all bookings in the system.
#         return self.bookings_db

#     def get_booked_seats(self, bus_id: int, travel_date: str):
#         """Returns a seat map showing which seats are available and which are booked
#         for a given bus and travel date.
#         """
#         seat_map = []

#         # Create a dict of all booked seat numbers for this bus and date
#         booked_seats = {
#             booking['seat_number']: booking['user_id']
#             for booking in self.bookings_db
#             if booking['bus_id'] == bus_id and booking['travel_date'] == travel_date
#         }

#         # Loop through all seat numbers and check their status
#         for seat in range(1, self.Total_Seats + 1):
#             if seat in booked_seats:
#                 seat_map.append({
#                     "seat_number": seat,
#                     "status": "unavailable",
#                     "user_id": booked_seats[seat]
#                 })
#             else:
#                 seat_map.append({
#                     "seat_number": seat,
#                     "status": "available"
#                 })
#         return seat_map

#     def cancel_booking(self, user_id: int, bus_id: int, travel_date: str):
#         """
# Cancels a booking for a given user, bus, and travel date.
#         """
#         for booking in self.bookings_db:
#             if (
#                 booking['user_id'] == user_id and
#                 booking['bus_id'] == bus_id and
#                 booking['travel_date'] == travel_date
#             ):
#                 self.bookings_db.remove(booking)
#                 return {"message": "Booking cancelled successfully."}
#         return {"error": "No matching booking found to cancel."}


