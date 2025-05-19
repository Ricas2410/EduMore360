"""
Script to set up Filebase bucket and test connectivity.
Run this script with: python scripts/setup_filebase.py
"""

import os
import sys
import django
import logging
import boto3
from pathlib import Path
from datetime import datetime
from botocore.exceptions import ClientError
from PIL import Image
from io import BytesIO

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_filebase_client():
    """Create and return a boto3 client for Filebase."""
    try:
        # Get Filebase credentials from Django settings
        access_key = settings.AWS_ACCESS_KEY_ID
        secret_key = settings.AWS_SECRET_ACCESS_KEY
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
        region_name = settings.AWS_S3_REGION_NAME
        
        # Create S3-compatible client for Filebase
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )
        
        return s3_client
    
    except Exception as e:
        logger.error(f"Error creating Filebase client: {e}")
        return None

def create_bucket():
    """Create a bucket in Filebase."""
    try:
        s3_client = create_filebase_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket {bucket_name} already exists")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.info(f"Bucket {bucket_name} does not exist, creating...")
                s3_client.create_bucket(Bucket=bucket_name)
                logger.info(f"Bucket {bucket_name} created successfully")
                return True
            else:
                logger.error(f"Error checking bucket: {e}")
                return False
    
    except Exception as e:
        logger.error(f"Error creating bucket: {e}")
        return False

def set_bucket_public():
    """Set the bucket to be publicly accessible."""
    try:
        s3_client = create_filebase_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
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

def create_test_image(width=200, height=200, color=(255, 0, 0)):
    """Create a test image for upload."""
    image = Image.new('RGB', (width, height), color)
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    return image_io

def test_upload():
    """Test uploading a file to Filebase using Django's default_storage."""
    try:
        # Create a test image
        test_filename = f"test_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        image_io = create_test_image()
        
        logger.info(f"Creating test image: {test_filename}")
        
        # Upload the file using Django's default_storage
        path = default_storage.save(test_filename, ContentFile(image_io.getvalue()))
        logger.info(f"File uploaded to: {path}")
        
        # Get the file URL
        url = default_storage.url(path)
        logger.info(f"File URL: {url}")
        
        # Check if the file exists
        exists = default_storage.exists(path)
        logger.info(f"File exists: {exists}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error testing upload: {e}")
        return False

def test_direct_upload():
    """Test uploading a file to Filebase using boto3."""
    try:
        s3_client = create_filebase_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        # Create a test file
        test_filename = f"test_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        test_content = f"This is a test file created at {datetime.now().isoformat()}"
        
        # Upload the file
        logger.info(f"Uploading test file: {test_filename}")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_filename,
            Body=test_content,
            ContentType='text/plain',
            ACL='public-read'
        )
        logger.info(f"File uploaded successfully")
        
        # Get the file URL
        file_url = f"{settings.AWS_S3_ENDPOINT_URL}/{bucket_name}/{test_filename}"
        logger.info(f"File URL: {file_url}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error testing direct upload: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 Filebase Setup")
    print("=========================")
    
    # Create bucket
    print("\nCreating bucket...")
    if not create_bucket():
        print("Failed to create bucket. Exiting.")
        sys.exit(1)
    
    # Set bucket to public
    print("\nSetting bucket to public...")
    if not set_bucket_public():
        print("Failed to set bucket to public. Exiting.")
        sys.exit(1)
    
    # Test upload using Django's default_storage
    print("\nTesting upload using Django's default_storage...")
    if not test_upload():
        print("Failed to upload file using Django's default_storage.")
    
    # Test direct upload using boto3
    print("\nTesting direct upload using boto3...")
    if not test_direct_upload():
        print("Failed to upload file using boto3.")
    
    print("\nSetup complete!")
