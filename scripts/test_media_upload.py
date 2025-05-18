"""
Script to test media upload and retrieval using Django's default_storage.
Run this script with: python scripts/test_media_upload.py
"""

import os
import sys
import django
import logging
from pathlib import Path
from datetime import datetime
from io import BytesIO
from PIL import Image

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

def test_media_upload():
    """Test media upload and retrieval using Django's default_storage."""
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
        
        # Read the file
        with default_storage.open(path, 'rb') as f:
            content = f.read()
            logger.info(f"File size: {len(content)} bytes")
        
        # Delete the file
        default_storage.delete(path)
        logger.info(f"File deleted")
        
        # Verify deletion
        exists = default_storage.exists(path)
        logger.info(f"File exists after deletion: {exists}")
        
        if not exists:
            logger.info("Media upload test completed successfully!")
            return True
        else:
            logger.error("Failed to delete test file")
            return False
        
    except Exception as e:
        logger.error(f"Error testing media upload: {e}")
        return False

if __name__ == "__main__":
    print("EduMore360 Media Upload Test")
    print("============================")
    
    # Check if B2 is configured
    if not hasattr(settings, 'AWS_STORAGE_BUCKET_NAME'):
        print("B2 storage is not configured. Please check your settings.")
        sys.exit(1)
    
    print(f"Testing media upload with bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
    
    # Run the test
    success = test_media_upload()
    
    if success:
        print("\nMedia upload test completed successfully!")
        print("\nImportant Notes for Using Private B2 Buckets:")
        print("1. All URLs are signed and expire after 1 hour by default")
        print("2. For user-uploaded content, the URLs will need to be refreshed if accessed after expiration")
        print("3. For static content like images on your site, consider using a CDN like Cloudflare")
    else:
        print("\nMedia upload test failed. Please check the logs for details.")
        sys.exit(1)
