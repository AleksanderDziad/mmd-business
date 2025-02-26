from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from app.crud.user import create_user, get_users
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

# Funkcja dependency dla bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Tworzy nowego użytkownika w bazie danych.
    """
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@router.get("/users/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """
    Pobiera listę wszystkich użytkowników.
    """
    users = get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

