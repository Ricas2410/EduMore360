"""
Script to test Backblaze B2 storage configuration.
Run this script with: python scripts/test_b2_storage.py
"""

import os
import sys
import django
import logging
import boto3
import environ
from pathlib import Path
from datetime import datetime
from io import BytesIO
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

def test_b2_storage():
    """Test B2 storage by uploading, retrieving, and deleting a test file."""
    try:
        # Get B2 credentials
        key_id, application_key, bucket_name = get_b2_credentials()
        if not all([key_id, application_key, bucket_name]):
            return False

        # Create a test file
        test_filename = f"test_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        test_content = f"This is a test file created at {datetime.now().isoformat()}"

        logger.info(f"Creating test file: {test_filename}")

        # Create S3 client
        s3_client = boto3.client(
            's3',
            endpoint_url='https://s3.us-east-005.backblazeb2.com',
            aws_access_key_id=key_id,
            aws_secret_access_key=application_key,
            region_name='us-east-005'
        )

        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket {bucket_name} exists")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.info(f"Bucket {bucket_name} does not exist, creating...")
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': 'us-east-005'}
                )
                logger.info(f"Bucket {bucket_name} created successfully")
            else:
                logger.error(f"Error checking bucket: {e}")
                return False

        # Upload the file
        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=test_filename,
                Body=test_content.encode('utf-8'),
                ContentType='text/plain',
                ACL='public-read'
            )
            logger.info(f"File uploaded to: {test_filename}")
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            return False

        # Get the file URL
        url = f"https://{bucket_name}.s3.us-east-005.backblazeb2.com/{test_filename}"
        logger.info(f"File URL: {url}")

        # Check if the file exists
        try:
            s3_client.head_object(Bucket=bucket_name, Key=test_filename)
            logger.info(f"File exists: True")
        except ClientError as e:
            logger.error(f"Error checking file: {e}")
            return False

        # Read the file
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=test_filename)
            content = response['Body'].read().decode('utf-8')
            logger.info(f"File content: {content}")
        except ClientError as e:
            logger.error(f"Error reading file: {e}")
            return False

        # Delete the file
        try:
            s3_client.delete_object(Bucket=bucket_name, Key=test_filename)
            logger.info(f"File deleted")
        except ClientError as e:
            logger.error(f"Error deleting file: {e}")
            return False

        # Verify deletion
        try:
            s3_client.head_object(Bucket=bucket_name, Key=test_filename)
            logger.error(f"File still exists after deletion")
            return False
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.info(f"File no longer exists: True")
                logger.info("B2 storage test completed successfully!")
                return True
            else:
                logger.error(f"Error verifying deletion: {e}")
                return False

    except Exception as e:
        logger.error(f"Error testing B2 storage: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 B2 Storage Test")
    print("==========================")

    # Get B2 credentials
    key_id, application_key, bucket_name = get_b2_credentials()
    if not all([key_id, application_key, bucket_name]):
        print("B2 credentials not found. Please check your .env file.")
        sys.exit(1)

    print(f"Testing B2 storage with bucket: {bucket_name}")
    print(f"Using key ID: {key_id[:4]}...{key_id[-4:]}")

    # Run the test
    success = test_b2_storage()

    if success:
        print("\nB2 storage test completed successfully!")
    else:
        print("\nB2 storage test failed. Please check the logs for details.")
        sys.exit(1)
