import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from database import SessionLocal, engine, Base
from app.models import User

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

client = TestClient(app)

# Reset bazy przed testami
def setup_module(module):
    """Resetuje bazę przed testami"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Opcjonalnie, usuń dane, jeśli baza nie obsługuje `drop_all()`
    db: Session = SessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()

def test_create_user():
    """Test poprawnego tworzenia użytkownika"""
    email = "unique@example.com"
    response = client.post("/users/", json={"email": email, "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email

def test_duplicate_email():
    """Test sprawdzający błąd przy dodawaniu tego samego e-maila"""
    email = "duplicate@example.com"
    client.post("/users/", json={"email": email, "password": "testpass"})
    response = client.post("/users/", json={"email": email, "password": "testpass"})
    assert response.status_code == 400  # Spodziewamy się błędu
    assert response.json()["detail"] == "Email already registered"

