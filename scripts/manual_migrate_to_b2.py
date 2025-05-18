"""
Script to manually migrate specific files from local storage to B2.
Run this script with: python scripts/manual_migrate_to_b2.py
"""

import os
import sys
import django
import logging
import environ
from pathlib import Path
from tqdm import tqdm
from b2sdk.v2 import InMemoryAccountInfo, B2Api

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.conf import settings

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

def create_b2_api():
    """Create and return a B2 API client and bucket."""
    try:
        # Get B2 credentials
        key_id, application_key, bucket_name = get_b2_credentials()
        if not all([key_id, application_key, bucket_name]):
            logger.error("B2 credentials not found. Please check your .env file.")
            sys.exit(1)
        
        # Set up B2 API
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        
        # Authorize account
        logger.info("Authorizing B2 account...")
        b2_api.authorize_account("production", key_id, application_key)
        logger.info("B2 account authorized successfully")
        
        # Get or create bucket
        logger.info(f"Looking for bucket: {bucket_name}")
        try:
            bucket = b2_api.get_bucket_by_name(bucket_name)
            logger.info(f"Found bucket: {bucket_name}")
        except Exception as e:
            logger.info(f"Bucket {bucket_name} not found, creating...")
            bucket = b2_api.create_bucket(bucket_name, 'allPrivate')
            logger.info(f"Bucket {bucket_name} created successfully")
        
        return b2_api, bucket
    
    except Exception as e:
        logger.error(f"Error creating B2 API client: {e}")
        sys.exit(1)

def upload_file_to_b2(bucket, file_path, object_name=None):
    """Upload a file to B2 bucket using the native API."""
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    try:
        # Upload the file
        uploaded_file = bucket.upload_local_file(
            local_file=file_path,
            file_name=object_name
        )
        logger.info(f"Uploaded {file_path} to {object_name} with ID {uploaded_file.id_}")
        return True
    except Exception as e:
        logger.error(f"Error uploading {file_path}: {e}")
        return False

def manual_migrate_files():
    """Manually migrate specific files from local storage to B2."""
    # Get the media root directory
    media_root = settings.MEDIA_ROOT
    
    if not os.path.exists(media_root):
        logger.error(f"Media directory {media_root} does not exist")
        return
    
    # Create B2 API client and get bucket
    _, bucket = create_b2_api()
    
    # List existing files in the bucket to avoid duplicates
    logger.info("Listing existing files in the bucket...")
    existing_files = set()
    try:
        for file_info, _ in bucket.ls():
            existing_files.add(file_info.file_name)
        logger.info(f"Found {len(existing_files)} existing files in the bucket")
    except Exception as e:
        logger.error(f"Error listing bucket contents: {e}")
        # Continue anyway, we'll just upload everything
    
    # Define the files to migrate
    files_to_migrate = [
        "hero_backgrounds/Educore_education_made_simple.gif",
        "hero_backgrounds/kids_learn.png",
        "hero_backgrounds/student_with_PCs.png",
        "hero_backgrounds/th.jfif",
        "hero_backgrounds/th_p60p5o5.jfif",
        "hero_foregrounds/Educore_education_made_simple.gif",
        "hero_foregrounds/Educore_education_made_simple_m0a1Jkf.gif",
        "hero_foregrounds/Educore_education_made_simple_qx7U2eA.gif",
        "hero_foregrounds/kids_learn.png",
        "hero_foregrounds/student_with_PCs.png",
        "mascots/th.jfif",
        "mascots/th_p06PuT7.jfif",
        "notes/others/E419503030010ST_1.pdf",
        "profile_pictures/PP.jpg",
        "profile_pictures/PP_BsXEb7I.jpg"
    ]
    
    # Normalize paths for Windows
    files_to_migrate = [f.replace('/', os.sep) for f in files_to_migrate]
    
    logger.info(f"Found {len(files_to_migrate)} files to migrate")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    with tqdm(total=len(files_to_migrate), desc="Migrating files") as pbar:
        for rel_path in files_to_migrate:
            file_path = os.path.join(media_root, rel_path)
            
            # Skip files that don't exist
            if not os.path.exists(file_path):
                logger.warning(f"File {file_path} does not exist, skipping")
                skip_count += 1
                pbar.update(1)
                continue
            
            # Normalize path for B2 (use forward slashes)
            b2_path = rel_path.replace(os.sep, '/')
            
            # Skip files that already exist in the bucket
            if b2_path in existing_files:
                logger.info(f"Skipping {b2_path} - already exists in bucket")
                skip_count += 1
                pbar.update(1)
                continue
            
            # Upload file to B2
            if upload_file_to_b2(bucket, file_path, b2_path):
                success_count += 1
            else:
                error_count += 1
            
            pbar.update(1)
    
    logger.info(f"Migration complete: {success_count} files uploaded successfully, {skip_count} files skipped, {error_count} errors")

if __name__ == "__main__":
    print("EduMore360 Manual Media Migration to B2")
    print("=======================================")
    
    # Perform migration
    print("\nStarting manual migration...")
    manual_migrate_files()
    print("\nMigration complete!")
    
    print("\nImportant Notes:")
    print("1. All files are now stored in a private B2 bucket")
    print("2. URLs for these files will be signed and expire after 1 hour by default")
    print("3. Use the media_url template tag to generate signed URLs in your templates")
    print("4. Example: {% load media_tags %}{% media_url object.image.name %}")
