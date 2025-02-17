#!/bin/bash

echo "🚀 Automatyczne uruchamianie wszystkiego..."

# Uruchamianie deploy.sh i sprawdzenie błędów
./deploy.sh || { echo "❌ Błąd w deploy.sh!"; exit 1; }

# Uruchamiamy logi w tle
./logs.sh > ~/mmd-business/logs/logs.log 2>&1 &

# Uruchamiamy auto-restart w tle
nohup ./auto-restart.sh > ~/mmd-business/logs/auto-restart.log 2>&1 &

echo "✅ Wszystkie procesy działają!"

