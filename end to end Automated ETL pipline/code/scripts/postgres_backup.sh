#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M")
BACKUP_DIR="/opt/airflow/backups"
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

# ✅ Provide password non-interactively
export PGPASSWORD="airflow"

pg_dump -h postgres -U airflow -d airflow > $BACKUP_FILE

# Remove password from environment
unset PGPASSWORD

# Check if backup is non-empty
if [ -s "$BACKUP_FILE" ]; then
    echo "✅ Backup created successfully: $BACKUP_FILE"
else
    echo "❌ Backup failed: file is empty"
fi

# Cleanup: keep last 7 backups
find /opt/airflow/backups -type f -name "backup_*.sql" -mtime +7 -delete
echo "🧹 Backups older than 7 days removed"