import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Pobranie danych połączeniowych z zmiennych środowiskowych (dla Dockera)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@postgres_mmd:5432/mydatabase")

# Debugowanie adresu bazy danych
print(f"🟢 DATABASE_URL: {DATABASE_URL}")

# Tworzenie silnika bazy danych
engine = create_engine(DATABASE_URL)

# Tworzenie sesji dla SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Deklaracja bazy
Base = declarative_base()

# Funkcja do pobierania sesji bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

