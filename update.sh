#!/bin/bash

echo "🔄 Pobieranie najnowszych zmian z repozytorium..."
git pull origin main

echo "🚀 Restartowanie aplikacji po aktualizacji..."
./restart.sh

