#!/bin/bash

echo "🔄 Restartowanie aplikacji..."
docker-compose down
docker-compose up -d --build
echo "✅ Aplikacja uruchomiona!"

