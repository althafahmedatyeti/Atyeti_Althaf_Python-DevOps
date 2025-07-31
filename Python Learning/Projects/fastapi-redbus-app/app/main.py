from fastapi import FastAPI
from database import engine, Base
from models.booking import Bookings
from models.bus import Bus
from models.user import User
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi

from api.v1 import booking_routes, user_routes, bus_routes

bearer_scheme = HTTPBearer()
# This ensures SQLAlchemy knows all models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="REDBUS")

app.include_router(booking_routes.router, prefix="/booking", tags=["Booking"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(bus_routes.router, prefix="/bus", tags=["Bus"])
# Custom OpenAPI schema with global security
def custom_openapi():
    if app.openapi_schema:
      return app.openapi_schema
    
    openapi_schema = get_openapi(#generate default schema
    title="RedBus Booking API",
    version="1.0.0",
    description="API for booking system",
    routes=app.routes,
    )
    #Inject security scheme into the schema
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    #Apply security globally to all routes
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema
# Attach custom OpenAPI to app
app.openapi = custom_openapi