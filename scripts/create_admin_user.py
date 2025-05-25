#!/usr/bin/env python
"""
Script to create an admin user for testing the admin dashboard.
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin_user():
    """Create an admin user for testing."""
    email = "admin@edumore360.com"
    password = "admin123"
    
    # Check if admin user already exists
    if User.objects.filter(email=email).exists():
        print(f"✅ Admin user '{email}' already exists!")
        user = User.objects.get(email=email)
        if not user.is_staff:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"✅ Updated user '{email}' to admin status!")
    else:
        # Create new admin user
        user = User.objects.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        print(f"✅ Created admin user '{email}' successfully!")
    
    print(f"\n🔑 Admin Login Credentials:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"\n🌐 Admin Dashboard URL: http://127.0.0.1:8000/my-admin/")
    print(f"📊 Analytics Dashboard: http://127.0.0.1:8000/my-admin/analytics/")

if __name__ == "__main__":
    create_admin_user()
