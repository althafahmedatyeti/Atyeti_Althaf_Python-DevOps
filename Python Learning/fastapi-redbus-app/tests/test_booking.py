from app.services.booking_service import BookingService

service = BookingService()

# Book a seat
print(service.book_ticket(user_id=1, bus_id=101, seat_number=1, travel_date="2023-10-01"))

# Try booking the same again
print(service.book_ticket(user_id=1, bus_id=101, seat_number=2, travel_date="2023-10-01"))

# Book for another user
print(service.book_ticket(user_id=2, bus_id=101, seat_number=1, travel_date="2023-10-01"))
