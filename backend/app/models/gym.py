from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Equipment(BaseModel):
    name: str = Field(..., example="Treadmill")
    quantity: int = Field(..., example=10)

class Trainer(BaseModel):
    name: str = Field(..., example="Mike Fit")
    specialization: str = Field(..., example="Weightlifting")
    fee: float = Field(..., example=50.0, description="Fee per session")

class SubscriptionPlan(BaseModel):
    name: str = Field(..., example="Gold Monthly")
    duration_days: int = Field(..., example=30)
    price: float = Field(..., example=100.0)
    features: List[str] = Field(default_factory=list, example=["All classes", "Sauna access"])

class TrainingType(BaseModel):
    name: str = Field(..., example="Yoga")
    description: Optional[str] = Field(None, example="Yoga for flexibility and strength")

class GymBase(BaseModel):
    name: str = Field(..., example="Fitness Hub")
    owner_id: str = Field(..., example="60d5ecf0e7a2e8a0a0f3d8e4", description="ID of the admin user who owns the gym")
    area_sq_ft: Optional[float] = Field(None, example=1000.50)
    address: Optional[str] = Field(None, example="456 Fitness Ave, Gymtown, USA")
    equipments: List[Equipment] = Field(default_factory=list)
    personal_trainers: List[Trainer] = Field(default_factory=list)
    subscription_plans: List[SubscriptionPlan] = Field(default_factory=list)
    training_types_offered: List[TrainingType] = Field(default_factory=list)
    is_verified: bool = Field(False, example=False, description="Whether the gym has been verified by platform admins")

class GymCreate(GymBase):
    # owner_id will be set by the system based on the logged-in admin
    pass

class GymUpdate(BaseModel): # For partial updates by gym owner
    name: Optional[str] = Field(None, example="Fitness Hub Deluxe")
    area_sq_ft: Optional[float] = Field(None, example=1200.75)
    address: Optional[str] = Field(None, example="789 Wellness Blvd, Gymtown, USA")
    equipments: Optional[List[Equipment]] = Field(None)
    personal_trainers: Optional[List[Trainer]] = Field(None)
    subscription_plans: Optional[List[SubscriptionPlan]] = Field(None)
    training_types_offered: Optional[List[TrainingType]] = Field(None)
    is_verified: Optional[bool] = Field(None, example=True) # Platform admin might verify

class GymInDB(GymBase):
    id: str = Field(..., alias="_id", example="60d5ed08e7a2e8a0a0f3d8e5")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }

class GymPublic(BaseModel): # What's safe to return to general users/public listings
    id: str = Field(..., example="60d5ed08e7a2e8a0a0f3d8e5")
    name: str = Field(..., example="Fitness Hub")
    # owner_id is typically not public
    area_sq_ft: Optional[float] = Field(None, example=1000.50)
    address: Optional[str] = Field(None, example="456 Fitness Ave, Gymtown, USA")
    equipments: List[Equipment] = Field(default_factory=list)
    personal_trainers: List[Trainer] = Field(default_factory=list) # Maybe only names and specializations, not fees
    subscription_plans: List[SubscriptionPlan] = Field(default_factory=list) # Might simplify for public view
    training_types_offered: List[TrainingType] = Field(default_factory=list)
    is_verified: bool = Field(False, example=False)
