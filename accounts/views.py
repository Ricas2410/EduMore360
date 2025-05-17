from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.http import JsonResponse

from .models import User, UserGroup
from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from core.models import UserProgress, UserAchievement
from quiz.models import QuizAttempt


@login_required
def profile(request):
    """View for user profile."""
    user = request.user

    # Get user's quiz statistics
    quiz_attempts = QuizAttempt.objects.filter(user=user)
    total_quizzes = quiz_attempts.count()
    completed_quizzes = quiz_attempts.filter(status='completed').count()
    avg_score = quiz_attempts.filter(status='completed').aggregate(avg_score=Sum('score') / Count('id'))['avg_score'] or 0

    # Get user's achievements
    achievements = UserAchievement.objects.filter(user=user)
    total_achievements = achievements.count()
    total_points = achievements.aggregate(total=Sum('points'))['total'] or 0

    # Get user's subscription info
    from subscription.models import Subscription
    subscription = Subscription.objects.filter(
        user=user,
        status='active'
    ).first()

    context = {
        'user': user,
        'total_quizzes': total_quizzes,
        'completed_quizzes': completed_quizzes,
        'avg_score': round(avg_score, 1),
        'total_achievements': total_achievements,
        'total_points': total_points,
        'subscription': subscription,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """View for editing user profile."""
    user = request.user

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        bio = request.POST.get('bio')

        # Update user profile
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        # Check if email is changed and not already in use
        if email and email != user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use.")
            else:
                user.email = email

        user.phone_number = phone_number
        user.bio = bio

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('accounts:profile')

    context = {
        'user': user,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def change_password(request):
    """View for changing password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def preferences(request):
    """View for user preferences."""
    user = request.user

    # Get all available curricula
    curricula = Curriculum.objects.filter(is_active=True)

    # Get class levels for the user's preferred curriculum
    class_levels = []
    if user.preferred_curriculum:
        class_levels = ClassLevel.objects.filter(
            curriculum=user.preferred_curriculum,
            is_active=True
        ).order_by('level_order')

    context = {
        'user': user,
        'curricula': curricula,
        'class_levels': class_levels,
    }
    return render(request, 'accounts/preferences.html', context)


@login_required
def set_curriculum_preference(request):
    """View for setting curriculum preference."""
    if request.method == 'POST':
        curriculum_id = request.POST.get('curriculum')

        if curriculum_id:
            curriculum = get_object_or_404(Curriculum, id=curriculum_id, is_active=True)

            # Update user's preferred curriculum
            user = request.user
            user.preferred_curriculum = curriculum
            user.save()

            # Reset class level if it doesn't belong to the new curriculum
            if user.preferred_class_level and user.preferred_class_level.curriculum != curriculum:
                user.preferred_class_level = None
                user.save()

            messages.success(request, f"Curriculum preference set to {curriculum.name}.")

        return redirect('accounts:preferences')

    return redirect('accounts:preferences')


@login_required
def set_class_level_preference(request):
    """View for setting class level preference."""
    if request.method == 'POST':
        class_level_id = request.POST.get('class_level')

        if class_level_id:
            class_level = get_object_or_404(ClassLevel, id=class_level_id, is_active=True)

            # Update user's preferred class level
            user = request.user

            # Ensure the class level belongs to the user's preferred curriculum
            if not user.preferred_curriculum or class_level.curriculum != user.preferred_curriculum:
                messages.error(request, "The selected class level does not belong to your preferred curriculum.")
                return redirect('accounts:preferences')

            user.preferred_class_level = class_level
            user.save()

            messages.success(request, f"Class level preference set to {class_level.name}.")

        return redirect('accounts:preferences')

    return redirect('accounts:preferences')


@login_required
def progress_overview(request):
    """View for showing progress overview."""
    user = request.user

    # Get user's progress records
    progress_records = UserProgress.objects.filter(user=user)

    # Group progress by subject
    subjects = Subject.objects.filter(
        id__in=progress_records.values_list('subject', flat=True)
    ).distinct()

    subject_progress = []
    for subject in subjects:
        # Calculate overall completion percentage for this subject
        subject_records = progress_records.filter(subject=subject)
        if subject_records.exists():
            avg_completion = subject_records.aggregate(avg=Sum('completion_percentage') / Count('id'))['avg'] or 0
            subject_progress.append({
                'subject': subject,
                'completion_percentage': round(avg_completion),
                'last_activity': subject_records.order_by('-last_activity').first().last_activity,
            })

    # Sort by last activity
    subject_progress.sort(key=lambda x: x['last_activity'], reverse=True)

    # Get recent quiz attempts
    recent_quizzes = QuizAttempt.objects.filter(user=user).order_by('-started_at')[:5]

    context = {
        'subject_progress': subject_progress,
        'recent_quizzes': recent_quizzes,
    }
    return render(request, 'accounts/progress_overview.html', context)


@login_required
def subject_progress(request, subject_slug):
    """View for showing progress for a specific subject."""
    user = request.user
    subject = get_object_or_404(Subject, slug=subject_slug)

    # Get progress records for this subject
    progress_records = UserProgress.objects.filter(user=user, subject=subject)

    # Group progress by topic
    topics = Topic.objects.filter(
        id__in=progress_records.values_list('topic', flat=True)
    ).distinct()

    topic_progress = []
    for topic in topics:
        # Get progress record for this topic
        topic_record = progress_records.filter(topic=topic, subtopic=None).first()
        if topic_record:
            topic_progress.append({
                'topic': topic,
                'completion_percentage': topic_record.completion_percentage,
                'last_activity': topic_record.last_activity,
                'notes_viewed': topic_record.notes_viewed.count(),
            })

    # Sort by last activity
    topic_progress.sort(key=lambda x: x['last_activity'], reverse=True)

    # Get quiz attempts for this subject
    quiz_attempts = QuizAttempt.objects.filter(
        user=user,
        quiz__subject=subject
    ).order_by('-started_at')

    context = {
        'subject': subject,
        'topic_progress': topic_progress,
        'quiz_attempts': quiz_attempts,
    }
    return render(request, 'accounts/subject_progress.html', context)


@login_required
def topic_progress(request, topic_slug):
    """View for showing progress for a specific topic."""
    user = request.user
    topic = get_object_or_404(Topic, slug=topic_slug)

    # Get progress record for this topic
    topic_progress = UserProgress.objects.filter(user=user, topic=topic, subtopic=None).first()

    # Get progress records for subtopics
    subtopic_progress = []
    if topic.subtopics.exists():
        for subtopic in topic.subtopics.filter(is_active=True):
            progress = UserProgress.objects.filter(user=user, topic=topic, subtopic=subtopic).first()
            if progress:
                subtopic_progress.append({
                    'subtopic': subtopic,
                    'completion_percentage': progress.completion_percentage,
                    'last_activity': progress.last_activity,
                    'notes_viewed': progress.notes_viewed.count(),
                })

    # Sort by last activity
    subtopic_progress.sort(key=lambda x: x['last_activity'], reverse=True)

    # Get notes viewed for this topic
    notes_viewed = []
    if topic_progress:
        notes_viewed = topic_progress.notes_viewed.all()

    # Get quiz attempts for this topic
    quiz_attempts = QuizAttempt.objects.filter(
        user=user,
        quiz__topic=topic
    ).order_by('-started_at')

    context = {
        'topic': topic,
        'topic_progress': topic_progress,
        'subtopic_progress': subtopic_progress,
        'notes_viewed': notes_viewed,
        'quiz_attempts': quiz_attempts,
    }
    return render(request, 'accounts/topic_progress.html', context)


@login_required
def get_class_levels(request):
    """AJAX view for getting class levels for a curriculum."""
    curriculum_id = request.GET.get('curriculum')

    if not curriculum_id:
        return JsonResponse({'error': 'No curriculum selected'}, status=400)

    try:
        curriculum = Curriculum.objects.get(id=curriculum_id)
        class_levels = ClassLevel.objects.filter(
            curriculum=curriculum,
            is_active=True
        ).order_by('level_order')

        options_html = '<option value="">Select a class level</option>'
        for level in class_levels:
            options_html += f'<option value="{level.id}">{level.name}</option>'

        return JsonResponse({'html': options_html})
    except Curriculum.DoesNotExist:
        return JsonResponse({'error': 'Curriculum not found'}, status=404)


@login_required
def set_notification_preferences(request):
    """View for setting notification preferences."""
    if request.method == 'POST':
        user = request.user

        # Get notification preferences
        email_notifications = request.POST.get('email_notifications') == 'on'
        quiz_reminders = request.POST.get('quiz_reminders') == 'on'
        new_content_notifications = request.POST.get('new_content_notifications') == 'on'
        achievement_notifications = request.POST.get('achievement_notifications') == 'on'
        subscription_notifications = request.POST.get('subscription_notifications') == 'on'

        # Update user's notification preferences
        from core.models import NotificationPreferences

        # Get or create notification preferences
        notification_prefs, created = NotificationPreferences.objects.get_or_create(user=user)

        notification_prefs.email_notifications = email_notifications
        notification_prefs.quiz_reminders = quiz_reminders
        notification_prefs.new_content_notifications = new_content_notifications
        notification_prefs.achievement_notifications = achievement_notifications
        notification_prefs.subscription_notifications = subscription_notifications
        notification_prefs.save()

        messages.success(request, "Notification preferences updated successfully.")

    return redirect('accounts:preferences')


@login_required
def set_subject_preferences(request):
    """View for setting subject preferences."""
    if request.method == 'POST':
        user = request.user

        # Get selected subjects
        subject_ids = request.POST.getlist('subjects')

        if subject_ids:
            # Clear existing preferences
            user.preferred_subjects.clear()

            # Add new preferences
            subjects = Subject.objects.filter(id__in=subject_ids)
            user.preferred_subjects.add(*subjects)

            messages.success(request, "Subject preferences updated successfully.")
        else:
            # If no subjects selected, clear preferences
            user.preferred_subjects.clear()
            messages.info(request, "All subject preferences have been cleared.")

    return redirect('accounts:preferences')
