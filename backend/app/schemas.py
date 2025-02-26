from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr  # Wymusza poprawny format e-maila
    password: str

