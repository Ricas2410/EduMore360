import os
import sys
import subprocess
import time

def run_command(command):
    """Run a shell command and print the output."""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Print output in real-time
    for line in process.stdout:
        print(line.strip())
    
    # Wait for the process to complete
    process.wait()
    
    # Print any errors
    for line in process.stderr:
        print(f"ERROR: {line.strip()}")
    
    return process.returncode

def activate_venv():
    """Activate the virtual environment."""
    if sys.platform == 'win32':
        return ".\\venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def main():
    """Main function to set up the project."""
    print("Setting up EduMore360 project...")
    
    # Activate virtual environment
    venv_activate = activate_venv()
    
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
    
    # Create superuser
    print("\n=== Creating superuser ===")
    print("Please create a superuser account:")
    run_command(f"{venv_activate} && python manage.py createsuperuser")
    
    # Populate sample data
    print("\n=== Populating sample data ===")
    run_command(f"{venv_activate} && python scripts/populate_sample_data.py")
    
    # Install Tailwind CSS dependencies
    print("\n=== Setting up Tailwind CSS ===")
    os.chdir("theme/static_src")
    run_command("npm install")
    run_command("npm run build")
    os.chdir("../..")
    
    # Collect static files
    print("\n=== Collecting static files ===")
    run_command(f"{venv_activate} && python manage.py collectstatic --noinput")
    
    print("\n=== Setup complete! ===")
    print("You can now run the development server with:")
    print(f"{venv_activate} && python manage.py runserver")

if __name__ == "__main__":
    main()
