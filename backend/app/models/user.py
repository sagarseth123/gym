from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: Optional[str] = None # For local auth
    google_id: Optional[str] = None # For Google auth
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: str = Field(..., alias="_id") # For MongoDB's _id field

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            # If you have ObjectIds, you might need a custom encoder here
            # ObjectId: str
        }

class UserPublic(BaseModel): # What's safe to return to clients
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool = True
