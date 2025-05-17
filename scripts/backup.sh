#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env.production

# Configuration
BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_BACKUP_PATH="$BACKUP_DIR/db_$TIMESTAMP.sql.gz"
MEDIA_BACKUP_PATH="$BACKUP_DIR/media_$TIMESTAMP.tar.gz"
KEEP_DAYS=7

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Extract database credentials from DATABASE_URL
DB_USER=$(echo $DATABASE_URL | sed -E 's/^postgres:\/\/([^:]+):.*/\1/')
DB_PASS=$(echo $DATABASE_URL | sed -E 's/^postgres:\/\/[^:]+:([^@]+).*/\1/')
DB_HOST=$(echo $DATABASE_URL | sed -E 's/^postgres:\/\/[^@]+@([^:]+).*/\1/')
DB_PORT=$(echo $DATABASE_URL | sed -E 's/^postgres:\/\/[^@]+@[^:]+:([^\/]+).*/\1/')
DB_NAME=$(echo $DATABASE_URL | sed -E 's/^postgres:\/\/[^@]+@[^\/]+\/([^?]+).*/\1/')

# Backup database
echo "Backing up database to $DB_BACKUP_PATH..."
PGPASSWORD=$DB_PASS pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME | gzip > $DB_BACKUP_PATH
echo "Database backup completed."

# Backup media files
echo "Backing up media files to $MEDIA_BACKUP_PATH..."
tar -czf $MEDIA_BACKUP_PATH -C /path/to/edumore360 media
echo "Media backup completed."

# Remove old backups
echo "Removing backups older than $KEEP_DAYS days..."
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +$KEEP_DAYS -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +$KEEP_DAYS -delete
echo "Old backups removed."

# Optional: Upload to cloud storage
if [ ! -z "$AWS_ACCESS_KEY_ID" ] && [ ! -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "Uploading backups to S3..."
    aws s3 cp $DB_BACKUP_PATH s3://$AWS_STORAGE_BUCKET_NAME/backups/
    aws s3 cp $MEDIA_BACKUP_PATH s3://$AWS_STORAGE_BUCKET_NAME/backups/
    echo "Upload completed."
fi

echo "Backup process completed successfully!"
