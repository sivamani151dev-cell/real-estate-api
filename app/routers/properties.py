from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.property import Property, PropertyType, PropertyCategory
from app.models.user import User
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/properties", tags=["Properties"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token) 
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=PropertyResponse, status_code=201)
def create_property(property: PropertyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_property = Property(
        title=property.title,
        description=property.description,
        price = property.price,
        property_type=property.property_type,
        property_category=property.property_category,
        bedrooms=property.bedrooms,
        bathrooms=property.bathrooms,
        area_sqft=property.area_sqft,
        location=property.location,
        city=property.city,
        state=property.state,
        owner_id=current_user.id
    )
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    logger.info(f"Property created by {current_user.username}: {property.title}")
    return new_property

@router.get("/", response_model=list[PropertyResponse])
def get_properties(
    city: Optional[str] = None,
    property_type: Optional[PropertyType] = None,
    property_category: Optional[PropertyCategory] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_bedrooms: Optional[int] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Property).filter(Property.is_active == True)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if property_category:
        query = query.filter(Property.property_category == property_category)
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    if min_bedrooms:
        query = query.filter(Property.bedrooms >= min_bedrooms)
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

@router.get("/my", response_model=list[PropertyResponse])
def get_my_properties(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Property).filter(Property.owner_id == current_user.id).all()

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.put("/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, update: PropertyUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    property = db.query(Property).filter(Property.id == property_id, Property.owner_id == current_user.id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if update.title is not None:
        property.title = update.title
    if update.description is not None:
        property.description = update.description
    if update.min_price is not None:
        property.min_price = update.min_price
    if update.max_price is not None:
        property.max_price = update.max_price
    if update.bedrooms is not None:
        property.bedrooms = update.bedrooms
    if update.bathrooms is not None:
        property.bathrooms = update.bathrooms
    if update.area_sqft is not None:
        property.area_sqft = update.area_sqft
    if update.location is not None:
        property.location = update.location
    if update.city is not None:
        property.city = update.city
    if update.state is not None:
        property.state = update.state
    if update.is_active is not None:
        property.is_active = update.is_active
    db.commit()
    db.refresh(property)
    return property

@router.delete("/{property_id}", status_code=204)
def delete_property(property_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    property = db.query(Property).filter(Property.id == property_id, Property.owner_id == current_user.id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(property)
    db.commit()
    return None