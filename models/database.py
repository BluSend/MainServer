from pydantic import BaseModel


class User(BaseModel):
    name: str
    roomNumber: str
    email: str

class UserStrict(BaseModel):
    name: str
    roomNumber: str
    userID: int
    email: str

class IDOnly(BaseModel):
    id: int

class Parcel(BaseModel):
    userID: int | None = None
    status: str | None = None
    tracking_id: int
    nDelivery: int | None = None
