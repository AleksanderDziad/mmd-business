#!/bin/bash

echo "📦 Aktualizacja kodu..."
git pull origin main

echo "🚀 Budowanie i wdrażanie kontenerów..."
docker-compose down
docker-compose up -d --build

echo "🛠️ Migracja bazy danych..."
docker exec -it mmd-business flask db upgrade

echo "📊 Optymalizacja bazy danych..."
docker exec -it mmd-db psql -U mmduser -d mmd_business -c "VACUUM ANALYZE;"

echo "📂 Wdrażanie modułów funkcjonalności..."

MODULES=("crm" "analytics" "seo" "inventory" "marketing")

for MODULE in "${MODULES[@]}"; do
    echo "🔧 Wdrażanie modułu: $MODULE..."
    docker exec -it mmd-business flask db migrate -m "Dodanie modułu $MODULE"
    docker exec -it mmd-business flask db upgrade
done

echo "✅ Wszystkie moduły zostały wdrożone!"

