"""
Context processors for the core app.
"""
from django.conf import settings
from core.models import Notification


def notifications(request):
    """
    Context processor that adds unread notification count to all templates.
    """
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    return {
        'unread_notifications_count': unread_notifications_count
    }


def seo_context(request):
    """
    Add SEO-related context variables to all templates.
    """
    path = request.path

    # Default SEO values
    seo_data = {
        'site_name': 'EduMore360',
        'site_description': 'Interactive learning platform offering comprehensive educational resources for students of all ages.',
        'site_keywords': 'education, online learning, courses, quizzes, interactive learning, e-learning, educational platform',
        'canonical_url': request.build_absolute_uri(),
        'og_type': 'website',
    }

    # Path-specific SEO values
    if path == '/':
        seo_data.update({
            'page_title': 'EduMore360 - Interactive Learning Platform',
            'page_description': 'EduMore360 is an interactive learning platform offering comprehensive educational resources for students of all ages. Explore courses, quizzes, and personalized learning paths.',
            'page_keywords': 'education, online learning, courses, quizzes, interactive learning, e-learning, educational platform',
        })
    elif '/curriculum/' in path:
        seo_data.update({
            'page_title': 'Courses & Curriculum - EduMore360',
            'page_description': 'Explore our comprehensive curriculum and courses designed to enhance your learning experience. Find courses in various subjects tailored to different learning levels.',
            'page_keywords': 'courses, curriculum, online courses, learning paths, educational content, subjects, lessons',
            'og_type': 'article',
        })
    elif '/quiz/' in path:
        seo_data.update({
            'page_title': 'Interactive Quizzes - EduMore360',
            'page_description': 'Test your knowledge with our interactive quizzes. Enhance your learning through engaging assessments and immediate feedback.',
            'page_keywords': 'quizzes, assessments, tests, interactive quizzes, knowledge testing, learning evaluation',
            'og_type': 'article',
        })
    elif '/subscription/' in path:
        seo_data.update({
            'page_title': 'Subscription Plans - EduMore360',
            'page_description': 'Choose the perfect subscription plan for your educational journey. Access premium content and features to enhance your learning experience.',
            'page_keywords': 'subscription, plans, pricing, premium content, membership, educational subscription',
        })
    elif '/accounts/' in path:
        seo_data.update({
            'page_title': 'Account Management - EduMore360',
            'page_description': 'Manage your EduMore360 account. Access your profile, track your progress, and customize your learning experience.',
            'page_keywords': 'account, profile, user account, learning progress, student profile',
        })
    else:
        # Default for other pages
        seo_data.update({
            'page_title': 'EduMore360 - Interactive Learning Platform',
            'page_description': seo_data['site_description'],
            'page_keywords': seo_data['site_keywords'],
        })

    return seo_data
