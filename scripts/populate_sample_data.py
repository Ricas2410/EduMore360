import os
import sys
import django
import random
from datetime import timedelta

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction

from curriculum.models import (
    Curriculum, ClassLevel, Subject, Branch,
    Topic, SubTopic, Note, Attachment
)
from quiz.models import (
    Question, QuestionChoice, ShortAnswer,
    Quiz, QuizAttempt, QuestionAttempt
)
from subscription.models import SubscriptionPlan, Subscription, Payment, CurriculumAccess
from core.models import SystemConfiguration, Notification, UserProgress, UserAchievement

User = get_user_model()

def create_admin_user():
    """Create an admin user if it doesn't exist."""
    if not User.objects.filter(email='admin@edumore360.com').exists():
        admin = User.objects.create_superuser(
            email='admin@edumore360.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User'
        )
        print("Admin user created.")
        return admin
    else:
        print("Admin user already exists.")
        return User.objects.get(email='admin@edumore360.com')

def create_test_users():
    """Create test users if they don't exist."""
    test_users = []

    if not User.objects.filter(email='student@edumore360.com').exists():
        student = User.objects.create_user(
            email='student@edumore360.com',
            password='studentpassword',
            first_name='Student',
            last_name='User',
            is_active=True
        )
        test_users.append(student)
        print("Student user created.")
    else:
        student = User.objects.get(email='student@edumore360.com')
        test_users.append(student)
        print("Student user already exists.")

    if not User.objects.filter(email='teacher@edumore360.com').exists():
        teacher = User.objects.create_user(
            email='teacher@edumore360.com',
            password='teacherpassword',
            first_name='Teacher',
            last_name='User',
            is_active=True,
            is_staff=True
        )
        test_users.append(teacher)
        print("Teacher user created.")
    else:
        teacher = User.objects.get(email='teacher@edumore360.com')
        test_users.append(teacher)
        print("Teacher user already exists.")

    return test_users

def create_curricula():
    """Create sample curricula."""
    curricula = []

    # US Curriculum
    us_curriculum, created = Curriculum.objects.get_or_create(
        name='US Curriculum',
        code='US',
        defaults={
            'description': 'Standard US K-12 curriculum covering all major subjects.',
            'is_active': True
        }
    )
    curricula.append(us_curriculum)
    if created:
        print("US Curriculum created.")
    else:
        print("US Curriculum already exists.")

    # Ghana Curriculum
    ghana_curriculum, created = Curriculum.objects.get_or_create(
        name='Ghana Curriculum',
        code='GH',
        defaults={
            'description': 'Ghana educational curriculum for primary and secondary education.',
            'is_active': True
        }
    )
    curricula.append(ghana_curriculum)
    if created:
        print("Ghana Curriculum created.")
    else:
        print("Ghana Curriculum already exists.")

    return curricula

def create_class_levels(curricula):
    """Create sample class levels for each curriculum."""
    class_levels = []

    # US Class Levels
    us_curriculum = curricula[0]
    us_levels = [
        {'name': 'Kindergarten', 'level_order': 0},
        {'name': 'Grade 1', 'level_order': 1},
        {'name': 'Grade 2', 'level_order': 2},
        {'name': 'Grade 3', 'level_order': 3},
        {'name': 'Grade 4', 'level_order': 4},
        {'name': 'Grade 5', 'level_order': 5},
        {'name': 'Grade 6', 'level_order': 6},
        {'name': 'Grade 7', 'level_order': 7},
        {'name': 'Grade 8', 'level_order': 8},
        {'name': 'Grade 9', 'level_order': 9},
        {'name': 'Grade 10', 'level_order': 10},
        {'name': 'Grade 11', 'level_order': 11},
        {'name': 'Grade 12', 'level_order': 12},
    ]

    for level_data in us_levels:
        level, created = ClassLevel.objects.get_or_create(
            curriculum=us_curriculum,
            level_order=level_data['level_order'],
            defaults={
                'name': level_data['name'],
                'description': f"{level_data['name']} curriculum for US education system.",
                'is_active': True
            }
        )
        class_levels.append(level)
        if created:
            print(f"{level.name} created.")
        else:
            print(f"{level.name} already exists.")

    # Ghana Class Levels
    ghana_curriculum = curricula[1]
    ghana_levels = [
        {'name': 'Primary 1', 'level_order': 1},
        {'name': 'Primary 2', 'level_order': 2},
        {'name': 'Primary 3', 'level_order': 3},
        {'name': 'Primary 4', 'level_order': 4},
        {'name': 'Primary 5', 'level_order': 5},
        {'name': 'Primary 6', 'level_order': 6},
        {'name': 'JHS 1', 'level_order': 7},
        {'name': 'JHS 2', 'level_order': 8},
        {'name': 'JHS 3', 'level_order': 9},
        {'name': 'SHS 1', 'level_order': 10},
        {'name': 'SHS 2', 'level_order': 11},
        {'name': 'SHS 3', 'level_order': 12},
    ]

    for level_data in ghana_levels:
        level, created = ClassLevel.objects.get_or_create(
            curriculum=ghana_curriculum,
            level_order=level_data['level_order'],
            defaults={
                'name': level_data['name'],
                'description': f"{level_data['name']} curriculum for Ghana education system.",
                'is_active': True
            }
        )
        class_levels.append(level)
        if created:
            print(f"{level.name} created.")
        else:
            print(f"{level.name} already exists.")

    return class_levels

def create_subjects(class_levels):
    """Create sample subjects for each class level."""
    subjects = []

    # Common subjects for both curricula
    common_subjects = [
        {'name': 'Mathematics', 'description': 'Study of numbers, quantities, and shapes.'},
        {'name': 'English', 'description': 'Study of English language, literature, and communication.'},
        {'name': 'Science', 'description': 'Study of the natural world through observation and experiment.'},
        {'name': 'Social Studies', 'description': 'Study of human society and social relationships.'},
    ]

    for class_level in class_levels:
        for subject_data in common_subjects:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                curriculum=class_level.curriculum,
                class_level=class_level,
                defaults={
                    'description': subject_data['description'],
                    'is_active': True
                }
            )
            subjects.append(subject)
            if created:
                print(f"{subject.name} for {class_level.name} created.")
            else:
                print(f"{subject.name} for {class_level.name} already exists.")

    return subjects

def create_branches(subjects):
    """Create sample branches for Science subject."""
    branches = []

    # Create branches for Science subjects
    science_subjects = [subject for subject in subjects if subject.name == 'Science']

    science_branches = [
        {'name': 'Biology', 'description': 'Study of living organisms and their interactions.'},
        {'name': 'Chemistry', 'description': 'Study of matter, its properties, and reactions.'},
        {'name': 'Physics', 'description': 'Study of matter, energy, and their interactions.'},
    ]

    for subject in science_subjects:
        for branch_data in science_branches:
            branch, created = Branch.objects.get_or_create(
                name=branch_data['name'],
                subject=subject,
                defaults={
                    'description': branch_data['description'],
                    'is_active': True
                }
            )
            branches.append(branch)
            if created:
                print(f"{branch.name} branch for {subject.name} ({subject.class_level.name}) created.")
            else:
                print(f"{branch.name} branch for {subject.name} ({subject.class_level.name}) already exists.")

    return branches

def create_subscription_plans():
    """Create subscription plans."""
    plans = []

    # Free plan
    free_plan, created = SubscriptionPlan.objects.get_or_create(
        plan_type='free',
        billing_cycle='monthly',
        defaults={
            'name': 'Free Tier',
            'description': 'Limited access to one curriculum and one grade level.',
            'price': 0.00,
            'features': '- Access to one curriculum and one grade level\n- Ad-supported experience\n- Basic progress tracking\n- Limited question attempts',
            'max_users': 1,
            'is_active': True,
            'all_curriculums': False,
            'all_grade_levels': False
        }
    )
    plans.append(free_plan)
    if created:
        print("Free Tier created.")
    else:
        print("Free Tier already exists.")

    # Tier One Monthly plan
    tier_one_monthly, created = SubscriptionPlan.objects.get_or_create(
        plan_type='tier_one',
        billing_cycle='monthly',
        defaults={
            'name': 'Tier One (Monthly)',
            'description': 'Access to one curriculum and one grade level of your choice.',
            'price': 4.99,
            'features': '- Choose one curriculum and one grade level\n- Ad-free experience\n- Comprehensive analytics and progress tracking\n- Unlimited question attempts\n- Downloadable content',
            'max_users': 1,
            'is_active': True,
            'all_curriculums': False,
            'all_grade_levels': False
        }
    )
    plans.append(tier_one_monthly)
    if created:
        print("Tier One Monthly Plan created.")
    else:
        print("Tier One Monthly Plan already exists.")

    # Tier One Yearly plan
    tier_one_yearly, created = SubscriptionPlan.objects.get_or_create(
        plan_type='tier_one',
        billing_cycle='yearly',
        defaults={
            'name': 'Tier One (Yearly)',
            'description': 'Access to one curriculum and one grade level of your choice with yearly billing.',
            'price': 49.99,
            'features': '- Choose one curriculum and one grade level\n- Ad-free experience\n- Comprehensive analytics and progress tracking\n- Unlimited question attempts\n- Downloadable content\n- 2 months free compared to monthly billing',
            'max_users': 1,
            'is_active': True,
            'all_curriculums': False,
            'all_grade_levels': False
        }
    )
    plans.append(tier_one_yearly)
    if created:
        print("Tier One Yearly Plan created.")
    else:
        print("Tier One Yearly Plan already exists.")

    # Tier Two Monthly plan
    tier_two_monthly, created = SubscriptionPlan.objects.get_or_create(
        plan_type='tier_two',
        billing_cycle='monthly',
        defaults={
            'name': 'Tier Two (Monthly)',
            'description': 'Access to one curriculum with all grade levels. Share with up to 5 family members.',
            'price': 9.99,
            'features': '- Choose one curriculum with all grade levels\n- Share with up to 5 family members\n- Ad-free experience\n- Comprehensive analytics and progress tracking\n- Unlimited question attempts\n- Downloadable content',
            'max_users': 5,
            'is_active': True,
            'all_curriculums': False,
            'all_grade_levels': True
        }
    )
    plans.append(tier_two_monthly)
    if created:
        print("Tier Two Monthly Plan created.")
    else:
        print("Tier Two Monthly Plan already exists.")

    # Tier Two Yearly plan
    tier_two_yearly, created = SubscriptionPlan.objects.get_or_create(
        plan_type='tier_two',
        billing_cycle='yearly',
        defaults={
            'name': 'Tier Two (Yearly)',
            'description': 'Access to one curriculum with all grade levels. Share with up to 5 family members. Yearly billing.',
            'price': 99.99,
            'features': '- Choose one curriculum with all grade levels\n- Share with up to 5 family members\n- Ad-free experience\n- Comprehensive analytics and progress tracking\n- Unlimited question attempts\n- Downloadable content\n- 2 months free compared to monthly billing',
            'max_users': 5,
            'is_active': True,
            'all_curriculums': False,
            'all_grade_levels': True
        }
    )
    plans.append(tier_two_yearly)
    if created:
        print("Tier Two Yearly Plan created.")
    else:
        print("Tier Two Yearly Plan already exists.")

    # Tier Three Monthly plan
    tier_three_monthly, created = SubscriptionPlan.objects.get_or_create(
        plan_type='tier_three',
        billing_cycle='monthly',
        defaults={
            'name': 'Tier Three (Monthly)',
            'description': 'Access to all curriculums and all grade levels. Share with up to 5 family members.',
            'price': 19.99,
            'features': '- Access to all curriculums and all grade levels\n- Share with up to 5 family members\n- Ad-free experience\n- Comprehensive analytics and progress tracking\n- Unlimited question attempts\n- Downloadable content',
            'max_users': 5,
            'is_active': True,
            'all_curriculums': True,
            'all_grade_levels': True
        }
    )
    plans.append(tier_three_monthly)
    if created:
        print("Tier Three Monthly Plan created.")
    else:
        print("Tier Three Monthly Plan already exists.")

    # Tier Three Yearly plan
    tier_three_yearly, created = SubscriptionPlan.objects.get_or_create(
        plan_type='tier_three',
        billing_cycle='yearly',
        defaults={
            'name': 'Tier Three (Yearly)',
            'description': 'Access to all curriculums and all grade levels. Share with up to 5 family members. Yearly billing.',
            'price': 199.99,
            'features': '- Access to all curriculums and all grade levels\n- Share with up to 5 family members\n- Ad-free experience\n- Comprehensive analytics and progress tracking\n- Unlimited question attempts\n- Downloadable content\n- 2 months free compared to monthly billing',
            'max_users': 5,
            'is_active': True,
            'all_curriculums': True,
            'all_grade_levels': True
        }
    )
    plans.append(tier_three_yearly)
    if created:
        print("Tier Three Yearly Plan created.")
    else:
        print("Tier Three Yearly Plan already exists.")

    return plans

def create_system_configuration():
    """Create system configuration."""
    config, created = SystemConfiguration.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'EduMore360',
            'site_description': 'Comprehensive educational platform for students from kindergarten through grade 12.',
            'maintenance_mode': False,
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_use_tls': True,
            'smtp_username': 'skillnetservices@gmail.com',
            'smtp_password': 'tdms ckdk tmgo fado',
            'default_from_email': 'skillnetservices@gmail.com',
            'enforce_single_session': False,
            'session_timeout_minutes': 30,
            'allow_registration': True,
            'require_email_verification': True,
            'enable_google_login': True,
            'currency': 'USD'
        }
    )

    if created:
        print("System configuration created.")
    else:
        print("System configuration already exists.")

    return config

def create_sample_subscriptions(users, plans, curricula, class_levels):
    """Create sample subscriptions for testing."""
    subscriptions = []

    # Get the student user
    student = next((user for user in users if user.email == 'student@edumore360.com'), None)
    if not student:
        print("Student user not found. Skipping subscription creation.")
        return subscriptions

    # Get the free plan
    free_plan = next((plan for plan in plans if plan.plan_type == 'free' and plan.billing_cycle == 'monthly'), None)

    # Get the tier one monthly plan
    tier_one_plan = next((plan for plan in plans if plan.plan_type == 'tier_one' and plan.billing_cycle == 'monthly'), None)

    # Get the tier two monthly plan
    tier_two_plan = next((plan for plan in plans if plan.plan_type == 'tier_two' and plan.billing_cycle == 'monthly'), None)

    # Get the tier three monthly plan
    tier_three_plan = next((plan for plan in plans if plan.plan_type == 'tier_three' and plan.billing_cycle == 'monthly'), None)

    # Get US curriculum and first class level
    us_curriculum = next((curr for curr in curricula if curr.code == 'US'), None)
    us_class_level = next((cl for cl in class_levels if cl.curriculum == us_curriculum), None) if us_curriculum else None

    # Get Ghana curriculum and first class level
    ghana_curriculum = next((curr for curr in curricula if curr.code == 'GH'), None)
    ghana_class_level = next((cl for cl in class_levels if cl.curriculum == ghana_curriculum), None) if ghana_curriculum else None

    if not (free_plan and us_curriculum and us_class_level):
        print("Required plans or curricula not found. Skipping subscription creation.")
        return subscriptions

    # Create a free subscription for the student
    start_date = timezone.now()
    end_date = start_date + timedelta(days=30)

    free_subscription, created = Subscription.objects.get_or_create(
        user=student,
        plan=free_plan,
        defaults={
            'status': 'active',
            'start_date': start_date,
            'end_date': end_date,
            'auto_renew': True
        }
    )
    subscriptions.append(free_subscription)

    if created:
        print(f"Free subscription created for {student.email}.")

        # Create curriculum access for the free subscription
        curriculum_access, created = CurriculumAccess.objects.get_or_create(
            subscription=free_subscription,
            curriculum=us_curriculum,
            class_level=us_class_level
        )

        if created:
            print(f"Curriculum access created for {student.email}: {us_curriculum.name} - {us_class_level.name}")
    else:
        print(f"Free subscription already exists for {student.email}.")

    # Create a teacher user with tier three access
    teacher = next((user for user in users if user.email == 'teacher@edumore360.com'), None)
    if teacher and tier_three_plan:
        tier_three_subscription, created = Subscription.objects.get_or_create(
            user=teacher,
            plan=tier_three_plan,
            defaults={
                'status': 'active',
                'start_date': start_date,
                'end_date': end_date,
                'auto_renew': True
            }
        )
        subscriptions.append(tier_three_subscription)

        if created:
            print(f"Tier Three subscription created for {teacher.email}.")
            # No need to create curriculum access as tier three has all_curriculums=True
        else:
            print(f"Tier Three subscription already exists for {teacher.email}.")

    return subscriptions


def main():
    """Main function to populate the database with sample data."""
    print("Starting to populate the database with sample data...")

    with transaction.atomic():
        # Create users
        admin = create_admin_user()
        test_users = create_test_users()

        # Create curricula and class levels
        curricula = create_curricula()
        class_levels = create_class_levels(curricula)

        # Create subjects and branches
        subjects = create_subjects(class_levels)
        branches = create_branches(subjects)

        # Create subscription plans
        plans = create_subscription_plans()

        # Create sample subscriptions
        subscriptions = create_sample_subscriptions(
            [admin] + test_users,
            plans,
            curricula,
            class_levels
        )

        # Create system configuration
        config = create_system_configuration()

    print("Sample data population completed successfully!")

if __name__ == "__main__":
    main()
