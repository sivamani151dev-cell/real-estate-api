from sqlalchemy import Column, Integer, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class InquiryStatus(enum.Enum):
    pending = "pending"
    responded = "responded"
    closed = "closed"

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=True)
    status = Column(Enum(InquiryStatus), default=InquiryStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    property_id = Column(Integer, ForeignKey("properties.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", backref="inquiries")