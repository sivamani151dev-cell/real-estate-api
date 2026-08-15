from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.favorite import Favorite
from app.models.property import Property
from app.models.user import User
from app.schemas.favorite import FavoriteResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/favorites", tags=["Favorites"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/{property_id}", response_model=FavoriteResponse, status_code=201)
def add_favorite(property_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.property_id == property_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")
    new_favorite = Favorite(user_id=current_user.id, property_id=property_id)
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    return new_favorite

@router.get("/", response_model=list[FavoriteResponse])
def get_favorites(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Favorite).filter(Favorite.user_id == current_user.id).all()

@router.delete("/{property_id}", status_code=204)
def remove_favorite(property_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.property_id == property_id
    ).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Not in favorites")
    db.delete(favorite)
    db.commit()
    return None