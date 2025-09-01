from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    phone_number: str

class UserCreate(UserBase):
    email: str
    password: str

class UserUpdate(UserBase):
    username: str | None = None
    phone_number: str | None = None

class UserResponse(UserBase):
    id: int
    balance: int
    email: str
    created_at: datetime