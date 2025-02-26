import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 🔹 Poprawienie ścieżki do aplikacji
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, "/app")  # <-- Dodatkowo upewnij się, że `/app` jest widoczne

# 🔹 Importowanie `Base` oraz modeli, aby Alembic je wykrył
from database import Base  # <-- Usunięcie `app.` z importu
import models  # <-- Importowanie modeli bez `app.`

# Pobranie konfiguracji Alembic
config = context.config

# Pobranie URL bazy danych z alembic.ini
DATABASE_URL = config.get_main_option("sqlalchemy.url")

# 🔹 Przypisanie metadanych modeli do migracji
target_metadata = Base.metadata  # <-- Kluczowa linia!

# 🔴 Tryb offline (bez połączenia z bazą danych)
def run_migrations_offline() -> None:
    """Uruchom migracje w trybie offline."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# 🟢 Tryb online (z połączeniem do bazy danych)
def run_migrations_online() -> None:
    """Uruchom migracje w trybie online."""
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

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
