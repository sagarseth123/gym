from datetime import datetime, timedelta # Added timedelta for examples
from typing import Optional

from pydantic import BaseModel, Field

class SubscriptionBase(BaseModel):
    user_id: str = Field(..., example="60d5ecf0e7a2e8a0a0f3d8e4")
    gym_id: str = Field(..., example="60d5ed08e7a2e8a0a0f3d8e5")
    plan_name: str = Field(..., example="Gold Monthly")
    start_date: datetime = Field(..., example=datetime.utcnow().isoformat())
    end_date: datetime = Field(..., example=(datetime.utcnow() + timedelta(days=30)).isoformat())
    is_active: bool = Field(True, example=True)
    training_type_opted: Optional[str] = Field(None, example="Weightlifting")

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionInDB(SubscriptionBase):
    id: str = Field(..., alias="_id", example="60d5ee94e7a2e8a0a0f3d8e6")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Note: start_date and end_date examples in SubscriptionBase are already isoformat strings
    # but in DB they are datetime objects. Pydantic handles conversion.

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True # To allow datetime objects from DB
        json_encoders = {
            datetime: lambda dt: dt.isoformat() # Ensures datetime is serialized to ISO string
        }
