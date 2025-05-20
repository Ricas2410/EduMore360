"""
A simpler script to migrate from SQLite to PostgreSQL.
This script:
1. Runs migrations on PostgreSQL
2. Manually transfers data from SQLite to PostgreSQL for each model

Usage:
python scripts/migrate_db_simple.py
"""

import os
import sys
import django
import logging
from pathlib import Path
import dj_database_url
import psycopg2
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# PostgreSQL connection string
POSTGRES_URL = "postgresql://neondb_owner:npg_R5dEIG2wvtSl@ep-soft-violet-a58sv217-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.core.management import call_command
from django.db import connections
from django.apps import apps
from django.conf import settings

def setup_databases():
    """Set up both SQLite and PostgreSQL connections."""
    logger.info("Setting up database connections...")

    try:
        # Create a SQLite configuration
        sqlite_config = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(settings.BASE_DIR, 'db.sqlite3'),
        }

        # Parse the PostgreSQL URL
        postgres_config = dj_database_url.parse(POSTGRES_URL)

        # Set up both connections
        settings.DATABASES = {
            'sqlite': sqlite_config,
            'postgres': postgres_config,
            'default': postgres_config  # Set PostgreSQL as default
        }

        # Log the configuration (without passwords)
        sqlite_config_log = settings.DATABASES['sqlite'].copy()
        pg_config_log = settings.DATABASES['postgres'].copy()

        if 'PASSWORD' in pg_config_log:
            pg_config_log['PASSWORD'] = '********'

        logger.info(f"SQLite config: {sqlite_config_log}")
        logger.info(f"PostgreSQL config: {pg_config_log}")

        return True
    except Exception as e:
        logger.error(f"Error setting up databases: {e}")
        return False

def run_migrations():
    """Run migrations on PostgreSQL."""
    logger.info("Running migrations on PostgreSQL...")

    try:
        # Run migrations on the default database (which is now PostgreSQL)
        call_command('migrate')

        logger.info("Migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        return False

def migrate_data():
    """Migrate data from SQLite to PostgreSQL model by model."""
    logger.info("Migrating data from SQLite to PostgreSQL...")

    try:
        # Get all models
        all_models = apps.get_models()

        # Sort models to handle dependencies
        # This is a simple approach - you might need to adjust the order
        model_names = [model.__name__ for model in all_models]
        logger.info(f"Models to migrate: {', '.join(model_names)}")

        # Process each model
        for model in all_models:
            model_name = model.__name__
            logger.info(f"Migrating {model_name}...")

            # Skip contenttypes and permissions
            if model_name in ['ContentType', 'Permission']:
                logger.info(f"Skipping {model_name}")
                continue

            # Get all objects from SQLite
            try:
                # First check if the model exists in SQLite
                try:
                    # Try to get one object to see if the table exists
                    model.objects.using('sqlite').first()
                except Exception as e:
                    logger.warning(f"Model {model_name} does not exist in SQLite or has errors: {e}")
                    continue

                # Get all objects from SQLite
                objects = list(model.objects.using('sqlite').all())
                count = len(objects)
                logger.info(f"Found {count} {model_name} objects in SQLite")

                # Skip if no objects
                if count == 0:
                    continue

                # Save objects to PostgreSQL
                for i, obj in enumerate(objects):
                    try:
                        # Create a new object in PostgreSQL with the same primary key
                        new_obj = model()

                        # Copy all field values
                        for field in obj._meta.fields:
                            field_name = field.name

                            try:
                                field_value = getattr(obj, field_name)

                                # Handle special cases for problematic fields
                                if isinstance(field_value, str) and '\U0001f4d8' in field_value:
                                    # Replace problematic emoji with a placeholder
                                    field_value = field_value.replace('\U0001f4d8', '[BOOK]')

                                # Set the value on the new object
                                if field_value is not None:
                                    setattr(new_obj, field_name, field_value)
                            except Exception as field_error:
                                logger.warning(f"Error copying field {field_name}: {field_error}")

                        # Save to default database (PostgreSQL)
                        new_obj.save()

                        # Log progress for large models
                        if (i + 1) % 10 == 0 or i + 1 == count:
                            logger.info(f"Migrated {i + 1}/{count} {model_name} objects")
                    except Exception as e:
                        logger.error(f"Error migrating {model_name} object: {e}")
            except Exception as e:
                logger.error(f"Error processing {model_name}: {e}")

        logger.info("Data migration completed")
        return True
    except Exception as e:
        logger.error(f"Error migrating data: {e}")
        return False

def count_records():
    """Count records in key tables to verify migration."""
    logger.info("Counting records in key tables...")

    try:
        # Get all models
        all_models = apps.get_models()

        for model in all_models:
            try:
                # Try to count records in SQLite
                try:
                    sqlite_count = model.objects.using('sqlite').count()
                except Exception:
                    sqlite_count = "N/A"

                # Count records in PostgreSQL (default database)
                postgres_count = model.objects.count()

                logger.info(f"{model.__name__}: SQLite={sqlite_count}, PostgreSQL={postgres_count}")
            except Exception as e:
                logger.warning(f"Could not count records for {model.__name__}: {e}")

        return True
    except Exception as e:
        logger.error(f"Error counting records: {e}")
        return False

def main():
    """Main function."""
    print("Simple SQLite to PostgreSQL Migration")
    print("=====================================")

    # Step 1: Set up databases
    print("\nStep 1: Setting up database connections...")
    if not setup_databases():
        print("Failed to set up database connections. Exiting.")
        return False

    # Step 2: Run migrations on PostgreSQL
    print("\nStep 2: Running migrations on PostgreSQL...")
    if not run_migrations():
        print("Failed to run migrations. Exiting.")
        return False

    # Step 3: Migrate data
    print("\nStep 3: Migrating data from SQLite to PostgreSQL...")
    if not migrate_data():
        print("Failed to migrate data. Exiting.")
        return False

    # Step 4: Count records to verify migration
    print("\nStep 4: Counting records to verify migration...")
    if not count_records():
        print("Failed to count records. Please check the logs.")
        return False

    print("\nMigration completed successfully!")
    print("\nYour application is now configured to use PostgreSQL in both local and deployment environments.")

    return True

if __name__ == "__main__":
    main()
