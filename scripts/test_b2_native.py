"""
Script to test Backblaze B2 storage using the native B2 API.
Run this script with: python scripts/test_b2_native.py
"""

import os
import sys
import logging
import environ
from pathlib import Path
from datetime import datetime
from io import BytesIO
from b2sdk.v2 import InMemoryAccountInfo, B2Api

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

def test_b2_native():
    """Test B2 storage using the native B2 API."""
    try:
        # Get B2 credentials
        key_id, application_key, bucket_name = get_b2_credentials()
        if not all([key_id, application_key, bucket_name]):
            return False

        # Create a test file
        test_filename = f"test_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        test_content = f"This is a test file created at {datetime.now().isoformat()}"

        logger.info(f"Creating test file: {test_filename}")

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
            logger.info(f"Bucket {bucket_name} not found, creating...")
            bucket = b2_api.create_bucket(bucket_name, 'allPrivate')
            logger.info(f"Bucket {bucket_name} created successfully")

        # Upload file
        logger.info(f"Uploading file: {test_filename}")
        uploaded_file = bucket.upload_bytes(
            test_content.encode('utf-8'),
            test_filename,
            content_type='text/plain'
        )
        logger.info(f"File uploaded: {uploaded_file.file_name}")

        # Get file info
        file_version = uploaded_file.id_
        logger.info(f"File version: {file_version}")

        # Generate a signed URL (valid for 1 hour)
        logger.info(f"Generating signed URL for: {test_filename}")

        # Get download URL with authorization
        file_url = bucket.get_download_url(test_filename)
        logger.info(f"File URL: {file_url}")

        # For B2 SDK v2, we need to use the download_url_params
        # Note: The URL is not pre-authorized in the free tier without payment info
        logger.info(f"Note: For private buckets, you'll need to generate authorized URLs in your application")

        # Download file using the bucket API
        logger.info(f"Downloading file using bucket API: {test_filename}")

        # Create a temporary file to save the content
        temp_file_path = f"temp_{test_filename}"

        try:
            # Download the file to a temporary location
            downloaded_file = bucket.download_file_by_name(test_filename)
            downloaded_file.save_to(temp_file_path)

            # Read the content from the temporary file
            with open(temp_file_path, 'r') as f:
                downloaded_content = f.read()
                logger.info(f"Downloaded content: {downloaded_content}")

        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logger.info(f"Temporary file {temp_file_path} removed")

        # Verify content
        if downloaded_content == test_content:
            logger.info("File content verified successfully")
        else:
            logger.error("File content verification failed")
            return False

        # Delete file
        logger.info(f"Deleting file: {test_filename}")
        # In B2 SDK v2, we need to use the file_id and file_name
        bucket.delete_file_version(file_id=file_version, file_name=test_filename)
        logger.info("File deleted successfully")

        # Verify deletion
        try:
            bucket.download_file_by_name(test_filename)
            logger.error("File still exists after deletion")
            return False
        except Exception as e:
            logger.info("File no longer exists, deletion verified")

        logger.info("B2 native API test completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Error testing B2 native API: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 B2 Native API Test")
    print("=============================")

    # Get B2 credentials
    key_id, application_key, bucket_name = get_b2_credentials()
    if not all([key_id, application_key, bucket_name]):
        print("B2 credentials not found. Please check your .env file.")
        sys.exit(1)

    print(f"Testing B2 native API with bucket: {bucket_name}")
    print(f"Using key ID: {key_id[:4]}...{key_id[-4:]}")

    # Run the test
    success = test_b2_native()

    if success:
        print("\nB2 native API test completed successfully!")
    else:
        print("\nB2 native API test failed. Please check the logs for details.")
        sys.exit(1)
