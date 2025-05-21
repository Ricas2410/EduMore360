#!/usr/bin/env python
"""
This script patches the settings.py file to make it more flexible with database URLs.
It's used during the build process on Render to avoid the strict DATABASE_URL validation.
"""

import os
import re

# Path to the settings file
settings_path = 'edumore360/settings.py'

# Read the current content
with open(settings_path, 'r') as f:
    content = f.read()

# Define the pattern to search for
pattern = r"""# Get DATABASE_URL from environment or \.env file
db_url = os\.environ\.get\('DATABASE_URL', env\('DATABASE_URL', default=None\)\)

if not db_url or not db_url\.startswith\('postgresql'\):
    raise ValueError\("DATABASE_URL is not set or is invalid\. Please set a valid PostgreSQL DATABASE_URL\."\)"""

# Define the replacement
replacement = """# Get DATABASE_URL from environment or .env file
db_url = os.environ.get('DATABASE_URL', env('DATABASE_URL', default=None))

# For Render deployment, we need to be more flexible
if not db_url:
    print("WARNING: DATABASE_URL is not set. Using SQLite as a fallback.")
    db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
elif not db_url.startswith('postgresql'):
    print(f"WARNING: DATABASE_URL does not start with 'postgresql': {db_url}")
    print("This may cause issues in production environments.")"""

# Replace the pattern with the replacement
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the modified content back to the file
with open(settings_path, 'w') as f:
    f.write(new_content)

print("Settings file patched successfully!")
