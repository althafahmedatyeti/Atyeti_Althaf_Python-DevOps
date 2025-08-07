from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

from database import engine, Base
from models.booking import Bookings
from models.bus import Bus
from models.user import User

from api import booking_routes, user_routes, bus_routes
from logging_config import setup_logging , logger 

# Global Logging Configuration
setup_logging()


# Initialize App & Model
app = FastAPI(title="REDBUS")
Base.metadata.create_all(bind=engine)  # Creates tables if they don't exist

# Include API Routers
app.include_router(booking_routes.router, prefix="/booking", tags=["Booking"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(bus_routes.router, prefix="/bus", tags=["Bus"])

# JWT Bearer Auth Schema
bearer_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="RedBus Booking API",
        version="1.0.0",
        description="API for booking system",
        routes=app.routes,
    )
    
    # Inject security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security globally to all endpoints
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Attach custom OpenAPI
app.openapi = custom_openapi

logger.info(" RedBus API started successfully!")

