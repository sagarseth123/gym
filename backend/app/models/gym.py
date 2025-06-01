from pydantic import BaseModel, Field
from typing import Optional, List

class Equipment(BaseModel):
    name: str
    quantity: int

class Trainer(BaseModel):
    name: str
    specialization: str
    fee: float

class SubscriptionPlan(BaseModel):
    name: str
    duration_days: int
    price: float
    features: List[str]

class TrainingType(BaseModel):
    name: str
    description: Optional[str] = None

class GymBase(BaseModel):
    name: str
    owner_id: str # Refers to User's ID (Gym Admin)
    area_sq_ft: Optional[float] = None
    address: Optional[str] = None
    equipments: List[Equipment] = []
    personal_trainers: List[Trainer] = []
    subscription_plans: List[SubscriptionPlan] = []
    training_types_offered: List[TrainingType] = []
    is_verified: bool = False # Admins might need to verify new gyms

class GymCreate(GymBase):
    pass

class GymInDB(GymBase):
    id: str = Field(..., alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            # ObjectId: str
        }

class GymPublic(GymBase): # What's safe to return
    id: str
    name: str
    area_sq_ft: Optional[float] = None
    address: Optional[str] = None
    equipments: List[Equipment] = []
    personal_trainers: List[Trainer] = []
    subscription_plans: List[SubscriptionPlan] = []
    training_types_offered: List[TrainingType] = []
    is_verified: bool = False
