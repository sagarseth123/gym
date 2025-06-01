from pydantic import BaseModel, EmailStr, Field # Added Field
from typing import Optional, List
from datetime import datetime, timedelta # Added timedelta for examples

from app.models.physical_data import PhysicalDataBase
from app.models.subscription import SubscriptionBase

# --- Token Schema ---
class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field("bearer", example="bearer")

# --- User Schemas ---
class SubscribedUserDetail(BaseModel):
    # User details
    id: str = Field(..., example="60d5ecf0e7a2e8a0a0f3d8e4")
    email: EmailStr = Field(..., example="user@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")
    address: Optional[str] = Field(None, example="123 Main St, Anytown, USA")

    # Subscription details
    plan_name: str = Field(..., example="Gold Monthly")
    subscription_start_date: datetime = Field(..., example=datetime.utcnow().isoformat())
    subscription_end_date: datetime = Field(..., example=(datetime.utcnow() + timedelta(days=30)).isoformat())
    subscription_is_active: bool = Field(..., example=True)
    training_type_opted: Optional[str] = Field(None, example="Weightlifting")

    # Physical data
    latest_physical_data: Optional[PhysicalDataBase] = Field(None) # Example for PhysicalDataBase itself is in its model definition

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        # Example for the whole SubscribedUserDetail can be defined in the route decorator
        # using this schema, or here if preferred for reusability.
        # schema_extra = {
        #     "example": {
        #         "id": "60d5ecf0e7a2e8a0a0f3d8e4",
        #         "email": "user@example.com",
        #         "full_name": "John Doe",
        #         # ... other fields ...
        #         "latest_physical_data": { # Example of PhysicalDataBase content
        #             "weight_kg": 70.5,
        #             "height_cm": 175.0,
        #             "bmi": 22.9,
        #             "record_date": datetime.utcnow().isoformat()
        #         }
        #     }
        # }
