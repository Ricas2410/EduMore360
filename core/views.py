from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Q

from .models import Notification, UserAchievement, HeroSection, KidFriendlyTheme
from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from quiz.models import QuizAttempt


def home(request):
    """Home page view."""
    # Get featured content for the home page
    curricula = Curriculum.objects.filter(is_active=True)

    # Get hero sections for the home page
    hero_sections = HeroSection.get_for_position('home')

    # Determine appropriate audience based on user if logged in
    audience = 'all'
    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'grade') and user.grade:
            if 1 <= user.grade <= 5:
                audience = 'elementary'
            elif 6 <= user.grade <= 8:
                audience = 'middle'
            elif 9 <= user.grade <= 12:
                audience = 'high'
        elif hasattr(user, 'is_parent') and user.is_parent:
            audience = 'parents'
        elif hasattr(user, 'is_teacher') and user.is_teacher:
            audience = 'teachers'

    # Filter hero sections by audience
    hero_sections = HeroSection.get_for_position('home', audience)

    # Get appropriate theme
    theme = None
    if request.user.is_authenticated and hasattr(request.user, 'grade') and request.user.grade:
        theme = KidFriendlyTheme.get_theme_for_grade(request.user.grade)
    else:
        theme = KidFriendlyTheme.objects.filter(is_default=True, is_active=True).first()

    context = {
        'curricula': curricula,
        'hero_sections': hero_sections,
        'theme': theme,
    }
    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    """User dashboard view."""
    user = request.user

    # Get user's preferred curriculum and class level
    curriculum = user.preferred_curriculum
    class_level = user.preferred_class_level

    # If user has no preferences, use defaults
    if not curriculum:
        curriculum = Curriculum.objects.filter(is_active=True).first()

    if not class_level and curriculum:
        class_level = ClassLevel.objects.filter(curriculum=curriculum, is_active=True).first()

    # Get user's active subscription
    from subscription.models import Subscription, CurriculumAccess, SubscriptionPlan
    from django.utils import timezone

    active_subscription = Subscription.objects.filter(
        user=user,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    # Check if the user needs to complete setup (free user without curriculum/class selection)
    needs_setup = False
    if active_subscription and active_subscription.plan.plan_type == 'free':
        # Check if the user has selected a curriculum and class level
        if not user.preferred_curriculum or not user.preferred_class_level:
            needs_setup = True

        # Check if the subscription has a curriculum access
        if not CurriculumAccess.objects.filter(subscription=active_subscription).exists():
            needs_setup = True

    # Get all curricula for tier three users
    all_curricula = []
    if active_subscription and active_subscription.plan.all_curriculums:
        all_curricula = Curriculum.objects.filter(is_active=True)

    # Get class levels for tier two users
    class_levels = []
    if active_subscription and active_subscription.plan.all_grade_levels and curriculum:
        class_levels = ClassLevel.objects.filter(curriculum=curriculum, is_active=True).order_by('level_order')

    # Get free tier curriculum and class level
    free_curriculum = None
    free_class_level = None

    if not active_subscription or active_subscription.plan.plan_type == 'free':
        # Find a free subscription to determine what's available in free tier
        from subscription.models import SubscriptionPlan
        free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
        if free_plan:
            # Find a sample curriculum access for the free tier
            sample_access = CurriculumAccess.objects.filter(
                subscription__plan=free_plan
            ).first()

            if sample_access:
                free_curriculum = sample_access.curriculum
                free_class_level = sample_access.class_level

    # Get recent activity
    recent_activity = user.get_recent_activity(limit=5)

    # Get unread notifications
    unread_notifications = Notification.objects.filter(user=user, is_read=False)[:5]

    # Get user achievements
    recent_achievements = UserAchievement.objects.filter(user=user).order_by('-earned_at')[:5]

    # Get user's quiz statistics
    quiz_stats = user.get_quiz_stats()

    # Get user's study progress
    study_progress = user.get_study_progress()

    # Get recommended content based on user's activity and progress
    if curriculum and class_level:
        # Check if user has access to this curriculum and class level based on subscription
        has_access = False

        # Staff and superusers have access to everything
        if user.is_staff or user.is_superuser:
            has_access = True
        # Check subscription-based access
        elif active_subscription:
            # Tier three has access to all curricula
            if active_subscription.plan.all_curriculums:
                has_access = True
            # Tier two has access to all grade levels of selected curriculum
            elif active_subscription.plan.all_grade_levels:
                # Check if user has access to this curriculum
                curriculum_accesses = active_subscription.curriculum_accesses.filter(curriculum=curriculum)
                has_access = curriculum_accesses.exists()
            # Tier one has access to specific curriculum and class level
            else:
                # Check if user has access to this specific curriculum and class level
                has_access = active_subscription.curriculum_accesses.filter(
                    curriculum=curriculum,
                    class_level=class_level
                ).exists()
        # Free tier users have access to free content
        elif free_curriculum and free_class_level:
            has_access = (curriculum.id == free_curriculum.id and class_level.id == free_class_level.id)

        # Get subjects the user has started but not completed
        in_progress_topics = []
        if has_access:
            for topic_progress in study_progress['topics']:
                if 0 < topic_progress['progress_percentage'] < 100:
                    in_progress_topics.append(topic_progress['topic'])

            # If there are in-progress topics, recommend those first
            if in_progress_topics:
                recommended_subjects = list(set([topic.subject for topic in in_progress_topics]))
            else:
                # Otherwise, recommend subjects based on curriculum and class level
                recommended_subjects = Subject.objects.filter(
                    curriculum=curriculum,
                    class_level=class_level,
                    is_active=True
                ).order_by('name')
        else:
            # User doesn't have access to this curriculum/class level
            # Show free content instead
            if free_curriculum and free_class_level:
                recommended_subjects = Subject.objects.filter(
                    curriculum=free_curriculum,
                    class_level=free_class_level,
                    is_active=True
                ).order_by('name')
            else:
                recommended_subjects = []
    else:
        recommended_subjects = []

    # Determine appropriate audience based on user
    audience = 'all'
    if hasattr(user, 'grade') and user.grade:
        if 1 <= user.grade <= 5:
            audience = 'elementary'
        elif 6 <= user.grade <= 8:
            audience = 'middle'
        elif 9 <= user.grade <= 12:
            audience = 'high'
    elif hasattr(user, 'is_parent') and user.is_parent:
        audience = 'parents'
    elif hasattr(user, 'is_teacher') and user.is_teacher:
        audience = 'teachers'

    # Get hero sections for the dashboard
    hero_sections = HeroSection.get_for_position('dashboard', audience)

    # Get appropriate theme
    theme = None
    if hasattr(user, 'grade') and user.grade:
        theme = KidFriendlyTheme.get_theme_for_grade(user.grade)
    else:
        theme = KidFriendlyTheme.objects.filter(is_default=True, is_active=True).first()

    # Get all available curricula and class levels for setup
    all_available_curricula = Curriculum.objects.filter(is_active=True)
    all_available_class_levels = {}
    for curr in all_available_curricula:
        all_available_class_levels[curr.id] = ClassLevel.objects.filter(
            curriculum=curr,
            is_active=True
        ).order_by('level_order')

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'recent_activity': recent_activity,
        'unread_notifications': unread_notifications,
        'recent_achievements': recent_achievements,
        'recommended_subjects': recommended_subjects,
        'hero_sections': hero_sections,
        'theme': theme,
        'audience': audience,
        'quiz_stats': quiz_stats,
        'study_progress': study_progress,
        'active_subscription': active_subscription,
        'all_curricula': all_curricula,
        'class_levels': class_levels,
        'free_curriculum': free_curriculum,
        'free_class_level': free_class_level,
        'needs_setup': needs_setup,
        'all_available_curricula': all_available_curricula,
        'all_available_class_levels': all_available_class_levels,
    }
    return render(request, 'core/dashboard.html', context)


def about(request):
    """About page view."""
    return render(request, 'core/about.html')


def contact(request):
    """Contact page view."""
    return render(request, 'core/contact.html')


def privacy_policy(request):
    """Privacy policy page view."""
    return render(request, 'core/privacy_policy.html')


def terms_of_service(request):
    """Terms of service page view."""
    return render(request, 'core/terms_of_service.html')


def faq(request):
    """FAQ page view."""
    # In a real application, these would come from a database
    # For now, we'll create some dummy data

    # Get query parameters
    category_slug = request.GET.get('category', '')
    search_query = request.GET.get('q', '')

    # Create dummy FAQ categories
    categories = [
        {'id': 1, 'name': 'General', 'slug': 'general'},
        {'id': 2, 'name': 'Subscription', 'slug': 'subscription'},
        {'id': 3, 'name': 'Content', 'slug': 'content'},
        {'id': 4, 'name': 'Quiz', 'slug': 'quiz'},
        {'id': 5, 'name': 'Technical', 'slug': 'technical'},
    ]

    # Create comprehensive FAQs
    all_faqs = [
        # Subscription FAQs
        {
            'id': 1,
            'question': 'What subscription plans do you offer?',
            'answer': '<p>We offer four subscription tiers to meet different needs:</p><ul><li><strong>Free Tier:</strong> Limited access to one curriculum and one grade level.</li><li><strong>Tier One (Monthly/Yearly):</strong> Access to one curriculum and one grade level of your choice for $4.99/month.</li><li><strong>Tier Two (Monthly/Yearly):</strong> Access to one curriculum with all grade levels, share with up to 5 family members for $9.99/month.</li><li><strong>Tier Three (Monthly/Yearly):</strong> Access to all curriculums and all grade levels, share with up to 5 family members for $19.99/month.</li></ul>',
            'category': {'id': 2, 'name': 'Subscription', 'slug': 'subscription'},
            'related_faqs': {'exists': True, 'all': [2, 3, 4]}
        },
        {
            'id': 2,
            'question': 'How do I cancel my subscription?',
            'answer': '<p>You can cancel your subscription at any time from your account settings:</p><ol><li>Log in to your EduMore360 account</li><li>Go to "Manage Subscription" in your account menu</li><li>Click on "Cancel Subscription"</li><li>Follow the prompts to confirm cancellation</li></ol><p>Your access will continue until the end of your current billing period. You can continue using EduMore360 with the free tier after your paid subscription ends.</p>',
            'category': {'id': 2, 'name': 'Subscription', 'slug': 'subscription'},
            'related_faqs': {'exists': True, 'all': [1, 3, 4]}
        },
        {
            'id': 3,
            'question': 'What payment methods do you accept?',
            'answer': '<p>We accept the following payment methods:</p><ul><li>Credit/Debit Cards (Visa, Mastercard, American Express)</li><li>PayPal</li><li>Mobile Money (for Ghana and select countries)</li><li>Bank Transfer (for institutional subscriptions)</li></ul><p>All payments are processed securely through our payment partners.</p>',
            'category': {'id': 2, 'name': 'Subscription', 'slug': 'subscription'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 4,
            'question': 'Is there a refund policy?',
            'answer': '<p>Yes, we offer a 7-day money-back guarantee for new subscribers. If you\'re not satisfied with our service within the first 7 days of your subscription, you can request a full refund by contacting our support team.</p><p>For subscriptions beyond the 7-day period, refunds are handled on a case-by-case basis. Please contact our support team with your specific situation.</p>',
            'category': {'id': 2, 'name': 'Subscription', 'slug': 'subscription'},
            'related_faqs': {'exists': False, 'all': []}
        },

        # Content FAQs
        {
            'id': 5,
            'question': 'What curricula do you support?',
            'answer': '<p>We support various curricula including:</p><ul><li>Ghana Curriculum (Primary, JHS, SHS)</li><li>Nigerian Curriculum (Primary, JSS, SSS)</li><li>Cambridge International Curriculum</li><li>International Baccalaureate (IB)</li><li>West African Senior School Certificate Examination (WASSCE)</li><li>More curricula are being added regularly</li></ul><p>Our content is aligned with these educational standards to ensure relevance and accuracy for students in different educational systems.</p>',
            'category': {'id': 3, 'name': 'Content', 'slug': 'content'},
            'related_faqs': {'exists': True, 'all': [6, 7, 8]}
        },
        {
            'id': 6,
            'question': 'How often is new content added?',
            'answer': '<p>We regularly update and add new content to our platform:</p><ul><li>Core subjects are updated at least once per term/semester</li><li>New topics and subjects are added monthly</li><li>Quiz questions are refreshed weekly</li><li>Special content for exam preparation is added seasonally</li></ul><p>We also respond to curriculum changes and updates from educational authorities to ensure our content remains current and accurate.</p>',
            'category': {'id': 3, 'name': 'Content', 'slug': 'content'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 7,
            'question': 'Can I download content for offline use?',
            'answer': '<p>Yes, paid subscribers can download certain content for offline use:</p><ul><li>Study notes can be downloaded as PDFs</li><li>Practice worksheets are available for download and printing</li><li>Some educational resources can be saved for offline access</li></ul><p>However, interactive quizzes and certain multimedia content require an internet connection to function properly. Downloaded content is for personal use only and subject to our terms of service.</p>',
            'category': {'id': 3, 'name': 'Content', 'slug': 'content'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 8,
            'question': 'How do I request new content?',
            'answer': '<p>We welcome content requests from our users. To request new content:</p><ol><li>Log in to your account</li><li>Go to the "Contact Us" page</li><li>Select "Content Request" from the dropdown menu</li><li>Provide details about the content you\'d like to see (curriculum, subject, topic, etc.)</li><li>Submit your request</li></ol><p>Our content team reviews all requests and prioritizes them based on demand and feasibility. While we can\'t guarantee all requests will be fulfilled, we value your input in helping us improve our platform.</p>',
            'category': {'id': 3, 'name': 'Content', 'slug': 'content'},
            'related_faqs': {'exists': False, 'all': []}
        },

        # Quiz FAQs
        {
            'id': 9,
            'question': 'How are quizzes graded?',
            'answer': '<p>Quizzes are automatically graded based on correct answers:</p><ul><li>Multiple-choice questions are checked against the correct option</li><li>Short-answer questions use pattern matching to evaluate responses</li><li>Each question is typically worth one point unless otherwise specified</li><li>Your final score is calculated as a percentage of correct answers</li><li>Passing score is typically 70% but may vary by quiz</li></ul><p>Detailed feedback is provided after each question to help you understand the correct answer.</p>',
            'category': {'id': 4, 'name': 'Quiz', 'slug': 'quiz'},
            'related_faqs': {'exists': True, 'all': [10, 11, 12]}
        },
        {
            'id': 10,
            'question': 'Can I retake quizzes?',
            'answer': '<p>Yes, you can retake quizzes as many times as you want. This is a great way to practice and reinforce your learning.</p><p>Each time you retake a quiz:</p><ul><li>Questions may be randomized to provide a fresh experience</li><li>Your previous scores are saved in your history</li><li>You can track your improvement over time</li></ul><p>We encourage students to retake quizzes until they achieve mastery of the subject matter.</p>',
            'category': {'id': 4, 'name': 'Quiz', 'slug': 'quiz'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 11,
            'question': 'Are there time limits for quizzes?',
            'answer': '<p>Yes, most quizzes have time limits to simulate exam conditions:</p><ul><li>Standard quizzes typically allow 30 seconds per question</li><li>Practice exams have time limits that match the actual exam format</li><li>A countdown timer is displayed during timed quizzes</li><li>Questions automatically advance when the time limit is reached</li></ul><p>The time limit helps students develop time management skills for actual exams. However, some study quizzes may not have time limits to allow for more relaxed learning.</p>',
            'category': {'id': 4, 'name': 'Quiz', 'slug': 'quiz'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 12,
            'question': 'How do I view my quiz history?',
            'answer': '<p>To view your quiz history and track your progress:</p><ol><li>Log in to your account</li><li>Click on "Quiz History" in the navigation menu or from your dashboard</li><li>View a list of all quizzes you\'ve taken, sorted by date</li><li>Click on any quiz to see detailed results, including:</li><ul><li>Your score and percentage</li><li>Time taken</li><li>Questions answered correctly/incorrectly</li><li>Explanations for correct answers</li></ul></ol><p>Your quiz history helps you identify areas where you\'ve improved and topics that may need more study.</p>',
            'category': {'id': 4, 'name': 'Quiz', 'slug': 'quiz'},
            'related_faqs': {'exists': False, 'all': []}
        },

        # Technical FAQs
        {
            'id': 13,
            'question': 'What devices are supported?',
            'answer': '<p>EduMore360 works on most modern devices:</p><ul><li><strong>Computers:</strong> Windows, Mac, and Linux operating systems</li><li><strong>Mobile Devices:</strong> iOS and Android smartphones and tablets</li><li><strong>Browsers:</strong> Chrome, Firefox, Safari, and Edge (latest versions recommended)</li></ul><p>Our platform is responsive and adapts to different screen sizes, making it accessible on various devices. For the best experience, we recommend using an updated browser and a stable internet connection.</p>',
            'category': {'id': 5, 'name': 'Technical', 'slug': 'technical'},
            'related_faqs': {'exists': True, 'all': [14, 15, 16]}
        },
        {
            'id': 14,
            'question': 'How do I reset my password?',
            'answer': '<p>To reset your password:</p><ol><li>Go to the login page</li><li>Click on "Forgot Password" or "Reset Password"</li><li>Enter the email address associated with your account</li><li>Check your email for a password reset link</li><li>Click the link and follow the instructions to create a new password</li><li>Log in with your new password</li></ol><p>If you don\'t receive the reset email, check your spam folder or contact our support team for assistance.</p>',
            'category': {'id': 5, 'name': 'Technical', 'slug': 'technical'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 15,
            'question': 'Is my data secure?',
            'answer': '<p>Yes, we take data security very seriously:</p><ul><li>All data is encrypted in transit using SSL/TLS</li><li>Personal information is stored securely and protected</li><li>We do not sell or share your personal data with third parties</li><li>Regular security audits and updates are performed</li><li>We comply with relevant data protection regulations</li></ul><p>For more details on how we handle your data, please refer to our <a href="/privacy-policy/">Privacy Policy</a>.</p>',
            'category': {'id': 5, 'name': 'Technical', 'slug': 'technical'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 16,
            'question': 'How do I report a technical issue?',
            'answer': '<p>If you encounter any technical issues:</p><ol><li>Go to the "Contact Us" page</li><li>Select "Technical Support" from the dropdown menu</li><li>Describe the issue in detail, including:</li><ul><li>What you were trying to do</li><li>What device and browser you were using</li><li>Any error messages you received</li><li>Screenshots if possible</li></ul><li>Submit your report</li></ol><p>Our technical team will investigate and respond as soon as possible. For urgent issues, you can also email us directly at support@edumore360.com.</p>',
            'category': {'id': 5, 'name': 'Technical', 'slug': 'technical'},
            'related_faqs': {'exists': False, 'all': []}
        },

        # General FAQs
        {
            'id': 17,
            'question': 'What is EduMore360?',
            'answer': '<p>EduMore360 is a comprehensive online learning platform designed to support students in their educational journey. We provide:</p><ul><li>Curriculum-aligned study materials and notes</li><li>Interactive quizzes and assessments</li><li>Progress tracking and performance analytics</li><li>Personalized learning recommendations</li></ul><p>Our mission is to make quality education accessible to students everywhere, with a focus on African curricula and international standards.</p>',
            'category': {'id': 1, 'name': 'General', 'slug': 'general'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 18,
            'question': 'How do I get started with EduMore360?',
            'answer': '<p>Getting started with EduMore360 is easy:</p><ol><li>Create a free account on our website</li><li>Select your curriculum and grade level</li><li>Explore available subjects and topics</li><li>Start with the free content to get familiar with the platform</li><li>Upgrade to a paid subscription for full access when ready</li></ol><p>Our free tier allows you to experience the platform before committing to a subscription, giving you access to sample notes and quizzes for one curriculum and grade level.</p>',
            'category': {'id': 1, 'name': 'General', 'slug': 'general'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 19,
            'question': 'Can parents monitor their child\'s progress?',
            'answer': '<p>Yes, parents can monitor their child\'s progress in several ways:</p><ul><li>Family accounts allow parents to link to their children\'s accounts</li><li>Progress reports show performance across subjects and topics</li><li>Quiz results and study history are visible to linked parent accounts</li><li>Parents can receive email notifications about significant achievements</li></ul><p>This monitoring helps parents stay involved in their child\'s education and provide support where needed.</p>',
            'category': {'id': 1, 'name': 'General', 'slug': 'general'},
            'related_faqs': {'exists': False, 'all': []}
        },
        {
            'id': 20,
            'question': 'Is EduMore360 suitable for homeschooling?',
            'answer': '<p>Absolutely! EduMore360 is an excellent resource for homeschooling families:</p><ul><li>Our curriculum-aligned content helps ensure comprehensive coverage</li><li>Structured learning paths guide progression through subjects</li><li>Quizzes and assessments provide objective evaluation</li><li>Progress tracking helps document learning achievements</li><li>Multiple grade levels allow for personalized pacing</li></ul><p>Many homeschooling families use EduMore360 as a core resource or as a supplement to their existing curriculum.</p>',
            'category': {'id': 1, 'name': 'General', 'slug': 'general'},
            'related_faqs': {'exists': False, 'all': []}
        }
    ]

    # Filter FAQs by category if specified
    if category_slug:
        faqs = [faq for faq in all_faqs if faq['category']['slug'] == category_slug]
    else:
        faqs = all_faqs

    # Filter FAQs by search query if specified
    if search_query:
        faqs = [faq for faq in faqs if search_query.lower() in faq['question'].lower() or search_query.lower() in faq['answer'].lower()]

    context = {
        'categories': categories,
        'faqs': faqs,
        'category': category_slug,
        'search_query': search_query,
    }

    return render(request, 'core/faq.html', context)


@login_required
def notification_list(request):
    """View for listing all user notifications."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'notifications': notifications,
    }
    return render(request, 'core/notification_list.html', context)


@login_required
def mark_notification_read(request, pk):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()

    # Return JSON response for AJAX requests
    if request.headers.get('HX-Request') or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('core:notification_list')


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read."""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)

    # Return JSON response for AJAX requests
    if request.headers.get('HX-Request') or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    messages.success(request, 'All notifications marked as read.')
    return redirect('core:notification_list')


@login_required
def delete_notification(request, pk):
    """Delete a notification."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()

    # Return JSON response for AJAX requests
    if request.headers.get('HX-Request') or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    messages.success(request, 'Notification deleted successfully.')
    return redirect('core:notification_list')


@login_required
def achievement_list(request):
    """View for listing all user achievements."""
    achievements = UserAchievement.objects.filter(user=request.user).order_by('-earned_at')

    # Group achievements by type
    achievement_types = {}
    for achievement in achievements:
        achievement_type = achievement.get_achievement_type_display()
        if achievement_type not in achievement_types:
            achievement_types[achievement_type] = []
        achievement_types[achievement_type].append(achievement)

    context = {
        'achievement_types': achievement_types,
        'total_points': sum(a.points for a in achievements),
    }
    return render(request, 'core/achievement_list.html', context)


@login_required
def complete_free_setup(request):
    """View for free users to complete their setup by selecting a curriculum and class level."""
    from subscription.models import Subscription, CurriculumAccess
    from django.utils import timezone

    # Get user's active subscription
    active_subscription = Subscription.objects.filter(
        user=request.user,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    # Verify this is a free subscription
    if not active_subscription or active_subscription.plan.plan_type != 'free':
        messages.error(request, "This setup is only for free tier users.")
        return redirect('core:dashboard')

    if request.method == 'POST':
        curriculum_id = request.POST.get('curriculum')
        class_level_id = request.POST.get('class_level')

        if not curriculum_id or not class_level_id:
            messages.error(request, "Please select both a curriculum and a class level.")
            return redirect('core:complete_free_setup')

        try:
            # Get the curriculum and class level
            curriculum = Curriculum.objects.get(id=curriculum_id, is_active=True)
            class_level = ClassLevel.objects.get(id=class_level_id, curriculum=curriculum, is_active=True)

            # Update user preferences
            user = request.user
            user.preferred_curriculum = curriculum
            user.preferred_class_level = class_level
            user.save()

            # Create or update curriculum access for the subscription
            CurriculumAccess.objects.update_or_create(
                subscription=active_subscription,
                defaults={
                    'curriculum': curriculum,
                    'class_level': class_level
                }
            )

            messages.success(request, f"Setup complete! You now have access to {curriculum.name} - {class_level.name}.")
            return redirect('core:dashboard')

        except (Curriculum.DoesNotExist, ClassLevel.DoesNotExist):
            messages.error(request, "Invalid curriculum or class level selected.")
            return redirect('core:complete_free_setup')

    # GET request - show the form
    curricula = Curriculum.objects.filter(is_active=True)

    context = {
        'curricula': curricula,
        'subscription': active_subscription,
    }
    return render(request, 'core/complete_free_setup.html', context)
