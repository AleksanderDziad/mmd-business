#!/bin/bash

echo "🧹 Czyszczenie starych kontenerów..."
docker system prune -af

echo "🗑 Usunięcie nieużywanych wolumenów..."
docker volume prune -f

echo "✅ Czyszczenie zakończone!"

