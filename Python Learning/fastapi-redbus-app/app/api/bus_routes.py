from fastapi import FastAPI, HTTPException, APIRouter, Query, Depends
from schemas.bus_schema import BusRequest
from services.bus_service import  add_buses, Remove_Bus,get_all_buses,search_buses
from database import get_db
from utils.auth_dependencies import admin_required
from sqlalchemy.orm import Session
router = APIRouter()
@router.post("/add-bus")#add bus
def add_bus_(request: BusRequest, db: Session = Depends(get_db), current_user: dict = Depends(admin_required)):
    return add_buses(db,request)
@router.delete("/remove-bus/{bus_id}")#remove bus by id
def remove_bus_(bus_id: int, db: Session = Depends(get_db), current_user: dict = Depends(admin_required)):
    return Remove_Bus(db, bus_id)
@router.get("/buses")#get all buses
def get_all_buses_(db: Session = Depends(get_db)):
    return get_all_buses(db)
@router.get("/search")
# def search_bus_(source: str, destination: str, travel_date : str ,db: Session = Depends(get_db)):
def search_bus_(
    source: str = Query(..., description="Source location"),
    destination: str = Query(..., description="Destination location"),
    travel_date: str = Query(..., description="Travel date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
                    ):
    return search_buses(db,source,destination,travel_date)