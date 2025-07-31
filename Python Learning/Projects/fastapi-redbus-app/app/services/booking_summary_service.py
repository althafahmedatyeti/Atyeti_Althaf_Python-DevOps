from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.booking import Bookings
from models.bus import Bus
from models.booked_bus_summary import BusBookingSummary
import logging

logger = logging.getLogger(__name__)


def create_summary(db: Session, bus_id: int, travel_date: str):
    """
    Creates or updates the summary of bookings for a given bus and travel date.
    """

    logger.info(f"Creating booking summary for bus_id={bus_id}, travel_date={travel_date}")

    try:
        travel_date_obj = datetime.strptime(travel_date, "%Y-%m-%d").date()
    except ValueError:
        logger.warning(f"Invalid date format received: {travel_date}")
        return {"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}

    try:
        bus = db.query(Bus).filter(Bus.bus_id == bus_id).first()
        if not bus:
            logger.error(f"Bus with id={bus_id} not found.")
            return {"success": False, "message": "Bus not found."}

        booked_count = db.query(func.count(Bookings.booking_id)).filter(
            Bookings.bus_id == bus_id,
            Bookings.travel_date == travel_date_obj
        ).scalar()

        available_seats = 40 - booked_count
        logger.info(f"Bus {bus_id} on {travel_date_obj}: {booked_count} booked, {available_seats} available.")

        summary = db.query(BusBookingSummary).filter_by(
            bus_id=bus_id,
            travel_date=travel_date_obj
        ).first()

        if summary:
            logger.info(f"Updating existing summary for bus {bus_id} on {travel_date_obj}.")
            summary.booked_seats = booked_count
            summary.available_seats = available_seats
        else:
            logger.info(f"Creating new summary for bus {bus_id} on {travel_date_obj}.")
            summary = BusBookingSummary(
                bus_id=bus_id,
                source=bus.bus_source,
                destination=bus.bus_destination,
                travel_date=travel_date_obj,
                booked_seats=booked_count,
                available_seats=available_seats,
            )
            db.add(summary)

        db.commit()
        db.refresh(summary)
        logger.info(f"Summary committed successfully for bus {bus_id}.")

        return {
            "success": True,
            "message": "Summary created/updated successfully.",
            "summary": {
                "bus_id": summary.bus_id,
                "travel_date": str(summary.travel_date),
                "booked_seats": summary.booked_seats,
                "available_seats": summary.available_seats,
                "source": summary.source,
                "destination": summary.destination
            }
        }

    except Exception as e:
        db.rollback()
        logger.exception("Error while creating/updating summary")
        return {"success": False, "message": f"Internal error: {str(e)}"}
