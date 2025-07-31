from models.bus import Bus
from sqlalchemy.orm import Session
from schemas.bus_schema import BusRequest
from services.booking_summary_service import create_summary
from models.booking import Bookings

def add_buses(db: Session, request: BusRequest):
        """Retrieves all buses from the database.
        """
        Existing_buses = db.query(Bus).filter(Bus.bus_id == request.bus_id).first()
        if  Existing_buses:
            return {
                "success": False,
                "message": "Bus Exists."
            }
        
        buses = Bus(
            bus_id=request.bus_id,  # Represents the bus ID for which the ticket is being booked
            bus_source=request.bus_source,  # Represents the source of the bus
            bus_destination=request.bus_destination,  # Represents the destination of the bus
            bus_name=request.bus_name  # Represents the name of the bus
        )
        db.add(buses)
        db.commit()
        db.refresh(buses)
        return {
            "message": "Bus added successfully",
            "bus_id": buses.bus_id,
            "bus_source": buses.bus_source,
            "bus_destination": buses.bus_destination,
            "bus_name": buses.bus_name,
        }
def Remove_Bus(db: Session, bus_id: int):
    buses=db.query(Bus).filter(Bus.bus_id == bus_id).first()
    if not buses:
        return {
            "success": False,
            "message": "Bus not found."
        }
    db.delete(buses)
    db.commit() # Commits the transaction to the database   
    return {
        "success": True,
        "message": "Bus removed successfully."
    }
        
def get_all_buses(db: Session):
    """Retrieves all buses from the database.
    """
    buses = db.query(Bus).all()
    return [
        {
            "bus_id": b.bus_id,
            "bus_source": b.bus_source,
            "bus_destination": b.bus_destination,
            "bus_name": b.bus_name
        }
        for b in buses
    ]
def search_buses(db:Session,source:str,destination:str,travel_date:str):
    search_data=db.query(Bus).filter(Bus.bus_source.ilike(f"%{source}"),Bus.bus_destination.ilike(F"%{destination}")).all()
    if not search_data:
        return["no bus found"]
          # Assuming you want to return summaries for all found buses
    summaries = []
    for bus in search_data:
        summary = create_summary(db, bus.bus_id, travel_date)

    if summary:
        summaries.append(summary)
    return summaries 

    