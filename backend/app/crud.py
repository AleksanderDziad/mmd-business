from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    """Tworzy nowego użytkownika"""
    db_user = User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    """Zwraca listę użytkowników"""
    return db.query(User).offset(skip).limit(limit).all()

