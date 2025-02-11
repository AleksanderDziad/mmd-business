#!/bin/bash

echo "🔥 Aktualizacja obrazu Docker..."
docker pull alex12323/mmd-business:latest

echo "🛑 Zatrzymanie starego kontenera..."
docker stop mmd-business || true
docker rm mmd-business || true

echo "🚀 Uruchomienie nowego kontenera..."
docker run -d --name mmd-business -p 80:5000 alex12323/mmd-business:latest
