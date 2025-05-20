"""
Simple script to migrate from SQLite to PostgreSQL.
This script:
1. Dumps data from SQLite
2. Updates settings to use PostgreSQL
3. Runs migrations on PostgreSQL
4. Loads data into PostgreSQL
"""

import os
import sys
import subprocess
import time

# Paths
BACKUP_DIR = "backups"
BACKUP_FILE = os.path.join(BACKUP_DIR, "data_backup.json")
ENV_FILE = ".env"

# PostgreSQL connection string
POSTGRES_URL = "postgresql://neondb_owner:npg_R5dEIG2wvtSl@ep-soft-violet-a58sv217-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

def run_command(command, description):
    """Run a command and print its output."""
    print(f"\n{description}...")
    print(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        
        print(f"Success: {description}")
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False

def backup_sqlite_data():
    """Backup data from SQLite."""
    # Create backup directory if it doesn't exist
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Dump data from SQLite
    return run_command(
        ["python", "manage.py", "dumpdata", "--exclude=contenttypes", "--exclude=auth.permission", 
         "--natural-foreign", "--natural-primary", "--indent=2", "--output=" + BACKUP_FILE],
        "Backing up data from SQLite"
    )

def update_env_file():
    """Update .env file to use PostgreSQL."""
    print("\nUpdating .env file to use PostgreSQL...")
    
    try:
        # Read current .env file
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace DATABASE_URL
        if "DATABASE_URL=" in content:
            content = content.replace(
                "DATABASE_URL=sqlite:///db.sqlite3",
                f"DATABASE_URL={POSTGRES_URL}"
            )
            content = content.replace(
                "DATABASE_URL=postgresql://neondb_owner:npg_R5dEIG2wvtSl@ep-soft-violet-a58sv217-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require",
                f"DATABASE_URL={POSTGRES_URL}"
            )
        else:
            content += f"\nDATABASE_URL={POSTGRES_URL}\n"
        
        # Write updated content
        with open(ENV_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Successfully updated .env file")
        return True
    except Exception as e:
        print(f"Error updating .env file: {e}")
        return False

def run_migrations():
    """Run migrations on PostgreSQL."""
    return run_command(
        ["python", "manage.py", "migrate"],
        "Running migrations on PostgreSQL"
    )

def load_data():
    """Load data into PostgreSQL."""
    return run_command(
        ["python", "manage.py", "loaddata", BACKUP_FILE],
        "Loading data into PostgreSQL"
    )

def test_connection():
    """Test PostgreSQL connection."""
    return run_command(
        ["python", "manage.py", "dbshell", "--command", "SELECT version();"],
        "Testing PostgreSQL connection"
    )

def main():
    """Main function."""
    print("Simple SQLite to PostgreSQL Migration")
    print("=====================================")
    
    # Step 1: Backup SQLite data
    if not backup_sqlite_data():
        print("Failed to backup SQLite data. Exiting.")
        return False
    
    # Step 2: Update .env file
    if not update_env_file():
        print("Failed to update .env file. Exiting.")
        return False
    
    # Step 3: Run migrations
    if not run_migrations():
        print("Failed to run migrations. Exiting.")
        return False
    
    # Step 4: Load data
    if not load_data():
        print("Failed to load data. Exiting.")
        return False
    
    # Step 5: Test connection
    if not test_connection():
        print("Failed to test connection. Exiting.")
        return False
    
    print("\nMigration completed successfully!")
    print("\nNext steps:")
    print("1. Test your application with the PostgreSQL database")
    print("2. Deploy your application to Railway")
    
    return True

if __name__ == "__main__":
    main()
