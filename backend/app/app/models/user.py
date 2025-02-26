from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}  # ✅ Umożliwia zmianę tabeli, jeśli już istnieje

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)  # Konto aktywne/nieaktywne
    role = Column(String, default="user")  # Rola użytkownika (user/admin)
    created_at = Column(DateTime, default=datetime.utcnow)  # Data rejestracji
    phone_number = Column(String, nullable=True)  # ✅ Nowa kolumna dla numeru telefonu
