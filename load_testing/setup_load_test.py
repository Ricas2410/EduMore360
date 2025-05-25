"""
Setup script for load testing EduMore360
Prepares the database and system for load testing
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.contrib.auth import get_user_model
from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from quiz.models import Quiz, Question
from subscription.models import SubscriptionPlan

User = get_user_model()

def setup_test_data():
    """Create test data for load testing"""
    print("🔧 Setting up test data for load testing...")
    
    # Create test curriculum if not exists
    curriculum, created = Curriculum.objects.get_or_create(
        name="Test Curriculum",
        defaults={
            'code': 'TEST',
            'country': 'Ghana',
            'description': 'Test curriculum for load testing',
            'is_active': True
        }
    )
    if created:
        print("✅ Created test curriculum")
    
    # Create test class level
    class_level, created = ClassLevel.objects.get_or_create(
        name="Test Class",
        curriculum=curriculum,
        defaults={
            'level_order': 1,
            'is_active': True
        }
    )
    if created:
        print("✅ Created test class level")
    
    # Create test subject
    subject, created = Subject.objects.get_or_create(
        name="Test Subject",
        curriculum=curriculum,
        class_level=class_level,
        defaults={
            'description': 'Test subject for load testing',
            'is_active': True
        }
    )
    if created:
        print("✅ Created test subject")
    
    # Create test topic
    topic, created = Topic.objects.get_or_create(
        name="Test Topic",
        subject=subject,
        defaults={
            'description': 'Test topic for load testing',
            'order': 1,
            'is_active': True
        }
    )
    if created:
        print("✅ Created test topic")
    
    # Create test quizzes
    for i in range(1, 11):  # Create 10 test quizzes
        quiz, created = Quiz.objects.get_or_create(
            title=f"Load Test Quiz {i}",
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            topic=topic,
            defaults={
                'description': f'Test quiz {i} for load testing',
                'time_limit': 30,
                'is_active': True,
                'show_results': True,
                'randomize_questions': True
            }
        )
        
        if created:
            # Create test questions for each quiz
            for j in range(1, 6):  # 5 questions per quiz
                Question.objects.create(
                    quiz=quiz,
                    question_text=f"Test question {j} for quiz {i}?",
                    choice_a=f"Option A for Q{j}",
                    choice_b=f"Option B for Q{j}",
                    choice_c=f"Option C for Q{j}",
                    choice_d=f"Option D for Q{j}",
                    correct_answer='A',
                    explanation=f"Explanation for question {j}",
                    order=j
                )
            print(f"✅ Created test quiz {i} with 5 questions")
    
    # Create subscription plans if not exist
    plans = [
        {'plan_type': 'free', 'name': 'Free Plan', 'price': 0},
        {'plan_type': 'basic', 'name': 'Basic Plan', 'price': 10},
        {'plan_type': 'premium', 'name': 'Premium Plan', 'price': 25},
    ]
    
    for plan_data in plans:
        plan, created = SubscriptionPlan.objects.get_or_create(
            plan_type=plan_data['plan_type'],
            defaults={
                'name': plan_data['name'],
                'price': plan_data['price'],
                'currency': 'USD',
                'duration_days': 30,
                'is_active': True
            }
        )
        if created:
            print(f"✅ Created {plan_data['name']}")
    
    print("🎉 Test data setup complete!")

def create_admin_user():
    """Create admin user for testing"""
    admin_email = "admin@edumore360.com"
    admin_password = "admin123test"
    
    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            email=admin_email,
            password=admin_password
        )
        print(f"✅ Created admin user: {admin_email} / {admin_password}")
    else:
        print(f"ℹ️ Admin user already exists: {admin_email}")

def optimize_database():
    """Optimize database for load testing"""
    print("🔧 Optimizing database for load testing...")
    
    from django.core.management import call_command
    
    # Collect static files
    call_command('collectstatic', '--noinput')
    print("✅ Collected static files")
    
    # Run migrations
    call_command('migrate')
    print("✅ Applied migrations")
    
    print("🎉 Database optimization complete!")

def check_system_requirements():
    """Check if system is ready for load testing"""
    print("🔍 Checking system requirements...")
    
    # Check database connection
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection working")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Check if we have test data
    quiz_count = Quiz.objects.count()
    if quiz_count < 5:
        print(f"⚠️ Only {quiz_count} quizzes found. Need at least 5 for testing.")
        return False
    else:
        print(f"✅ Found {quiz_count} quizzes for testing")
    
    # Check user model
    try:
        User.objects.count()
        print("✅ User model working")
    except Exception as e:
        print(f"❌ User model error: {e}")
        return False
    
    print("🎉 System requirements check passed!")
    return True

def main():
    """Main setup function"""
    print("🚀 EduMore360 Load Testing Setup")
    print("=" * 50)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements check failed. Please fix issues before testing.")
        return
    
    # Setup test data
    setup_test_data()
    
    # Create admin user
    create_admin_user()
    
    # Optimize database
    optimize_database()
    
    print("\n" + "=" * 50)
    print("🎉 Load testing setup complete!")
    print("\n📋 Next steps:")
    print("1. Install locust: pip install locust")
    print("2. Run load test: locust -f load_testing/locustfile.py --host=http://127.0.0.1:8000")
    print("3. Open browser: http://localhost:8089")
    print("4. Configure test: 2000 users, 100 spawn rate")
    print("\n⚠️ Important:")
    print("- Run this on a production-like environment")
    print("- Monitor CPU, memory, and database performance")
    print("- Test with your actual hosting provider")

if __name__ == "__main__":
    main()
