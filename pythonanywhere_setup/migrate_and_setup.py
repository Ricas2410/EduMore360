#!/usr/bin/env python
"""
🗃️ EduMore360 Database Setup Script for PythonAnywhere
This script sets up the database, creates admin user, and loads sample data
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings_pythonanywhere')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import transaction
from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from subscription.models import SubscriptionPlan
from core.models import SystemConfiguration

def print_status(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def run_migrations():
    """Run database migrations"""
    print_info("Running database migrations...")
    
    try:
        # Make migrations
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Apply migrations
        execute_from_command_line(['manage.py', 'migrate'])
        
        print_status("Database migrations completed successfully")
        return True
    except Exception as e:
        print_error(f"Migration failed: {str(e)}")
        return False

def create_superuser():
    """Create admin superuser"""
    print_info("Creating admin superuser...")
    
    try:
        User = get_user_model()
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            print_info("Superuser already exists, skipping creation")
            return True
        
        # Create superuser
        admin_user = User.objects.create_user(
            email='admin@edumore360.com',
            password='admin123',  # Change this in production!
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        
        print_status("Admin superuser created successfully")
        print_info("Email: admin@edumore360.com")
        print_info("Password: admin123")
        print_info("⚠️  Please change the password after first login!")
        
        return True
    except Exception as e:
        print_error(f"Failed to create superuser: {str(e)}")
        return False

def setup_basic_curriculum():
    """Set up basic curriculum structure"""
    print_info("Setting up basic curriculum...")
    
    try:
        with transaction.atomic():
            # Create Ghana Education Service curriculum
            curriculum, created = Curriculum.objects.get_or_create(
                name="Ghana Education Service",
                defaults={
                    'code': 'GES',
                    'country': 'Ghana',
                    'description': 'Official Ghana Education Service Curriculum',
                    'is_active': True
                }
            )
            
            if created:
                print_status("Created Ghana Education Service curriculum")
            
            # Create class levels
            class_levels_data = [
                ('Primary 1', 1), ('Primary 2', 2), ('Primary 3', 3),
                ('Primary 4', 4), ('Primary 5', 5), ('Primary 6', 6),
                ('JHS 1', 7), ('JHS 2', 8), ('JHS 3', 9),
                ('SHS 1', 10), ('SHS 2', 11), ('SHS 3', 12)
            ]
            
            for name, order in class_levels_data:
                class_level, created = ClassLevel.objects.get_or_create(
                    name=name,
                    curriculum=curriculum,
                    defaults={
                        'level_order': order,
                        'is_active': True
                    }
                )
                if created:
                    print_status(f"Created class level: {name}")
            
            # Create basic subjects for Primary 5 and 6
            subjects_data = [
                'Mathematics', 'English Language', 'Science', 
                'Social Studies', 'ICT', 'Creative Arts'
            ]
            
            primary_5 = ClassLevel.objects.get(name='Primary 5', curriculum=curriculum)
            primary_6 = ClassLevel.objects.get(name='Primary 6', curriculum=curriculum)
            
            for subject_name in subjects_data:
                # Create for Primary 5
                subject_p5, created = Subject.objects.get_or_create(
                    name=subject_name,
                    curriculum=curriculum,
                    class_level=primary_5,
                    defaults={'is_active': True}
                )
                if created:
                    print_status(f"Created subject: {subject_name} for Primary 5")
                
                # Create for Primary 6
                subject_p6, created = Subject.objects.get_or_create(
                    name=subject_name,
                    curriculum=curriculum,
                    class_level=primary_6,
                    defaults={'is_active': True}
                )
                if created:
                    print_status(f"Created subject: {subject_name} for Primary 6")
        
        print_status("Basic curriculum setup completed")
        return True
        
    except Exception as e:
        print_error(f"Failed to setup curriculum: {str(e)}")
        return False

def setup_subscription_plans():
    """Set up subscription plans"""
    print_info("Setting up subscription plans...")
    
    try:
        plans_data = [
            {
                'name': 'Free Plan',
                'plan_type': 'free',
                'price': 0.00,
                'duration_days': 365,
                'features': ['Access to free quizzes', 'Basic progress tracking'],
                'is_active': True
            },
            {
                'name': 'Basic Plan',
                'plan_type': 'basic',
                'price': 10.00,
                'duration_days': 30,
                'features': ['All free features', 'Premium quizzes', 'Detailed analytics'],
                'is_active': True
            },
            {
                'name': 'Premium Plan',
                'plan_type': 'premium',
                'price': 25.00,
                'duration_days': 30,
                'features': ['All basic features', 'Unlimited access', 'Priority support'],
                'is_active': True
            }
        ]
        
        for plan_data in plans_data:
            plan, created = SubscriptionPlan.objects.get_or_create(
                plan_type=plan_data['plan_type'],
                defaults=plan_data
            )
            if created:
                print_status(f"Created subscription plan: {plan_data['name']}")
        
        print_status("Subscription plans setup completed")
        return True
        
    except Exception as e:
        print_error(f"Failed to setup subscription plans: {str(e)}")
        return False

def setup_system_configuration():
    """Set up system configuration"""
    print_info("Setting up system configuration...")
    
    try:
        config, created = SystemConfiguration.objects.get_or_create(
            defaults={
                'site_name': 'EduMore360',
                'site_description': 'Ghana\'s Premier Educational Platform',
                'maintenance_mode': False,
                'quiz_show_immediate_feedback': True,
                'quiz_randomize_questions': True,
                'quiz_randomize_choices': True,
                'quiz_feedback_time': 3,
                'session_timeout_minutes': 60,
                'enforce_single_session': False,
                'currency': 'GHS'
            }
        )
        
        if created:
            print_status("System configuration created")
        else:
            print_info("System configuration already exists")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to setup system configuration: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 Starting EduMore360 Database Setup...")
    print("=" * 50)
    
    success = True
    
    # Run migrations
    if not run_migrations():
        success = False
    
    # Create superuser
    if not create_superuser():
        success = False
    
    # Setup curriculum
    if not setup_basic_curriculum():
        success = False
    
    # Setup subscription plans
    if not setup_subscription_plans():
        success = False
    
    # Setup system configuration
    if not setup_system_configuration():
        success = False
    
    print("=" * 50)
    
    if success:
        print("🎉 Database setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Login to admin: /my-admin/")
        print("2. Change admin password")
        print("3. Add quiz questions")
        print("4. Test the platform")
        print("\n🌟 Your EduMore360 platform is ready!")
    else:
        print("❌ Database setup completed with errors")
        print("Please check the error messages above and fix any issues")
    
    return success

if __name__ == '__main__':
    main()
