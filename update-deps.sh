#!/bin/bash

echo "📦 Aktualizacja zależności backendu..."
docker exec backend pip install --upgrade -r /app/requirements.txt

echo "📦 Aktualizacja zależności frontend..."
docker exec frontend npm update

echo "✅ Aktualizacja zależności zakończona!"

