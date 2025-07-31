from pydantic import BaseModel
class BusRequest(BaseModel):
    bus_id:int
    bus_source:str
    bus_destination : str
    bus_name :str