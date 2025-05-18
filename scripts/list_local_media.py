"""
Script to list all files in the local media directory.
Run this script with: python scripts/list_local_media.py
"""

import os
import sys
import django
from pathlib import Path

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.conf import settings

def list_local_media():
    """List all files in the local media directory."""
    media_root = settings.MEDIA_ROOT
    
    if not os.path.exists(media_root):
        print(f"Media directory {media_root} does not exist")
        return
    
    print(f"\nListing files in {media_root}:")
    print("-" * 80)
    
    total_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk(media_root):
        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, media_root)
            size = os.path.getsize(file_path)
            
            print(f"{rel_path:<70} {size:<10} bytes")
            
            total_files += 1
            total_size += size
    
    print("-" * 80)
    print(f"Total: {total_files} files, {total_size} bytes")

if __name__ == "__main__":
    print("EduMore360 Local Media Listing")
    print("==============================")
    
    list_local_media()
