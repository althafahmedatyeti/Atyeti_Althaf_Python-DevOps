from pydantic import BaseModel
class AdminRequest(BaseModel):

    email:str
    password:str