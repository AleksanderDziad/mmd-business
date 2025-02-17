#!/bin/bash

echo "📜 Pobieranie logów Backend..."
docker logs backend --tail 50

echo "📜 Pobieranie logów Frontend..."
docker logs frontend --tail 50

echo "📜 Uruchamiam monitorowanie logów backendu i frontendu..."
docker-compose logs -f backend frontend

