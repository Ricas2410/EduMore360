"""
Script to test Wasabi Cloud Storage integration.
Run this script with: python scripts/test_wasabi.py
"""

import os
import sys
import django
import logging
from pathlib import Path
from datetime import datetime
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import ClientError

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

def create_test_image(width=200, height=200, color=(255, 0, 0)):
    """Create a test image for upload."""
    image = Image.new('RGB', (width, height), color)
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    return image_io

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

        return s3_client

    except Exception as e:
        logger.error(f"Error creating Wasabi client: {e}")
        return None

def test_bucket_exists(s3_client, bucket_name):
    """Test if the bucket exists, create it if not."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} exists")
        return True
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
                return True
            except Exception as e:
                logger.error(f"Error creating bucket: {e}")
                return False
        else:
            logger.error(f"Error checking bucket: {e}")
            return False

def test_django_storage():
    """Test Django's default_storage with Wasabi."""
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

        # Delete the file
        default_storage.delete(path)
        logger.info(f"File deleted")

        # Verify deletion
        exists = default_storage.exists(path)
        logger.info(f"File exists after deletion: {exists}")

        if not exists:
            logger.info("Django storage test completed successfully!")
            return True
        else:
            logger.error("Failed to delete test file")
            return False

    except Exception as e:
        logger.error(f"Error testing Django storage: {e}")
        return False

def test_direct_boto3():
    """Test direct boto3 access to Wasabi."""
    try:
        # Create S3 client
        s3_client = create_wasabi_client()
        if not s3_client:
            return False

        # Get bucket name from settings
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        # Test if bucket exists
        if not test_bucket_exists(s3_client, bucket_name):
            return False

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

        # Download the file
        logger.info(f"Downloading file: {test_filename}")
        response = s3_client.get_object(Bucket=bucket_name, Key=test_filename)
        downloaded_content = response['Body'].read().decode('utf-8')
        logger.info(f"Downloaded content: {downloaded_content}")

        # Verify content
        if downloaded_content == test_content:
            logger.info("File content verified successfully")
        else:
            logger.error("File content verification failed")
            return False

        # Delete the file
        logger.info(f"Deleting file: {test_filename}")
        s3_client.delete_object(Bucket=bucket_name, Key=test_filename)
        logger.info("File deleted successfully")

        # Verify deletion
        try:
            s3_client.head_object(Bucket=bucket_name, Key=test_filename)
            logger.error("File still exists after deletion")
            return False
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.info("File no longer exists, deletion verified")
            else:
                logger.error(f"Error checking file deletion: {e}")
                return False

        logger.info("Direct boto3 test completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Error testing direct boto3: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 Wasabi Cloud Storage Test")
    print("====================================")

    print("\nTesting Django storage integration...")
    django_success = test_django_storage()

    print("\nTesting direct boto3 access...")
    boto3_success = test_direct_boto3()

    if django_success and boto3_success:
        print("\nAll tests completed successfully!")
        print("\nWasabi Cloud Storage is properly configured and working.")
    else:
        print("\nSome tests failed. Please check the logs for details.")
