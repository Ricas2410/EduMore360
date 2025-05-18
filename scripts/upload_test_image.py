"""
Script to upload a test image to B2 bucket.
Run this script with: python scripts/upload_test_image.py
"""

import os
import sys
import django
import logging
from pathlib import Path
from datetime import datetime
from PIL import Image
from io import BytesIO
from b2sdk.v2 import InMemoryAccountInfo, B2Api

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

def get_b2_credentials():
    """Get B2 credentials from .env file."""
    import environ
    env = environ.Env()
    env.read_env(str(Path(__file__).resolve().parent.parent / '.env'))
    
    key_id = env('B2_KEY_ID')
    application_key = env('B2_APPLICATION_KEY')
    bucket_name = env('B2_BUCKET_NAME')
    
    if not all([key_id, application_key, bucket_name]):
        logger.error("B2 credentials not found in environment variables")
        return None, None, None
    
    return key_id, application_key, bucket_name

def upload_test_image():
    """Upload a test image to B2 bucket using Django's default_storage."""
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
        logger.error(f"Error uploading test image: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 Test Image Upload")
    print("===========================")
    
    # Upload test image
    success = upload_test_image()
    
    if success:
        print("\nTest image uploaded successfully!")
        print("\nImportant Notes:")
        print("1. The image is stored in a private B2 bucket")
        print("2. The URL is signed and expires after 1 hour by default")
        print("3. Use the media_url template tag to generate signed URLs in your templates")
        print("4. Example: {% load media_tags %}{% media_url object.image.name %}")
    else:
        print("\nTest image upload failed. Please check the logs for details.")
