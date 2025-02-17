#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="db_backups"
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

echo "📦 Tworzenie kopii zapasowej bazy danych..."
docker exec db pg_dump -U db_user -d db_name > $BACKUP_FILE

echo "✅ Backup zapisany jako: $BACKUP_FILE"

