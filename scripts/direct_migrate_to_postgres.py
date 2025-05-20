"""
Script to directly migrate data from SQLite to PostgreSQL.
Run this script with: python scripts/direct_migrate_to_postgres.py
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
from django.db import connections
from django.apps import apps

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
            'default': sqlite_config  # Keep default as SQLite for now
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

def test_connections():
    """Test both database connections."""
    logger.info("Testing database connections...")

    try:
        # Test SQLite connection
        cursor = connections['sqlite'].cursor()
        cursor.execute("SELECT sqlite_version();")
        sqlite_version = cursor.fetchone()[0]
        logger.info(f"SQLite version: {sqlite_version}")

        # Test PostgreSQL connection
        cursor = connections['postgres'].cursor()
        cursor.execute("SELECT version();")
        pg_version = cursor.fetchone()[0]
        logger.info(f"PostgreSQL version: {pg_version}")

        return True
    except Exception as e:
        logger.error(f"Error testing connections: {e}")
        return False

def run_migrations_on_postgres():
    """Run migrations on PostgreSQL."""
    logger.info("Running migrations on PostgreSQL...")

    try:
        # Run migrations using subprocess to ensure proper database selection
        cmd = [
            sys.executable,
            'manage.py',
            'migrate',
            '--database=postgres'
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        if result.returncode != 0:
            logger.error(f"Error running migrations: {result.stderr}")
            return False

        logger.info("Migrations completed successfully")
        logger.info(result.stdout)
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
                objects = list(model.objects.using('sqlite').all())
                count = len(objects)
                logger.info(f"Found {count} {model_name} objects in SQLite")

                # Skip if no objects
                if count == 0:
                    continue

                # Save objects to PostgreSQL
                for i, obj in enumerate(objects):
                    try:
                        # Reset primary key to let PostgreSQL assign a new one
                        # This helps avoid conflicts
                        if hasattr(obj, 'pk'):
                            obj.pk = None

                        # Save to PostgreSQL
                        obj.save(using='postgres')

                        # Log progress for large models
                        if (i + 1) % 100 == 0 or i + 1 == count:
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

def set_postgres_as_default():
    """Set PostgreSQL as the default database."""
    logger.info("Setting PostgreSQL as the default database...")

    try:
        # Update the .env file
        env_path = os.path.join(settings.BASE_DIR, '.env')
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()

        # Replace the DATABASE_URL line
        if 'DATABASE_URL=' in env_content:
            env_content = env_content.replace(
                'DATABASE_URL=sqlite:///db.sqlite3',
                f'DATABASE_URL={POSTGRES_URL}'
            )

        # Write the updated content
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)

        logger.info("Updated .env file with PostgreSQL connection string")
        return True
    except Exception as e:
        logger.error(f"Error setting PostgreSQL as default: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 Direct SQLite to PostgreSQL Migration")
    print("===============================================")

    # Step 1: Set up databases
    print("\nStep 1: Setting up database connections...")
    if not setup_databases():
        print("Failed to set up database connections. Exiting.")
        sys.exit(1)

    # Step 2: Test connections
    print("\nStep 2: Testing database connections...")
    if not test_connections():
        print("Failed to connect to databases. Exiting.")
        sys.exit(1)

    # Step 3: Run migrations on PostgreSQL
    print("\nStep 3: Running migrations on PostgreSQL...")
    if not run_migrations_on_postgres():
        print("Failed to run migrations. Exiting.")
        sys.exit(1)

    # Step 4: Migrate data
    print("\nStep 4: Migrating data from SQLite to PostgreSQL...")
    if not migrate_data():
        print("Failed to migrate data. Exiting.")
        sys.exit(1)

    # Step 5: Set PostgreSQL as default
    print("\nStep 5: Setting PostgreSQL as the default database...")
    if not set_postgres_as_default():
        print("Failed to set PostgreSQL as default. Exiting.")
        sys.exit(1)

    print("\nMigration completed successfully!")
    print("\nNext steps:")
    print("1. Test your application with the PostgreSQL database")
    print("2. Deploy your application to Railway")
