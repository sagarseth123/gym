from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class PhysicalDataBase(BaseModel):
    weight_kg: Optional[float] = Field(None, example=70.5)
    height_cm: Optional[float] = Field(None, example=175.0)
    bmi: Optional[float] = Field(None, example=22.9, description="Body Mass Index, can be calculated from weight and height")
    record_date: datetime = Field(..., example=datetime.utcnow().isoformat())

    class Config:
        # This Config is useful if this model is returned directly by an endpoint
        # or used in ORM mode, even if embedded.
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class PhysicalDataInDB(PhysicalDataBase):
    # If this were to be a standalone collection, it would need an ID:
    # id: str = Field(..., alias="_id", example="60d5ef...")
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime = Field(default_factory=datetime.utcnow)
    # For now, as it's used as embedded, these are not strictly necessary here.
    pass

# If PhysicalData is always embedded within User.physical_data_history,
# PhysicalDataBase is the primary model used for those embedded documents.
# PhysicalDataInDB is kept for potential future use as a separate collection.
