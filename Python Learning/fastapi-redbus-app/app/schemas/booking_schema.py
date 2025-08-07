#Pydantic schema (used for input validation in FastAPI
from pydantic import BaseModel
class BookingRequest(BaseModel):
    #user_id: int
    bus_id: int
    seat_number: int
    travel_date: str   
# class BusRequest(BaseModel):
#     bus_id: int
#     bus_source: int
#     bus_destination: str
#     bus_name: str
