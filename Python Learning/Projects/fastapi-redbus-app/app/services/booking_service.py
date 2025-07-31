from sqlalchemy import create_engine, Column, Integer, String
from models.booking import Bookings 
from models.bus import Bus
from schemas.booking_schema import BookingRequest
from sqlalchemy.orm import Session
from typing import List

def book_ticket(db: Session,request:BookingRequest):  # db should be of type Session,request:Represents user input 
    # bus=db.query(Bus).filter(Bus.bus_id == request.bus_id).first()
    # if not bus:
    #     return {
    #         "sucess": False,
    #         "message": "Bus not found."
    #     }
    #       # Checks if the bus exists
    existing_booking = db.query(Bookings).filter(
         # Checks if a booking already exists for the user
        Bookings.bus_id == request.bus_id,
        Bookings.travel_date == request.travel_date,
        Bookings.seat_number == request.seat_number
    ).first()  # Checks if a booking already exists for the user on the same bus
    if existing_booking:
        return {
            "sucess": False,
            "message": "Seat already booked for this bus on the selected date."}
    
    bookings=Bookings(
        user_id=request.user_id,
        bus_id=request.bus_id,  # Represents the bus ID for which the ticket is being booked
        seat_number=request.seat_number,  # Represents the seat number being booked
        travel_date=request.travel_date  # Represents the date of travel for the booking
    )
    db.add(bookings)
    db.commit()  # Commits the transaction to the database
    db.refresh(bookings)  # Refreshes the instance to reflect the latest state from the database
    return {
            "message": "Booking successful", 
            "Booking_id":bookings.booking_id,
            "bus_id": bookings.bus_id,
            "seat_number": bookings.seat_number,
            "user_id": bookings.user_id,
            }  # Returns a success message with booking details

def get_all_bookings(db: Session)->List[dict]:
    bookings=db.query(Bookings).all() 
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
def get_available_seats(db: Session, bus_id: int, travel_date: str) -> List[int]:
    """
    Retrieves all available seats for a given bus and travel date.
    """
    booked_seats = db.query(Bookings.seat_number).filter(
        Bookings.bus_id == bus_id,
        Bookings.travel_date == travel_date
    ).all()
    return [seats[0] for seats in booked_seats]
def cancel_booking(db:Session,booking_id:int):
    """
    Cancel Bookings
    """
    booking = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
    if not booking:
        return{"status" : False,
            "messege":"Booking not found."}
    db.delete(booking)
    db.commit()
    return {"status": True,
            "message": "Booking cancelled successfully."}
def get_booking_by_user(db: Session, user_id: int) -> List[dict]:
    """
    Gets all bookings made by a specific user.
    """
    bookings=db.query(Bookings).filter(Bookings.user_id == user_id).all()
    if not bookings:
        return {"status": False, "message": "No bookings found for this user."} 
    return [{
        "booking_id": b.booking_id,
        "user_id": b.user_id,
        "bus_id": b.bus_id,
        "seat_number": b.seat_number,
        "travel_date": b.travel_date
    } for b in bookings]
def get_available_seats_count(db: Session, bus_id: int, travel_date: str) -> int:
    booked_seats = get_available_seats(db, bus_id, travel_date)
    return len(booked_seats)






















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


