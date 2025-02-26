from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, products  # ✅ Poprawiony import z prefiksem `app.`
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import uvicorn  # ✅ Import Uvicorn do poprawnego uruchamiania aplikacji
from sqlalchemy.exc import SQLAlchemyError
import debugpy  # ✅ Dodanie obsługi debuggera

# 🔹 Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Debugger (jeśli aktywowany)
debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
if debug_mode:
    logger.info("🟢 Debugger nasłuchuje na porcie 5678...")
    debugpy.listen(("0.0.0.0", 5678))
    debugpy.wait_for_client()

# 🔹 Inicjalizacja aplikacji FastAPI
app = FastAPI(title="MMD-Business API", version="1.0")

# 🔹 Pobranie listy dozwolonych domen z `.env`
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
origins = cors_origins_env.split(",") if cors_origins_env else ["*"]

# 🔹 Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista domen lub "*" dla wszystkich
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Tworzenie tabel w bazie danych (jeśli nie używasz Alembic)
try:
    logger.info("🛠️ Tworzenie tabel w bazie danych...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tabele zostały utworzone!")
except SQLAlchemyError as e:
    logger.error(f"❌ Błąd SQLAlchemy podczas tworzenia tabel: {e}")
except Exception as e:
    logger.error(f"❌ Nieznany błąd podczas tworzenia tabel: {e}")

# 🔹 Rejestracja routerów API
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])

@app.get("/", summary="Strona główna API", response_model=dict)
def read_root():
    """Strona główna API"""
    return {"message": "API MMD-Business działa poprawnie!"}

@app.get("/health", summary="Sprawdzenie statusu API", response_model=dict)
def health_check():
    """Endpoint do sprawdzania statusu API"""
    return {"status": "ok"}

# 🔹 Uruchamianie aplikacji FastAPI w kontenerze Docker
if __name__ == "__main__":
    logger.info("🚀 Aplikacja MMD-Business API uruchomiona!")
    uvicorn.run("app.app.main:app", host="0.0.0.0", port=8000, reload=False, workers=1)

