from fastapi import FastAPI, HTTPException, APIRouter, Query, Depends, status
from schemas.bus_schema import BusRequest
from services.bus_service import add_buses, Remove_Bus, get_all_buses, search_buses
from database import get_db
from sqlalchemy.orm import Session
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Initialize the router
router = APIRouter()

#  Add a new bus entry
@router.post("/add-bus")
def add_bus_(
    request: BusRequest,
    db: Session = Depends(get_db)
):
    """
    Adds a new bus to the database.
    """
    try:
        logger.info(f"Adding bus: {request.bus_name} from {request.bus_source} to {request.bus_destination}")
        return add_buses(db, request)
    except Exception as e:
        logger.error(f"Error adding bus: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add bus")


#  Remove a bus using its ID
@router.delete("/remove-bus/{bus_id}")
def remove_bus_(
    bus_id: int,
    db: Session = Depends(get_db)
):
    """
    Deletes a bus record by its ID.
    """
    try:
        logger.info(f"Removing bus with ID: {bus_id}")
        return Remove_Bus(db, bus_id)
    except Exception as e:
        logger.error(f"Error removing bus {bus_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove bus")


# Get all buses
@router.get("/buses")
def get_all_buses_(
    db: Session = Depends(get_db)
):
    """
    Retrieves a list of all available buses.
    """
    try:
        logger.info("Fetching all available buses")
        return get_all_buses(db)
    except Exception as e:
        logger.error(f"Error fetching buses: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch buses")


#  Search for buses based on source, destination, and travel date
@router.get("/search")
def search_bus_(
    source: str = Query(..., description="Source location"),
    destination: str = Query(..., description="Destination location"),
    travel_date: str = Query(..., description="Travel date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Searches for available buses based on source, destination, and date.
    """
    try:
        logger.info(f"Searching buses from {source} to {destination} on {travel_date}")
        return search_buses(db, source, destination, travel_date)
    except Exception as e:
        logger.error(f"Error searching for buses: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to search buses")
