#!/bin/bash

echo "🔍 Sprawdzanie dostępności usług..."

# Sprawdzenie Backend
if curl -s http://localhost:8000/ > /dev/null; then
  echo "✅ Backend działa!"
else
  echo "❌ Backend nie odpowiada!"
fi

# Sprawdzenie Frontend
if curl -s http://localhost:3000/ > /dev/null; then
  echo "✅ Frontend działa!"
else
  echo "❌ Frontend nie odpowiada!"
fi

