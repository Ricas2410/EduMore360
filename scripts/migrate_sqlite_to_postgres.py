"""
Script to migrate data from SQLite to PostgreSQL.
This script:
1. Creates a temporary SQLite database connection
2. Creates a temporary PostgreSQL database connection
3. Migrates data from SQLite to PostgreSQL
4. Handles Unicode characters properly

Usage:
python scripts/migrate_sqlite_to_postgres.py
"""

import os
import sys
import django
import logging
import subprocess
import time
from pathlib import Path
import dj_database_url
import psycopg2
import sqlite3
import json

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

# SQLite database path
SQLITE_PATH = "db.sqlite3"

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
os.environ['DATABASE_URL'] = POSTGRES_URL  # Set PostgreSQL as the default database
django.setup()

from django.core.management import call_command
from django.db import connections
from django.apps import apps
from django.conf import settings

def test_postgres_connection():
    """Test the PostgreSQL connection."""
    logger.info("Testing PostgreSQL connection...")
    
    try:
        # Parse the database URL
        db_config = dj_database_url.parse(POSTGRES_URL)
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=db_config['HOST'],
            port=db_config['PORT'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            dbname=db_config['NAME'],
            sslmode='require'
        )
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute a test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        logger.info(f"PostgreSQL version: {version}")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        return False

def test_sqlite_connection():
    """Test the SQLite connection."""
    logger.info("Testing SQLite connection...")
    
    try:
        # Connect to SQLite
        conn = sqlite3.connect(SQLITE_PATH)
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute a test query
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()[0]
        logger.info(f"SQLite version: {version}")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        logger.error(f"Error connecting to SQLite: {e}")
        return False

def run_migrations():
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

def dump_sqlite_data():
    """Dump data from SQLite to a JSON file."""
    logger.info("Dumping data from SQLite...")
    
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
            '--database=sqlite',
            f'--output={backup_file}'
        ]
        
        # Create a temporary settings file for SQLite
        temp_settings = """
from edumore360.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
"""
        with open('temp_settings.py', 'w', encoding='utf-8') as f:
            f.write(temp_settings)
        
        # Run the command with the temporary settings
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'temp_settings'
        
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        # Clean up the temporary settings file
        os.remove('temp_settings.py')
        
        if result.returncode != 0:
            logger.error(f"Error during dumpdata: {result.stderr}")
            return False
        
        logger.info(f"SQLite data dumped successfully to {backup_file}")
        return backup_file
    except Exception as e:
        logger.error(f"Error dumping SQLite data: {e}")
        return False

def load_data_to_postgres(backup_file):
    """Load data from JSON file to PostgreSQL."""
    logger.info("Loading data to PostgreSQL...")
    
    try:
        # Set environment variable to force UTF-8 encoding
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        # Use subprocess to run loaddata with proper encoding
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
        return True
    except Exception as e:
        logger.error(f"Error loading data to PostgreSQL: {e}")
        return False

def count_records():
    """Count records in key tables to verify migration."""
    logger.info("Counting records in key tables...")
    
    try:
        # Get all models
        all_models = apps.get_models()
        
        for model in all_models:
            try:
                count = model.objects.count()
                logger.info(f"{model.__name__}: {count} records")
            except Exception as e:
                logger.warning(f"Could not count records for {model.__name__}: {e}")
        
        return True
    except Exception as e:
        logger.error(f"Error counting records: {e}")
        return False

def main():
    """Main function."""
    print("SQLite to PostgreSQL Migration")
    print("==============================")
    
    # Step 1: Test connections
    print("\nStep 1: Testing database connections...")
    if not test_sqlite_connection():
        print("Failed to connect to SQLite. Exiting.")
        return False
    
    if not test_postgres_connection():
        print("Failed to connect to PostgreSQL. Exiting.")
        return False
    
    # Step 2: Run migrations on PostgreSQL
    print("\nStep 2: Running migrations on PostgreSQL...")
    if not run_migrations():
        print("Failed to run migrations. Exiting.")
        return False
    
    # Step 3: Dump data from SQLite
    print("\nStep 3: Dumping data from SQLite...")
    backup_file = dump_sqlite_data()
    if not backup_file:
        print("Failed to dump data from SQLite. Exiting.")
        return False
    
    # Step 4: Load data to PostgreSQL
    print("\nStep 4: Loading data to PostgreSQL...")
    if not load_data_to_postgres(backup_file):
        print("Failed to load data to PostgreSQL. Exiting.")
        return False
    
    # Step 5: Count records to verify migration
    print("\nStep 5: Counting records to verify migration...")
    if not count_records():
        print("Failed to count records. Please check the logs.")
        return False
    
    print("\nMigration completed successfully!")
    print("\nYour application is now configured to use PostgreSQL in both local and deployment environments.")
    
    return True

if __name__ == "__main__":
    main()
