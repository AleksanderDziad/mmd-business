from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from app.models.user import User
from core.security import (
    hash_password, verify_password, create_access_token,
    create_refresh_token, get_current_user, get_current_admin
)

router = APIRouter()

# Rejestracja użytkownika
@router.post("/register")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Użytkownik już istnieje")

    new_user = User(email=email, hashed_password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Użytkownik zarejestrowany"}

# Logowanie użytkownika
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane logowania")

    access_token = create_access_token({"sub": user.email, "role": user.role}, timedelta(minutes=30))
    refresh_token = create_refresh_token({"sub": user.email, "role": user.role}, timedelta(days=7))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Odświeżanie tokena
@router.post("/refresh")
def refresh_token(current_user: dict = Depends(get_current_user)):
    new_access_token = create_access_token({"sub": current_user["email"], "role": current_user["role"]}, timedelta(minutes=30))
    return {"access_token": new_access_token, "token_type": "bearer"}

# Wylogowanie użytkownika
@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")  # Usunięcie access tokena
    response.delete_cookie("refresh_token")  # Usunięcie refresh tokena
    return {"message": "Wylogowano pomyślnie"}

# Endpoint chroniony (dla zalogowanych użytkowników)
@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "Dostęp przyznany!", "user": current_user}

# Endpoint dla administratora
@router.get("/admin")
def admin_only(current_admin: dict = Depends(get_current_admin)):
    return {"message": "Witaj, adminie!", "user": current_admin}

# Zmiana roli użytkownika (dostępne tylko dla adminów)
@router.patch("/role")
def change_user_role(email: str, new_role: str, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")   
    
    if new_role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Nieprawidłowa rola")
        
    user.role = new_role
    db.commit()
    db.refresh(user)

    return {"message": f"Rola użytkownika {email} zmieniona na {new_role}"}

# Dezaktywacja użytkownika (dostępne tylko dla adminów)
@router.patch("/deactivate")
def deactivate_user(email: str, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")

    user.is_active = False
    db.commit()
    db.refresh(user)

    return {"message": f"Konto użytkownika {email} zostało dezaktywowane"}

# Aktywacja użytkownika (dostępne tylko dla adminów)
@router.patch("/activate")
def activate_user(email: str, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")

    user.is_active = True
    db.commit()
    db.refresh(user)

    return {"message": f"Konto użytkownika {email} zostało aktywowane"}

# Usuwanie użytkownika (dostępne tylko dla adminów)
@router.delete("/delete")
def delete_user(email: str, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")

    db.delete(user)
    db.commit()

    return {"message": f"Konto użytkownika {email} zostało usunięte"}

