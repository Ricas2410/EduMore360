"""
Script to migrate media files from local storage to Wasabi Cloud Storage.
Run this script with: python scripts/migrate_to_wasabi.py
"""

import os
import sys
import django
import logging
from pathlib import Path
from tqdm import tqdm
import boto3
from botocore.exceptions import ClientError

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

def create_wasabi_client():
    """Create and return a boto3 client for Wasabi."""
    try:
        # Get Wasabi credentials from Django settings
        # These are now loaded from environment variables in settings.py
        access_key = settings.AWS_ACCESS_KEY_ID
        secret_key = settings.AWS_SECRET_ACCESS_KEY
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
        region_name = settings.AWS_S3_REGION_NAME

        # Create S3-compatible client for Wasabi
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )

        return s3_client, settings.AWS_STORAGE_BUCKET_NAME

    except Exception as e:
        logger.error(f"Error creating Wasabi client: {e}")
        sys.exit(1)

def upload_file_to_wasabi(s3_client, bucket_name, file_path, object_name=None):
    """Upload a file to Wasabi bucket."""
    if object_name is None:
        object_name = file_path

    try:
        s3_client.upload_file(
            file_path,
            bucket_name,
            object_name,
            ExtraArgs={'ACL': 'public-read'}  # Use public-read ACL
        )
        return True
    except ClientError as e:
        logger.error(f"Error uploading {file_path}: {e}")
        return False

def migrate_media_files():
    """Migrate all media files from local storage to Wasabi."""
    # Get the media root directory
    media_root = os.path.join(settings.BASE_DIR, 'media')

    if not os.path.exists(media_root):
        logger.error(f"Media directory {media_root} does not exist")
        return

    # Create Wasabi client
    s3_client, bucket_name = create_wasabi_client()

    # Check if bucket exists
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} exists")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            logger.info(f"Bucket {bucket_name} does not exist, creating...")
            try:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': settings.AWS_S3_REGION_NAME}
                )
                logger.info(f"Bucket {bucket_name} created successfully")
            except Exception as e:
                logger.error(f"Error creating bucket: {e}")
                return
        else:
            logger.error(f"Error checking bucket: {e}")
            return

    # List existing files in the bucket to avoid duplicates
    logger.info("Listing existing files in the bucket...")
    existing_files = set()
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Contents' in page:
                for obj in page['Contents']:
                    existing_files.add(obj['Key'])
        logger.info(f"Found {len(existing_files)} existing files in the bucket")
    except Exception as e:
        logger.error(f"Error listing bucket contents: {e}")
        # Continue anyway, we'll just upload everything

    # Walk through the media directory
    total_files = sum([len(files) for _, _, files in os.walk(media_root)])
    logger.info(f"Found {total_files} files to migrate")

    success_count = 0
    skip_count = 0
    error_count = 0

    with tqdm(total=total_files, desc="Migrating files") as pbar:
        for root, _, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)

                # Get relative path from media root
                rel_path = os.path.relpath(file_path, media_root)

                # Skip hidden files and directories
                if file.startswith('.') or any(part.startswith('.') for part in rel_path.split(os.sep)):
                    pbar.update(1)
                    continue

                # Skip files that already exist in the bucket
                if rel_path in existing_files:
                    logger.debug(f"Skipping {rel_path} - already exists in bucket")
                    skip_count += 1
                    pbar.update(1)
                    continue

                # Upload file to Wasabi
                if upload_file_to_wasabi(s3_client, bucket_name, file_path, rel_path):
                    success_count += 1
                else:
                    error_count += 1

                pbar.update(1)

    logger.info(f"Migration complete: {success_count} files uploaded successfully, {skip_count} files skipped, {error_count} errors")

def test_wasabi_connection():
    """Test the connection to Wasabi."""
    try:
        s3_client, bucket_name = create_wasabi_client()

        # List objects in bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=5)

        if 'Contents' in response:
            logger.info(f"Successfully connected to Wasabi bucket {bucket_name}")
            logger.info(f"Found {len(response['Contents'])} objects in bucket")
            for obj in response['Contents']:
                logger.info(f"  - {obj['Key']} ({obj['Size']} bytes)")
        else:
            logger.info(f"Successfully connected to Wasabi bucket {bucket_name} (empty bucket)")

        return True

    except Exception as e:
        logger.error(f"Error testing Wasabi connection: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 Media Migration to Wasabi Cloud Storage")
    print("=================================================")

    # Test Wasabi connection
    print("\nTesting connection to Wasabi...")
    if not test_wasabi_connection():
        print("Failed to connect to Wasabi. Please check your credentials and try again.")
        sys.exit(1)

    # Confirm migration
    print("\nThis script will migrate all media files from your local storage to Wasabi Cloud Storage.")
    print("Your local files will NOT be deleted.")
    confirm = input("\nDo you want to continue? (y/n): ")

    if confirm.lower() != 'y':
        print("Migration cancelled.")
        sys.exit(0)

    # Perform migration
    print("\nStarting migration...")
    migrate_media_files()
    print("\nMigration complete!")

    print("\nImportant Notes:")
    print("1. All files are now stored in Wasabi Cloud Storage")
    print("2. Files are publicly accessible (using public-read ACL)")
    print("3. Use the media_url template tag to generate URLs in your templates")
    print("4. Example: {% load media_tags %}{% media_url object.image.name %}")
