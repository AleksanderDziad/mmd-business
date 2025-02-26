import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 🔹 Poprawienie ścieżki do aplikacji
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

# Pobranie konfiguracji Alembic
config = context.config

# Pobranie URL bazy danych z alembic.ini lub zmiennej środowiskowej
DATABASE_URL = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

# 🔹 Importowanie `Base` oraz modeli, aby Alembic je wykrył
try:
    from app.database import Base  # Import klasy bazowej SQLAlchemy
    from app.models import user, product  # Importowanie wszystkich modeli
except ModuleNotFoundError as e:
    print(f"❌ Błąd importu: {e}. Upewnij się, że katalogi i moduły istnieją!")
    sys.exit(1)

# 🔹 Przypisanie metadanych modeli do migracji
target_metadata = Base.metadata

# 🔴 Tryb offline (bez połączenia z bazą danych)
def run_migrations_offline() -> None:
    """Uruchom migracje w trybie offline."""
    try:
        context.configure(
            url=DATABASE_URL,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()
    except Exception as e:
        print(f"❌ Błąd migracji offline: {e}")
        sys.exit(1)

# 🟢 Tryb online (z połączeniem do bazy danych)
def run_migrations_online() -> None:
    """Uruchom migracje w trybie online."""
    try:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                render_as_batch=True if "sqlite" in DATABASE_URL else False,
            )

            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        print(f"❌ Błąd połączenia z bazą danych: {e}")
        sys.exit(1)

# 🔹 Wybór trybu migracji (offline/online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

