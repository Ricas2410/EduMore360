"""
Script to toggle between local and B2 storage.
Run this script with: python scripts/toggle_storage.py [local|b2]
"""

import os
import sys
import django
import boto3
import logging
from pathlib import Path
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.conf import settings
import environ

def create_b2_bucket():
    """Create a B2 bucket if it doesn't exist."""
    try:
        # Get B2 credentials from environment
        env = environ.Env()
        env.read_env(str(Path(settings.BASE_DIR) / '.env'))

        key_id = env('B2_KEY_ID')
        application_key = env('B2_APPLICATION_KEY')
        bucket_name = env('B2_BUCKET_NAME')

        if not all([key_id, application_key, bucket_name]):
            logger.error("B2 credentials not found in environment variables")
            return False

        # Create S3-compatible client for B2
        s3_client = boto3.client(
            's3',
            endpoint_url='https://s3.us-east-005.backblazeb2.com',
            aws_access_key_id=key_id,
            aws_secret_access_key=application_key,
            region_name='us-east-005'
        )

        # Check if bucket exists, create if not
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket {bucket_name} exists")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.info(f"Bucket {bucket_name} does not exist, creating...")
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': 'us-east-005'},
                    ACL='private'  # Use private ACL instead of public
                )
                logger.info(f"Bucket {bucket_name} created successfully")
                return True
            else:
                logger.error(f"Error checking bucket: {e}")
                return False

    except Exception as e:
        logger.error(f"Error creating B2 bucket: {e}")
        return False

def toggle_storage(mode):
    """Toggle between local and B2 storage."""
    env_file = Path(settings.BASE_DIR) / '.env'

    if not env_file.exists():
        logger.error(f"Error: .env file not found at {env_file}")
        return False

    # Read the current .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()

    # Find the DEBUG line
    debug_line_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('DEBUG='):
            debug_line_index = i
            break

    if debug_line_index is None:
        logger.error("Error: DEBUG setting not found in .env file")
        return False

    # Update the DEBUG setting
    if mode == 'local':
        lines[debug_line_index] = 'DEBUG=True\n'
        logger.info("Switching to local storage (DEBUG=True)")
    elif mode == 'b2':
        # Create B2 bucket if it doesn't exist
        if not create_b2_bucket():
            logger.error("Failed to create or verify B2 bucket. Check your credentials.")
            return False

        lines[debug_line_index] = 'DEBUG=False\n'
        logger.info("Switching to B2 storage (DEBUG=False)")
    else:
        logger.error(f"Error: Invalid mode '{mode}'. Use 'local' or 'b2'")
        return False

    # Write the updated .env file
    with open(env_file, 'w') as f:
        f.writelines(lines)

    logger.info(f"Storage mode updated to: {mode}")
    logger.info("Restart your Django server for changes to take effect")

    return True

if __name__ == "__main__":
    print("EduMore360 Storage Toggle")
    print("=========================")

    if len(sys.argv) != 2 or sys.argv[1] not in ['local', 'b2', 'create-bucket']:
        print("Usage: python scripts/toggle_storage.py [local|b2|create-bucket]")
        print("  local: Use local storage (DEBUG=True)")
        print("  b2: Use B2 storage (DEBUG=False)")
        print("  create-bucket: Create B2 bucket without changing storage mode")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == 'create-bucket':
        print("Creating B2 bucket...")
        if create_b2_bucket():
            print("B2 bucket created or verified successfully")
        else:
            print("Failed to create or verify B2 bucket. Check your credentials.")
            sys.exit(1)
    else:
        toggle_storage(mode)
