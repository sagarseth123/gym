from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime # For example in PhysicalData
from .physical_data import PhysicalDataBase as PhysicalData

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")
    # hashed_password should not have an example for security reasons
    hashed_password: Optional[str] = None
    google_id: Optional[str] = Field(None, example="google_oauth_id_12345")
    role: UserRole = Field(..., example=UserRole.user)
    is_active: bool = Field(True, example=True)
    address: Optional[str] = Field(None, example="123 Main St, Anytown, USA")
    physical_data_history: List[PhysicalData] = Field(default_factory=list, example=[]) # Example for list can be tricky if PhysicalData is complex

class UserCreate(UserBase):
    # For creation, password is required (but will be hashed)
    # Role might be set by system depending on route (e.g. admin signup vs user signup)
    hashed_password: str = Field(..., example="strongpassword123") # Example is for input, will be hashed

class UserUpdate(BaseModel): # For updating user profile
    full_name: Optional[str] = Field(None, example="Johnathan Doe")
    address: Optional[str] = Field(None, example="456 New Ave, Anytown, USA")
    is_active: Optional[bool] = Field(None, example=False) # Admin might change this
    # Role changes should be handled by specific admin endpoints, not general update
    # physical_data_history updates would likely be through dedicated endpoints

class UserInDB(UserBase):
    id: str = Field(..., alias="_id", example="60d5ecf0e7a2e8a0a0f3d8e4")
    # Potentially add created_at, updated_at if tracked in DB model
    created_at: datetime = Field(default_factory=datetime.utcnow, example=datetime.utcnow().isoformat())
    updated_at: datetime = Field(default_factory=datetime.utcnow, example=datetime.utcnow().isoformat())


    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            # ObjectId: str # Already handled by str alias in Pydantic
        }

class UserPublic(BaseModel): # What's safe to return to clients
    id: str = Field(..., example="60d5ecf0e7a2e8a0a0f3d8e4")
    email: EmailStr = Field(..., example="user@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")
    address: Optional[str] = Field(None, example="123 Main St, Anytown, USA")
    role: UserRole = Field(..., example=UserRole.user)
    is_active: bool = Field(True, example=True)
