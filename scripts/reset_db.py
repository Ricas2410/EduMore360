import os
import sys
import shutil
import subprocess

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')

def activate_venv():
    """Get the command to activate the virtual environment."""
    if sys.platform == 'win32':
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def run_command(command):
    """Run a shell command and print the output."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stderr)
        return False

def reset_database():
    """Reset the database by removing the SQLite file."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')
    if os.path.exists(db_path):
        print(f"Removing database file: {db_path}")
        os.remove(db_path)
        print("Database file removed.")
    else:
        print("Database file does not exist. Nothing to remove.")

def remove_migrations():
    """Remove all migration files except __init__.py."""
    apps = ['accounts', 'core', 'curriculum', 'quiz', 'subscription']
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for app in apps:
        migrations_dir = os.path.join(base_dir, app, 'migrations')
        if os.path.exists(migrations_dir):
            print(f"Cleaning migrations for {app}...")
            for filename in os.listdir(migrations_dir):
                if filename != '__init__.py' and filename.endswith('.py'):
                    file_path = os.path.join(migrations_dir, filename)
                    os.remove(file_path)
                    print(f"  Removed: {filename}")
            
            # Also remove __pycache__ directory
            pycache_dir = os.path.join(migrations_dir, '__pycache__')
            if os.path.exists(pycache_dir):
                shutil.rmtree(pycache_dir)
                print(f"  Removed: __pycache__")

def main():
    """Main function to reset the database and run migrations."""
    print("Starting database reset process...")
    
    # Activate virtual environment
    venv_activate = activate_venv()
    
    # Reset database
    reset_database()
    
    # Remove migrations
    remove_migrations()
    
    # Make migrations
    print("\n=== Making migrations ===")
    run_command(f"{venv_activate} && python manage.py makemigrations accounts")
    run_command(f"{venv_activate} && python manage.py makemigrations core")
    run_command(f"{venv_activate} && python manage.py makemigrations curriculum")
    run_command(f"{venv_activate} && python manage.py makemigrations quiz")
    run_command(f"{venv_activate} && python manage.py makemigrations subscription")
    
    # Apply migrations
    print("\n=== Applying migrations ===")
    run_command(f"{venv_activate} && python manage.py migrate")
    
    # Populate sample data
    print("\n=== Populating sample data ===")
    run_command(f"{venv_activate} && python scripts/populate_sample_data.py")
    
    print("\nDatabase reset and population completed successfully!")

if __name__ == "__main__":
    main()
