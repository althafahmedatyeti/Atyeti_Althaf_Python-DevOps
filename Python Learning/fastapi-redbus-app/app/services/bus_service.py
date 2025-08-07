from models.bus import Bus
from sqlalchemy.orm import Session
from schemas.bus_schema import BusRequest
from services.booking_summary_service import create_summary
from models.booking import Bookings
import logging

logger = logging.getLogger(__name__)

def add_buses(db: Session, request: BusRequest):
    """
    Adds a new bus to the database if it doesn't already exist.
    """
    try:
        logger.info(f"Trying to add bus: {request.bus_id}")
        existing_bus = db.query(Bus).filter(Bus.bus_id == request.bus_id).first()
        if existing_bus:
            logger.warning(f"Bus {request.bus_id} already exists.")
            return {"success": False, "message": "Bus Exists."}

        new_bus = Bus(
            bus_id=request.bus_id,
            bus_source=request.bus_source,
            bus_destination=request.bus_destination,
            bus_name=request.bus_name
        )
        db.add(new_bus)
        db.commit()
        db.refresh(new_bus)
        logger.info(f"Bus {new_bus.bus_id} added successfully.")
        return {
            "success": True,
            "message": "Bus added successfully",
            "bus_id": new_bus.bus_id,
            "bus_source": new_bus.bus_source,
            "bus_destination": new_bus.bus_destination,
            "bus_name": new_bus.bus_name
        }
    except Exception as e:
        logger.error(f"Error while adding bus: {str(e)}")
        return {"success": False, "message": "Internal Server Error"}


def Remove_Bus(db: Session, bus_id: int):
    """
    Deletes a bus from the database if it exists.
    """
    try:
        logger.info(f"Trying to remove bus: {bus_id}")
        bus = db.query(Bus).filter(Bus.bus_id == bus_id).first()
        if not bus:
            logger.warning(f"Bus {bus_id} not found.")
            return {"success": False, "message": "Bus not found."}

        db.delete(bus)
        db.commit()
        logger.info(f"Bus {bus_id} removed successfully.")
        return {"success": True, "message": "Bus removed successfully."}
    except Exception as e:
        logger.error(f"Error while removing bus: {str(e)}")
        return {"success": False, "message": "Internal Server Error"}


def get_all_buses(db: Session):
    """
    Retrieves all buses from the database.
    """
    try:
        logger.info("Fetching all buses.")
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
    except Exception as e:
        logger.error(f"Error fetching buses: {str(e)}")
        return []


def search_buses(db: Session, source: str, destination: str, travel_date: str):
    """
    Searches buses based on source and destination, then returns booking summary for matching buses.
    """
    try:
        logger.info(f"Searching buses from {source} to {destination} on {travel_date}")
        matching_buses = db.query(Bus).filter(
            Bus.bus_source.ilike(f"%{source}%"),
            Bus.bus_destination.ilike(f"%{destination}%")
        ).all()

        if not matching_buses:
            logger.warning("No matching buses found.")
            return ["No bus found"]

        summaries = []
        for bus in matching_buses:
            summary = create_summary(db, bus.bus_id, travel_date)
            if summary:
                summaries.append(summary)

        logger.info(f"Found {len(summaries)} summaries.")
        return summaries
    except Exception as e:
        logger.error(f"Error in search_buses: {str(e)}")
        return ["Internal Server Error"]
