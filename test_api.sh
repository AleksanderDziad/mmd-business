#!/bin/bash

echo "🚀 Testowanie API..."

echo "🔍 Sprawdzanie endpointu głównego..."
curl -s http://localhost:8000/ | jq .

echo "🔍 Sprawdzanie rejestracji użytkownika..."
curl -s -X POST http://localhost:8000/register -H "Content-Type: application/json" -d '{"username":"test","password":"1234"}' | jq .

echo "✅ Testy zakończone!"

