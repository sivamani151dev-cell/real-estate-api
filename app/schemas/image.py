from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImageCreate(BaseModel):
    image_url: str
    is_primary: Optional[bool] = True
    property_id: int

class ImageResponse(BaseModel):
    id: int
    image_url: str
    is_primary: bool
    created_at: datetime
    property_id: int

    class Config:
        from_attributes=True