from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.product import Product
from core.security import get_current_admin

router = APIRouter()

# Dodawanie nowego produktu (tylko admin)
@router.post("/")
def create_product(name: str, description: str, price: float, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    new_product = Product(name=name, description=description, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Produkt dodany", "product": new_product}

