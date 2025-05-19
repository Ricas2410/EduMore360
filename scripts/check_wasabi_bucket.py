"""
Script to check Wasabi bucket configuration.
Run this script with: python scripts/check_wasabi_bucket.py
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
        
        return s3_client
    
    except Exception as e:
        logger.error(f"Error creating Wasabi client: {e}")
        return None

def check_bucket_acl():
    """Check the ACL of the bucket."""
    try:
        s3_client = create_wasabi_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        # Get bucket ACL
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        logger.info(f"Bucket ACL: {acl}")
        
        # Check if bucket is public
        is_public = False
        for grant in acl['Grants']:
            if 'URI' in grant['Grantee'] and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                is_public = True
                logger.info(f"Permission for AllUsers: {grant['Permission']}")
        
        if is_public:
            logger.info("Bucket is publicly accessible")
        else:
            logger.info("Bucket is NOT publicly accessible")
        
        return is_public
    
    except Exception as e:
        logger.error(f"Error checking bucket ACL: {e}")
        return False

def check_bucket_policy():
    """Check the policy of the bucket."""
    try:
        s3_client = create_wasabi_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        # Get bucket policy
        try:
            policy = s3_client.get_bucket_policy(Bucket=bucket_name)
            logger.info(f"Bucket policy: {policy['Policy']}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                logger.info("No bucket policy found")
            else:
                raise
        
        return True
    
    except Exception as e:
        logger.error(f"Error checking bucket policy: {e}")
        return False

def check_bucket_cors():
    """Check the CORS configuration of the bucket."""
    try:
        s3_client = create_wasabi_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        # Get bucket CORS
        try:
            cors = s3_client.get_bucket_cors(Bucket=bucket_name)
            logger.info(f"Bucket CORS: {cors}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
                logger.info("No CORS configuration found")
            else:
                raise
        
        return True
    
    except Exception as e:
        logger.error(f"Error checking bucket CORS: {e}")
        return False

def list_bucket_objects():
    """List objects in the bucket."""
    try:
        s3_client = create_wasabi_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        # List objects in bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=10)
        
        if 'Contents' in response:
            logger.info(f"Found {len(response['Contents'])} objects in bucket")
            for obj in response['Contents']:
                logger.info(f"  - {obj['Key']} ({obj['Size']} bytes)")
                
                # Try to get the object ACL
                try:
                    acl = s3_client.get_object_acl(Bucket=bucket_name, Key=obj['Key'])
                    is_public = False
                    for grant in acl['Grants']:
                        if 'URI' in grant['Grantee'] and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                            is_public = True
                            logger.info(f"    Permission for AllUsers: {grant['Permission']}")
                    
                    if is_public:
                        logger.info("    Object is publicly accessible")
                    else:
                        logger.info("    Object is NOT publicly accessible")
                except Exception as e:
                    logger.error(f"    Error getting object ACL: {e}")
        else:
            logger.info("No objects found in bucket")
        
        return True
    
    except Exception as e:
        logger.error(f"Error listing bucket objects: {e}")
        return False

def set_bucket_public():
    """Set the bucket to be publicly accessible."""
    try:
        s3_client = create_wasabi_client()
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

def set_objects_public():
    """Set all objects in the bucket to be publicly accessible."""
    try:
        s3_client = create_wasabi_client()
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
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
                    if count % 10 == 0:
                        logger.info(f"Set {count} objects to public-read")
        
        logger.info(f"All {count} objects set to public-read")
        
        return True
    
    except Exception as e:
        logger.error(f"Error setting objects to public: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 Wasabi Bucket Checker")
    print("================================")
    
    # Check bucket ACL
    print("\nChecking bucket ACL...")
    check_bucket_acl()
    
    # Check bucket policy
    print("\nChecking bucket policy...")
    check_bucket_policy()
    
    # Check bucket CORS
    print("\nChecking bucket CORS...")
    check_bucket_cors()
    
    # List bucket objects
    print("\nListing bucket objects...")
    list_bucket_objects()
    
    # Ask if user wants to set bucket and objects to public
    print("\nDo you want to set the bucket and all objects to public-read? (y/n)")
    choice = input().lower()
    
    if choice == 'y':
        print("\nSetting bucket to public-read...")
        set_bucket_public()
        
        print("\nSetting all objects to public-read...")
        set_objects_public()
        
        print("\nDone!")
    else:
        print("\nSkipping public access settings.")
