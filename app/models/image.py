from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.sql import func

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, unique=True, nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    property_id = Column(Integer, ForeignKey("properties.id"))