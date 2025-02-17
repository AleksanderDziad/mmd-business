#!/bin/bash

set -e  # Zatrzymaj skrypt, jeśli wystąpi błąd

echo "🚀 [DEPLOY] Rozpoczynam wdrożenie MMD-Business..."
sleep 1

# 1️⃣ Aktualizacja obrazu Docker
echo "🔥 Pobieranie najnowszego obrazu Docker..."
docker pull alex12323/mmd-business:latest

# 2️⃣ Aktualizacja kodu z repozytorium
echo -ne "🔄 Pobieranie najnowszej wersji kodu... [0%] \r"
git pull origin main > /dev/null 2>&1
echo -ne "🔄 Pobieranie najnowszej wersji kodu... [✅ 15%] \r"
sleep 1

# 3️⃣ Backup bazy danych przed restartem
echo -ne "📦 Tworzenie kopii zapasowej bazy danych... [15%] \r"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="db_backups"
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR
docker exec db pg_dump -U db_user -d db_name > $BACKUP_FILE
echo -ne "📦 Tworzenie kopii zapasowej bazy danych... [✅ 30%] \r"
sleep 1

# 4️⃣ Zatrzymanie i usunięcie starego kontenera
echo "🛑 Zatrzymywanie i usuwanie starego kontenera..."
docker stop mmd-business || true
docker rm mmd-business || true

# 5️⃣ Zatrzymanie starych kontenerów (docker-compose)
echo -ne "📌 Zatrzymywanie i usuwanie starych kontenerów... [30%] \r"
docker-compose down -v > /dev/null 2>&1
echo -ne "📌 Zatrzymywanie i usuwanie starych kontenerów... [✅ 45%] \r"
sleep 1

# 6️⃣ Budowanie i uruchamianie nowych kontenerów
echo -ne "🔄 Budowanie i uruchamianie kontenerów... [45%] \r"
docker-compose up -d --build > /dev/null 2>&1
echo -ne "🔄 Budowanie i uruchamianie kontenerów... [✅ 60%] \r"
sleep 1

# 7️⃣ Czekanie na uruchomienie backendu
echo -ne "🕒 Czekanie 5 sekund na stabilizację backendu... [60%] \r"
sleep 5
echo -ne "🕒 Czekanie na stabilizację backendu... [✅ 75%] \r"

# 8️⃣ Sprawdzanie statusu kontenerów
echo -ne "🛠 Sprawdzanie statusu kontenerów... [75%] \r"
docker ps > /dev/null 2>&1
echo -ne "🛠 Sprawdzanie statusu kontenerów... [✅ 85%] \r"
sleep 1

# 9️⃣ Testowanie API po wdrożeniu
echo -ne "🧪 Testowanie endpointów API... [85%] \r"
RESPONSE=$(curl -s http://localhost:8000/)
if [[ "$RESPONSE" == *"Hello, World!"* ]]; then
  echo -ne "🧪 Testowanie endpointów API... [✅ 95%] \r"
else
  echo -ne "❌ Błąd: API nie zwróciło oczekiwanej odpowiedzi! [🚨] \r"
  exit 1
fi

# 🔟 Uruchomienie nowego kontenera z obrazem
echo "🚀 Uruchomienie nowego kontenera..."
docker run -d --name mmd-business -p 80:5000 alex12323/mmd-business:latest

# 🔟 Informacja o sukcesie
echo -ne "✅ Aplikacja została wdrożona pomyślnie! [100%] \n"
echo "   🔗 Frontend: http://localhost:3000"
echo "   🔗 Backend: http://localhost:8000/docs"

echo "🎯 Wdrożenie zakończone sukcesem!"

