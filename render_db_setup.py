#!/usr/bin/env python
"""
This script sets up the database configuration for Render deployment.
It creates a direct database configuration file that will be used during runtime.
"""

import os
import json

# Get the DATABASE_URL from the environment
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("WARNING: DATABASE_URL is not set. Using SQLite as a fallback.")
    db_config = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
else:
    # Parse the DATABASE_URL
    if db_url.startswith('postgres://'):
        # Extract the components from the URL
        # Format: postgres://username:password@host:port/database
        db_url = db_url.replace('postgres://', '')
        auth, rest = db_url.split('@', 1)
        username, password = auth.split(':', 1)
        host_port, database = rest.split('/', 1)
        
        if ':' in host_port:
            host, port = host_port.split(':', 1)
        else:
            host = host_port
            port = '5432'
            
        # Handle query parameters
        if '?' in database:
            database, params = database.split('?', 1)
        else:
            params = ''
            
        # Create the database configuration
        db_config = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': database,
            'USER': username,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }
        
        # Add SSL options if needed
        if 'sslmode=require' in params:
            db_config['OPTIONS'] = {'sslmode': 'require'}
    else:
        print(f"WARNING: Unsupported DATABASE_URL format: {db_url}")
        print("Using SQLite as a fallback.")
        db_config = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }

# Create the database configuration file
config_dir = 'edumore360'
config_file = os.path.join(config_dir, 'db_config.json')

# Ensure the directory exists
os.makedirs(config_dir, exist_ok=True)

# Write the configuration to the file
with open(config_file, 'w') as f:
    json.dump({'default': db_config}, f, indent=2)

print(f"Database configuration written to {config_file}")
print(f"Using database engine: {db_config['ENGINE']}")
print(f"Database name: {db_config['NAME']}")
if 'HOST' in db_config:
    print(f"Database host: {db_config['HOST']}")
