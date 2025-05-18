"""
Script to list all files in the B2 bucket.
Run this script with: python scripts/list_b2_files.py
"""

import os
import sys
import django
import logging
import environ
from pathlib import Path
from b2sdk.v2 import InMemoryAccountInfo, B2Api

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_b2_credentials():
    """Get B2 credentials from .env file."""
    env = environ.Env()
    env.read_env(str(Path(__file__).resolve().parent.parent / '.env'))
    
    key_id = env('B2_KEY_ID')
    application_key = env('B2_APPLICATION_KEY')
    bucket_name = env('B2_BUCKET_NAME')
    
    if not all([key_id, application_key, bucket_name]):
        logger.error("B2 credentials not found in environment variables")
        return None, None, None
    
    return key_id, application_key, bucket_name

def list_b2_files():
    """List all files in the B2 bucket."""
    try:
        # Get B2 credentials
        key_id, application_key, bucket_name = get_b2_credentials()
        if not all([key_id, application_key, bucket_name]):
            logger.error("B2 credentials not found. Please check your .env file.")
            return False
        
        # Set up B2 API
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        
        # Authorize account
        logger.info("Authorizing B2 account...")
        b2_api.authorize_account("production", key_id, application_key)
        logger.info("B2 account authorized successfully")
        
        # Get bucket
        logger.info(f"Looking for bucket: {bucket_name}")
        try:
            bucket = b2_api.get_bucket_by_name(bucket_name)
            logger.info(f"Found bucket: {bucket_name}")
        except Exception as e:
            logger.error(f"Bucket {bucket_name} not found: {e}")
            return False
        
        # List all files in the bucket
        logger.info(f"Listing all files in bucket {bucket_name}...")
        file_count = 0
        file_list = []
        
        for file_info, _ in bucket.ls():
            file_count += 1
            file_list.append({
                'name': file_info.file_name,
                'size': file_info.size,
                'id': file_info.id_
            })
        
        # Sort files by name
        file_list.sort(key=lambda x: x['name'])
        
        # Print file list
        print(f"\nFound {file_count} files in bucket {bucket_name}:")
        print("-" * 80)
        print(f"{'File Name':<50} {'Size':<10} {'ID':<20}")
        print("-" * 80)
        
        for file in file_list:
            print(f"{file['name']:<50} {file['size']:<10} {file['id']}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error listing B2 files: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 B2 File Listing")
    print("==========================")
    
    list_b2_files()
