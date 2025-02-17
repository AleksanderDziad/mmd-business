#!/bin/bash

echo "⚠️  Resetowanie bazy danych..."

# Zatrzymujemy kontener DB
docker-compose stop db

# Usuwamy stare dane
docker volume rm mmd-business_db_data

# Restartujemy bazę
docker-compose up -d db

echo "✅ Baza danych została zresetowana!"

