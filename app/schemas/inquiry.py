from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.inquiry import InquiryStatus

class InquiryCreate(BaseModel):
    message: Optional[str] = None
    property_id: int

class InquiryResponse(BaseModel):
    id: int
    message: Optional[str] = None
    status: InquiryStatus
    created_at : datetime
    property_id: int
    user_id: int

    class Config:
        from_attributes=True