from sqlalchemy import Column, Integer, Float, Enum, Boolean, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class PropertyType(enum.Enum):
    sale = "sale"
    rent = "rent"

class PropertyCategory(enum.Enum):
    apartment = "apartment"
    house = "house"
    commercial = "commercial"
    land = "land"

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    property_type = Column(Enum(PropertyType), default=PropertyType.sale)
    property_category = Column(Enum(PropertyCategory), default=PropertyCategory.apartment)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    area_sqft = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    city = Column(String)
    state = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    images = relationship("Image", backref="property")
    favorites = relationship("Favorite", backref="saved_by_users")
    inquiries = relationship("Inquiry", backref="property")