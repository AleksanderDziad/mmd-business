#!/bin/bash

echo "🚀 Uruchamianie automatycznego restartowania usług..."

while true; do
  # Sprawdzenie, czy backend działa
  if ! docker ps | grep -q "backend"; then
    echo "⚠️  Backend padł! Restartuję..."
    docker-compose restart backend
  fi

  # Sprawdzenie, czy frontend działa
  if ! docker ps | grep -q "frontend"; then
    echo "⚠️  Frontend padł! Restartuję..."
    docker-compose restart frontend
  fi

  sleep 10  # Sprawdzamy co 10 sekund
done

