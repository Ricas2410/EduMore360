"""
Script to migrate data from SQLite to PostgreSQL.
Run this script with: python scripts/migrate_to_postgres.py
"""

import os
import sys
import django
import logging
import subprocess
from pathlib import Path
import dj_database_url

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# PostgreSQL connection string
POSTGRES_URL = "postgresql://neondb_owner:npg_R5dEIG2wvtSl@ep-soft-violet-a58sv217-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

def backup_sqlite_data():
    """Create a JSON dump of all data from SQLite."""
    logger.info("Creating a backup of SQLite data...")

    try:
        # Create backups directory if it doesn't exist
        os.makedirs('backups', exist_ok=True)

        # Set environment variable to force UTF-8 encoding
        os.environ['PYTHONIOENCODING'] = 'utf-8'

        # Use subprocess to run dumpdata with proper encoding
        backup_file = os.path.join('backups', 'sqlite_data.json')

        # Build the command
        cmd = [
            sys.executable,  # Current Python interpreter
            'manage.py',
            'dumpdata',
            '--exclude=contenttypes',
            '--exclude=auth.permission',
            '--natural-foreign',
            '--natural-primary',
            '--indent=2',
        ]

        # Run the command and capture output
        logger.info(f"Running command: {' '.join(cmd)}")
        with open(backup_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

        if result.returncode != 0:
            logger.error(f"Error during dumpdata: {result.stderr}")
            return False

        logger.info(f"SQLite data backup created successfully at {backup_file}")
        return True
    except Exception as e:
        logger.error(f"Error backing up SQLite data: {e}")
        return False

def configure_postgres():
    """Configure Django to use PostgreSQL."""
    logger.info("Configuring Django to use PostgreSQL...")

    try:
        # Parse the database URL
        db_config = dj_database_url.parse(POSTGRES_URL)

        # Update Django settings
        settings.DATABASES['default'] = db_config

        # Log the configuration (without password)
        safe_config = db_config.copy()
        if 'PASSWORD' in safe_config:
            safe_config['PASSWORD'] = '********'
        logger.info(f"Database configuration updated: {safe_config}")

        return True
    except Exception as e:
        logger.error(f"Error configuring PostgreSQL: {e}")
        return False

def migrate_database():
    """Run migrations on PostgreSQL."""
    logger.info("Running migrations on PostgreSQL...")

    try:
        # Run migrations
        call_command('migrate')

        logger.info("Migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        return False

def load_data_to_postgres():
    """Load data from JSON dump to PostgreSQL."""
    logger.info("Loading data to PostgreSQL...")

    try:
        # Set environment variable to force UTF-8 encoding
        os.environ['PYTHONIOENCODING'] = 'utf-8'

        # Use subprocess to run loaddata with proper encoding
        backup_file = os.path.join('backups', 'sqlite_data.json')

        # Build the command
        cmd = [
            sys.executable,  # Current Python interpreter
            'manage.py',
            'loaddata',
            backup_file
        ]

        # Run the command
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        if result.returncode != 0:
            logger.error(f"Error during loaddata: {result.stderr}")
            return False

        logger.info("Data loaded successfully to PostgreSQL")
        logger.info(result.stdout)
        return True
    except Exception as e:
        logger.error(f"Error loading data to PostgreSQL: {e}")
        return False

def test_postgres_connection():
    """Test the PostgreSQL connection."""
    logger.info("Testing PostgreSQL connection...")

    from django.db import connections
    try:
        # Get a cursor
        cursor = connections['default'].cursor()
        # Execute a simple query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result[0] == 1:
            logger.info("PostgreSQL connection test successful")
            return True
        else:
            logger.error("PostgreSQL connection test failed")
            return False
    except Exception as e:
        logger.error(f"Error testing PostgreSQL connection: {e}")
        return False

def count_records():
    """Count records in key tables to verify migration."""
    logger.info("Counting records in key tables...")

    from django.apps import apps

    try:
        # Get all models
        all_models = apps.get_models()

        for model in all_models:
            count = model.objects.count()
            logger.info(f"{model.__name__}: {count} records")

        return True
    except Exception as e:
        logger.error(f"Error counting records: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 SQLite to PostgreSQL Migration")
    print("=========================================")

    # Step 1: Backup SQLite data
    print("\nStep 1: Backing up SQLite data...")
    if not backup_sqlite_data():
        print("Failed to backup SQLite data. Exiting.")
        sys.exit(1)

    # Step 2: Configure PostgreSQL
    print("\nStep 2: Configuring PostgreSQL...")
    if not configure_postgres():
        print("Failed to configure PostgreSQL. Exiting.")
        sys.exit(1)

    # Step 3: Test PostgreSQL connection
    print("\nStep 3: Testing PostgreSQL connection...")
    if not test_postgres_connection():
        print("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)

    # Step 4: Run migrations on PostgreSQL
    print("\nStep 4: Running migrations on PostgreSQL...")
    if not migrate_database():
        print("Failed to run migrations. Exiting.")
        sys.exit(1)

    # Step 5: Load data to PostgreSQL
    print("\nStep 5: Loading data to PostgreSQL...")
    if not load_data_to_postgres():
        print("Failed to load data to PostgreSQL. Exiting.")
        sys.exit(1)

    # Step 6: Count records to verify migration
    print("\nStep 6: Verifying migration by counting records...")
    if not count_records():
        print("Failed to verify migration. Please check the logs.")
        sys.exit(1)

    print("\nMigration completed successfully!")
    print("\nNext steps:")
    print("1. Update your .env file with the PostgreSQL connection string")
    print("2. Update your settings.py to use PostgreSQL by default")
    print("3. Test your application with the new database")
