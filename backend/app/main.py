from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()

# Model użytkownika
class User(BaseModel):
    username: str
    password: str

# Tymczasowa baza danych (lista użytkowników)
users_db = []

@router.post("/register")
def register(user: User):
    for existing_user in users_db:
        if existing_user["username"] == user.username:
            raise HTTPException(status_code=400, detail="User already exists")
    
    users_db.append({"username": user.username, "password": user.password})
    return {"message": "User registered successfully"}

@router.get("/")
def get_users():
    return users_db

app.include_router(router)
