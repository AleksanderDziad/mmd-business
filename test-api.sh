#!/bin/bash

echo "🧪 Testowanie backendu..."
RESPONSE=$(curl -s http://localhost:8000/)

if [[ "$RESPONSE" == *"Hello, World!"* ]]; then
  echo "✅ API działa poprawnie!"
else
  echo "❌ Błąd: API nie działa!"
  exit 1
fi

