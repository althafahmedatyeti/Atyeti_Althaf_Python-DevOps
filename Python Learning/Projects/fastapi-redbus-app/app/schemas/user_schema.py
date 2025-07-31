from pydantic import BaseModel
class UserCreate(BaseModel):
    user_id: int
    name: str
    email: str
    password: str
class UserLogin(BaseModel):
    email: str
    password: str
class ShowUser(BaseModel):
    id: int
    name: str
    email: str
   