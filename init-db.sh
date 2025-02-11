#!/bin/bash

echo "🗄️ Migracja bazy danych..."
docker exec -it mmd-business flask db upgrade

echo "📊 Optymalizacja bazy danych..."
docker exec -it mmd-db psql -U mmduser -d mmd_business -c "VACUUM ANALYZE;"

echo "✅ Baza danych gotowa!"

