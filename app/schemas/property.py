from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.property import PropertyCategory, PropertyType

class PropertyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    property_type: PropertyType
    property_category: PropertyCategory
    bedrooms: int
    bathrooms: int
    area_sqft: float
    location: str
    city: str
    state: str

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    is_active: Optional[bool] = None

class PropertyResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    property_type: PropertyType
    property_category: PropertyCategory
    bedrooms: int
    bathrooms: int
    area_sqft: float
    location: str
    city: str
    state: str
    is_active: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True