from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inquiry import Inquiry, InquiryStatus
from app.models.property import Property
from app.models.user import User
from app.schemas.inquiry import InquiryCreate, InquiryResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/inquiries", tags=["Inquiries"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/{property_id}", response_model=InquiryResponse, status_code=201)
def send_inquiry(property_id: int, inquiry: InquiryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    new_inquiry = Inquiry(
        message=inquiry.message,
        property_id=property_id,
        user_id=current_user.id
    )
    db.add(new_inquiry)
    db.commit()
    db.refresh(new_inquiry)
    return new_inquiry

@router.get("/my", response_model=list[InquiryResponse])
def get_my_inquiries(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Inquiry).filter(Inquiry.user_id == current_user.id).all()

@router.get("/received", response_model=list[InquiryResponse])
def get_received_inquiries(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_properties = db.query(Property).filter(Property.owner_id == current_user.id).all()
    property_ids = [p.id for p in my_properties]
    return db.query(Inquiry).filter(Inquiry.property_id.in_(property_ids)).all()

@router.put("/{inquiry_id}", response_model=InquiryResponse)
def update_inquiry_status(inquiry_id: int, status: InquiryStatus, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    inquiry.status = status
    db.commit()
    db.refresh(inquiry)
    return inquiry