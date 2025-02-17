#!/bin/bash

set -e  # Zatrzymaj skrypt, jeśli wystąpi błąd

echo "🚀 [DEPLOY] Rozpoczynam wdrożenie MMD-Business..."

# 1️⃣ Aktualizacja obrazu Docker
echo "🔥 Pobieranie najnowszego obrazu Docker..."
docker pull alex12323/mmd-business:latest

# 2️⃣ Backup bazy danych przed restartem
echo "📦 Tworzenie kopii zapasowej bazy danych..."
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="db_backups"
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR
docker exec db pg_dump -U db_user -d db_name > $BACKUP_FILE
echo "✅ Backup zapisany jako: $BACKUP_FILE"

# 3️⃣ Zatrzymanie i usunięcie starego kontenera
echo "🛑 Zatrzymywanie i usuwanie starego kontenera..."
docker stop mmd-business || true
docker rm mmd-business || true

# 4️⃣ Zatrzymanie starych kontenerów (docker-compose)
echo "📌 Zatrzymywanie i usuwanie starych kontenerów..."
docker-compose down -v

# 5️⃣ Budowanie i uruchamianie nowych kontenerów
echo "🔄 Budowanie i uruchamianie kontenerów..."
docker-compose up -d --build

# 6️⃣ Czekanie na uruchomienie backendu
echo "🕒 Czekanie 5 sekund na stabilizację backendu..."
sleep 5

# 7️⃣ Sprawdzanie statusu kontenerów
echo "🛠 Sprawdzanie statusu kontenerów..."
docker ps

# 8️⃣ Testowanie API po wdrożeniu
echo "🧪 Testowanie endpointów API..."
RESPONSE=$(curl -s http://localhost:8000/)
if [[ "$RESPONSE" == *"Hello, World!"* ]]; then
  echo "✅ API działa poprawnie!"
else
  echo "❌ Błąd: API nie zwróciło oczekiwanej odpowiedzi!"
  exit 1
fi

# 9️⃣ Uruchomienie nowego kontenera z obrazem
echo "🚀 Uruchomienie nowego kontenera..."
docker run -d --name mmd-business -p 80:5000 alex12323/mmd-business:latest

# 🔟 Informacja o sukcesie
echo "✅ Aplikacja została wdrożona pomyślnie!"
echo "   🔗 Frontend: http://localhost:3000"
echo "   🔗 Backend: http://localhost:8000/docs"

echo "🎯 Wdrożenie zakończone sukcesem!"

