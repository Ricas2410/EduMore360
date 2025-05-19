"""
Script to re-upload specific files to Wasabi.
Run this script with: python scripts/reupload_to_wasabi.py
"""

import os
import sys
import django
import logging
import boto3
from pathlib import Path
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

def upload_file_to_wasabi(s3_client, bucket_name, file_path, object_name=None, content_type=None):
    """Upload a file to Wasabi bucket."""
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    # Determine content type based on file extension if not provided
    if content_type is None:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.jpg', '.jpeg']:
            content_type = 'image/jpeg'
        elif ext == '.png':
            content_type = 'image/png'
        elif ext == '.gif':
            content_type = 'image/gif'
        elif ext == '.pdf':
            content_type = 'application/pdf'
        else:
            content_type = 'application/octet-stream'
    
    try:
        extra_args = {
            'ACL': 'public-read',
            'ContentType': content_type
        }
        
        s3_client.upload_file(
            file_path, 
            bucket_name, 
            object_name,
            ExtraArgs=extra_args
        )
        logger.info(f"Successfully uploaded {file_path} to {object_name}")
        return True
    except ClientError as e:
        logger.error(f"Error uploading {file_path}: {e}")
        return False

def reupload_specific_files():
    """Re-upload specific files to Wasabi."""
    # Get the media root directory
    media_root = os.path.join(settings.BASE_DIR, 'media')
    
    if not os.path.exists(media_root):
        logger.error(f"Media directory {media_root} does not exist")
        return
    
    # Create Wasabi client
    s3_client, bucket_name = create_wasabi_client()
    
    # List of specific files to re-upload
    files_to_upload = [
        # Hero backgrounds
        "hero_backgrounds/Educore_education_made_simple.gif",
        "hero_backgrounds/kids_learn.png",
        "hero_backgrounds/student_with_PCs.png",
        "hero_backgrounds/th.jfif",
        "hero_backgrounds/th_p60p5o5.jfif",
        
        # Hero foregrounds
        "hero_foregrounds/Educore_education_made_simple.gif",
        "hero_foregrounds/Educore_education_made_simple_m0a1Jkf.gif",
        "hero_foregrounds/Educore_education_made_simple_qx7U2eA.gif",
        "hero_foregrounds/kids_learn.png",
        "hero_foregrounds/student_with_PCs.png",
        
        # Mascots
        "mascots/th.jfif",
        "mascots/th_p06PuT7.jfif",
        
        # Notes
        "notes/others/E419503030010ST_1.pdf",
        
        # Profile pictures
        "profile_pictures/PP.jpg",
        "profile_pictures/PP_BsXEb7I.jpg"
    ]
    
    # Normalize paths for Windows
    files_to_upload = [f.replace('/', os.sep) for f in files_to_upload]
    
    # Upload each file
    success_count = 0
    error_count = 0
    
    for rel_path in files_to_upload:
        file_path = os.path.join(media_root, rel_path)
        
        # Skip files that don't exist
        if not os.path.exists(file_path):
            logger.warning(f"File {file_path} does not exist, skipping")
            error_count += 1
            continue
        
        # Normalize path for Wasabi (use forward slashes)
        wasabi_path = rel_path.replace(os.sep, '/')
        
        # Upload file to Wasabi
        if upload_file_to_wasabi(s3_client, bucket_name, file_path, wasabi_path):
            success_count += 1
        else:
            error_count += 1
    
    logger.info(f"Re-upload complete: {success_count} files uploaded successfully, {error_count} errors")

def set_bucket_public():
    """Set the bucket to be publicly accessible."""
    try:
        s3_client, bucket_name = create_wasabi_client()
        
        # Set bucket ACL to public-read
        s3_client.put_bucket_acl(
            Bucket=bucket_name,
            ACL='public-read'
        )
        logger.info("Bucket ACL set to public-read")
        
        return True
    
    except Exception as e:
        logger.error(f"Error setting bucket to public: {e}")
        return False

def set_objects_public():
    """Set all objects in the bucket to be publicly accessible."""
    try:
        s3_client, bucket_name = create_wasabi_client()
        
        # List all objects in bucket
        paginator = s3_client.get_paginator('list_objects_v2')
        count = 0
        
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Contents' in page:
                for obj in page['Contents']:
                    # Set object ACL to public-read
                    s3_client.put_object_acl(
                        Bucket=bucket_name,
                        Key=obj['Key'],
                        ACL='public-read'
                    )
                    count += 1
                    logger.info(f"Set {obj['Key']} to public-read")
        
        logger.info(f"All {count} objects set to public-read")
        
        return True
    
    except Exception as e:
        logger.error(f"Error setting objects to public: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 Re-upload to Wasabi")
    print("==============================")
    
    # Set bucket to public
    print("\nSetting bucket to public...")
    set_bucket_public()
    
    # Re-upload specific files
    print("\nRe-uploading specific files...")
    reupload_specific_files()
    
    # Set all objects to public
    print("\nSetting all objects to public...")
    set_objects_public()
    
    print("\nRe-upload complete!")
