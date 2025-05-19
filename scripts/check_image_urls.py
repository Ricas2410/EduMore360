"""
Script to check image URLs in the database.
Run this script with: python scripts/check_image_urls.py
"""

import os
import sys
import django
import logging
import requests
from pathlib import Path

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from core.models import HeroSection, KidFriendlyTheme

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_url(url, description):
    """Check if a URL is accessible."""
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            logger.info(f"✅ {description} URL is accessible: {url}")
            return True
        else:
            logger.error(f"❌ {description} URL returned status code {response.status_code}: {url}")
            return False
    except Exception as e:
        logger.error(f"❌ {description} URL is not accessible: {url} - Error: {e}")
        return False

def check_hero_section_images():
    """Check all hero section images."""
    hero_sections = HeroSection.objects.all()
    logger.info(f"Found {hero_sections.count()} hero sections")
    
    for hero in hero_sections:
        logger.info(f"\nChecking images for hero section: {hero.title}")
        
        if hero.background_image:
            url = default_storage.url(hero.background_image.name)
            check_url(url, f"Background image for {hero.title}")
            logger.info(f"Background image name: {hero.background_image.name}")
            logger.info(f"Background image URL: {url}")
        else:
            logger.info(f"No background image for {hero.title}")
        
        if hero.foreground_image:
            url = default_storage.url(hero.foreground_image.name)
            check_url(url, f"Foreground image for {hero.title}")
            logger.info(f"Foreground image name: {hero.foreground_image.name}")
            logger.info(f"Foreground image URL: {url}")
        else:
            logger.info(f"No foreground image for {hero.title}")
        
        if hero.mascot_image:
            url = default_storage.url(hero.mascot_image.name)
            check_url(url, f"Mascot image for {hero.title}")
            logger.info(f"Mascot image name: {hero.mascot_image.name}")
            logger.info(f"Mascot image URL: {url}")
        else:
            logger.info(f"No mascot image for {hero.title}")

def check_theme_images():
    """Check all theme images."""
    themes = KidFriendlyTheme.objects.all()
    logger.info(f"\nFound {themes.count()} themes")
    
    for theme in themes:
        logger.info(f"\nChecking images for theme: {theme.name}")
        
        if theme.background_image:
            url = default_storage.url(theme.background_image.name)
            check_url(url, f"Background image for {theme.name}")
            logger.info(f"Background image name: {theme.background_image.name}")
            logger.info(f"Background image URL: {url}")
        else:
            logger.info(f"No background image for {theme.name}")
        
        if theme.header_image:
            url = default_storage.url(theme.header_image.name)
            check_url(url, f"Header image for {theme.name}")
            logger.info(f"Header image name: {theme.header_image.name}")
            logger.info(f"Header image URL: {url}")
        else:
            logger.info(f"No header image for {theme.name}")
        
        if theme.footer_image:
            url = default_storage.url(theme.footer_image.name)
            check_url(url, f"Footer image for {theme.name}")
            logger.info(f"Footer image name: {theme.footer_image.name}")
            logger.info(f"Footer image URL: {url}")
        else:
            logger.info(f"No footer image for {theme.name}")
        
        if theme.mascot_image:
            url = default_storage.url(theme.mascot_image.name)
            check_url(url, f"Mascot image for {theme.name}")
            logger.info(f"Mascot image name: {theme.mascot_image.name}")
            logger.info(f"Mascot image URL: {url}")
        else:
            logger.info(f"No mascot image for {theme.name}")

def check_storage_configuration():
    """Check the storage configuration."""
    logger.info("\nChecking storage configuration:")
    logger.info(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    logger.info(f"MEDIA_URL: {settings.MEDIA_URL}")
    logger.info(f"AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
    logger.info(f"AWS_S3_ENDPOINT_URL: {settings.AWS_S3_ENDPOINT_URL}")
    logger.info(f"AWS_DEFAULT_ACL: {settings.AWS_DEFAULT_ACL}")
    logger.info(f"AWS_QUERYSTRING_AUTH: {settings.AWS_QUERYSTRING_AUTH}")

if __name__ == "__main__":
    print("EduMore360 Image URL Checker")
    print("============================")
    
    # Check storage configuration
    check_storage_configuration()
    
    # Check hero section images
    check_hero_section_images()
    
    # Check theme images
    check_theme_images()
