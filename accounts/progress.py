import json
from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator

from curriculum.models import Subject, Topic, Subtopic, Note
from quiz.models import Quiz, QuizAttempt
from core.models import Achievement, UserAchievement
from .models import UserActivity, ContentView, TimeSpent


@login_required
def progress_overview(request):
    """
    Display an overview of the user's learning progress.
    """
    # Get user's preferred subjects
    user_subjects = request.user.preferred_subjects.all()
    
    # If user has no preferred subjects, show all subjects
    if not user_subjects.exists():
        subjects = Subject.objects.all()
    else:
        subjects = user_subjects
    
    # Get subject progress data
    subject_progress = []
    for subject in subjects:
        # Get total topics for this subject
        total_topics = Topic.objects.filter(subject=subject).count()
        
        # Get viewed topics for this subject
        viewed_topics = ContentView.objects.filter(
            user=request.user,
            content_type='topic',
            content_id__in=Topic.objects.filter(subject=subject).values_list('id', flat=True)
        ).values('content_id').distinct().count()
        
        # Calculate completion percentage
        completion_percentage = (viewed_topics / total_topics * 100) if total_topics > 0 else 0
        
        # Get last activity for this subject
        last_activity = UserActivity.objects.filter(
            user=request.user,
            subject=subject
        ).order_by('-timestamp').first()
        
        subject_progress.append({
            'subject': subject,
            'total_topics': total_topics,
            'viewed_topics': viewed_topics,
            'completion_percentage': round(completion_percentage, 1),
            'last_activity': last_activity.timestamp if last_activity else None,
        })
    
    # Get quiz statistics
    quiz_attempts = QuizAttempt.objects.filter(user=request.user)
    completed_quizzes = quiz_attempts.filter(status='completed')
    
    total_quizzes = quiz_attempts.count()
    avg_score = completed_quizzes.aggregate(Avg('score'))['score__avg'] or 0
    
    # Get time spent statistics
    total_time_spent = TimeSpent.objects.filter(user=request.user).aggregate(Sum('seconds'))['seconds__sum'] or 0
    avg_time_per_session = total_time_spent / quiz_attempts.count() if quiz_attempts.count() > 0 else 0
    
    # Get achievement statistics
    total_achievements = UserAchievement.objects.filter(user=request.user).count()
    total_achievement_points = UserAchievement.objects.filter(user=request.user).aggregate(
        total_points=Sum('achievement__points')
    )['total_points'] or 0
    
    # Get recent activities
    recent_activities = UserActivity.objects.filter(
        user=request.user
    ).select_related(
        'subject'
    ).order_by('-timestamp')[:10]
    
    context = {
        'subject_progress': subject_progress,
        'total_quizzes': total_quizzes,
        'avg_score': round(avg_score, 1),
        'total_time_spent': format_time_spent(total_time_spent),
        'avg_time_per_session': format_time_spent(avg_time_per_session),
        'total_achievements': total_achievements,
        'total_achievement_points': total_achievement_points,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'accounts/progress_overview.html', context)


@login_required
def subject_progress(request, subject_slug):
    """
    Display detailed progress for a specific subject.
    """
    subject = get_object_or_404(Subject, slug=subject_slug)
    
    # Get all topics for this subject
    topics = Topic.objects.filter(subject=subject)
    
    # Get topic progress data
    topic_progress = []
    for topic in topics:
        # Get total subtopics for this topic
        total_subtopics = Subtopic.objects.filter(topic=topic).count()
        
        # Get viewed subtopics for this topic
        viewed_subtopics = ContentView.objects.filter(
            user=request.user,
            content_type='subtopic',
            content_id__in=Subtopic.objects.filter(topic=topic).values_list('id', flat=True)
        ).values('content_id').distinct().count()
        
        # Calculate completion percentage
        completion_percentage = (viewed_subtopics / total_subtopics * 100) if total_subtopics > 0 else 0
        
        # Check if topic has been viewed
        topic_viewed = ContentView.objects.filter(
            user=request.user,
            content_type='topic',
            content_id=topic.id
        ).exists()
        
        # Get last activity for this topic
        last_activity = UserActivity.objects.filter(
            user=request.user,
            topic=topic
        ).order_by('-timestamp').first()
        
        topic_progress.append({
            'topic': topic,
            'total_subtopics': total_subtopics,
            'viewed_subtopics': viewed_subtopics,
            'completion_percentage': round(completion_percentage, 1),
            'topic_viewed': topic_viewed,
            'last_activity': last_activity.timestamp if last_activity else None,
        })
    
    # Get quiz statistics for this subject
    subject_quizzes = Quiz.objects.filter(subject=subject)
    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user,
        quiz__in=subject_quizzes
    )
    completed_quizzes = quiz_attempts.filter(status='completed')
    
    total_quizzes = subject_quizzes.count()
    attempted_quizzes = quiz_attempts.values('quiz').distinct().count()
    avg_score = completed_quizzes.aggregate(Avg('score'))['score__avg'] or 0
    
    # Get time spent statistics for this subject
    total_time_spent = TimeSpent.objects.filter(
        user=request.user,
        subject=subject
    ).aggregate(Sum('seconds'))['seconds__sum'] or 0
    
    # Get recent activities for this subject
    recent_activities = UserActivity.objects.filter(
        user=request.user,
        subject=subject
    ).order_by('-timestamp')[:10]
    
    context = {
        'subject': subject,
        'topic_progress': topic_progress,
        'total_quizzes': total_quizzes,
        'attempted_quizzes': attempted_quizzes,
        'avg_score': round(avg_score, 1),
        'total_time_spent': format_time_spent(total_time_spent),
        'recent_activities': recent_activities,
    }
    
    return render(request, 'accounts/subject_progress.html', context)


@login_required
def topic_progress(request, subject_slug, topic_slug):
    """
    Display detailed progress for a specific topic.
    """
    subject = get_object_or_404(Subject, slug=subject_slug)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject)
    
    # Get all subtopics for this topic
    subtopics = Subtopic.objects.filter(topic=topic)
    
    # Get subtopic progress data
    subtopic_progress = []
    for subtopic in subtopics:
        # Get total notes for this subtopic
        total_notes = Note.objects.filter(subtopic=subtopic).count()
        
        # Get viewed notes for this subtopic
        viewed_notes = ContentView.objects.filter(
            user=request.user,
            content_type='note',
            content_id__in=Note.objects.filter(subtopic=subtopic).values_list('id', flat=True)
        ).values('content_id').distinct().count()
        
        # Calculate completion percentage
        completion_percentage = (viewed_notes / total_notes * 100) if total_notes > 0 else 0
        
        # Check if subtopic has been viewed
        subtopic_viewed = ContentView.objects.filter(
            user=request.user,
            content_type='subtopic',
            content_id=subtopic.id
        ).exists()
        
        # Get last activity for this subtopic
        last_activity = UserActivity.objects.filter(
            user=request.user,
            subtopic=subtopic
        ).order_by('-timestamp').first()
        
        subtopic_progress.append({
            'subtopic': subtopic,
            'total_notes': total_notes,
            'viewed_notes': viewed_notes,
            'completion_percentage': round(completion_percentage, 1),
            'subtopic_viewed': subtopic_viewed,
            'last_activity': last_activity.timestamp if last_activity else None,
        })
    
    # Get quiz statistics for this topic
    topic_quizzes = Quiz.objects.filter(topic=topic)
    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user,
        quiz__in=topic_quizzes
    )
    completed_quizzes = quiz_attempts.filter(status='completed')
    
    total_quizzes = topic_quizzes.count()
    attempted_quizzes = quiz_attempts.values('quiz').distinct().count()
    avg_score = completed_quizzes.aggregate(Avg('score'))['score__avg'] or 0
    
    # Get time spent statistics for this topic
    total_time_spent = TimeSpent.objects.filter(
        user=request.user,
        topic=topic
    ).aggregate(Sum('seconds'))['seconds__sum'] or 0
    
    # Get recent activities for this topic
    recent_activities = UserActivity.objects.filter(
        user=request.user,
        topic=topic
    ).order_by('-timestamp')[:10]
    
    context = {
        'subject': subject,
        'topic': topic,
        'subtopic_progress': subtopic_progress,
        'total_quizzes': total_quizzes,
        'attempted_quizzes': attempted_quizzes,
        'avg_score': round(avg_score, 1),
        'total_time_spent': format_time_spent(total_time_spent),
        'recent_activities': recent_activities,
    }
    
    return render(request, 'accounts/topic_progress.html', context)


@login_required
def activity_history(request):
    """
    Display the user's activity history.
    """
    # Get filter parameters
    subject_slug = request.GET.get('subject')
    activity_type = request.GET.get('type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Base queryset
    activities = UserActivity.objects.filter(user=request.user)
    
    # Apply filters
    if subject_slug:
        activities = activities.filter(subject__slug=subject_slug)
    
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            activities = activities.filter(timestamp__date__gte=date_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            activities = activities.filter(timestamp__date__lte=date_to)
        except ValueError:
            pass
    
    # Order by timestamp
    activities = activities.order_by('-timestamp')
    
    # Get all subjects for filter
    subjects = Subject.objects.all()
    
    # Get activity types for filter
    activity_types = UserActivity.objects.filter(
        user=request.user
    ).values_list('activity_type', flat=True).distinct()
    
    # Paginate results
    paginator = Paginator(activities, 20)
    page_number = request.GET.get('page', 1)
    activities_page = paginator.get_page(page_number)
    
    context = {
        'activities': activities_page,
        'subjects': subjects,
        'activity_types': activity_types,
        'selected_subject': subject_slug,
        'selected_type': activity_type,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'accounts/activity_history.html', context)


@login_required
@require_POST
def record_content_view(request):
    """
    Record a content view.
    """
    try:
        content_type = request.POST.get('content_type')
        content_id = request.POST.get('content_id')
        
        if not content_type or not content_id:
            return JsonResponse({'success': False, 'error': 'Missing content type or ID'}, status=400)
        
        # Record the content view
        ContentView.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            content_id=content_id
        )
        
        # Record user activity
        record_activity(request.user, content_type, content_id)
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def record_time_spent(request):
    """
    Record time spent on content.
    """
    try:
        content_type = request.POST.get('content_type')
        content_id = request.POST.get('content_id')
        seconds = int(request.POST.get('seconds', 0))
        
        if not content_type or not content_id or seconds <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid parameters'}, status=400)
        
        # Get content object and related objects
        subject = None
        topic = None
        subtopic = None
        
        if content_type == 'topic':
            topic = get_object_or_404(Topic, id=content_id)
            subject = topic.subject
        elif content_type == 'subtopic':
            subtopic = get_object_or_404(Subtopic, id=content_id)
            topic = subtopic.topic
            subject = topic.subject
        elif content_type == 'note':
            note = get_object_or_404(Note, id=content_id)
            subtopic = note.subtopic
            topic = subtopic.topic
            subject = topic.subject
        
        # Record time spent
        TimeSpent.objects.create(
            user=request.user,
            content_type=content_type,
            content_id=content_id,
            seconds=seconds,
            subject=subject,
            topic=topic,
            subtopic=subtopic
        )
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def record_activity(user, content_type, content_id):
    """
    Record user activity for a content view.
    """
    # Get content object and related objects
    subject = None
    topic = None
    subtopic = None
    activity_type = f"{content_type}_viewed"
    description = f"Viewed {content_type}"
    
    if content_type == 'topic':
        topic = get_object_or_404(Topic, id=content_id)
        subject = topic.subject
        description = f"Viewed topic: {topic.title}"
    elif content_type == 'subtopic':
        subtopic = get_object_or_404(Subtopic, id=content_id)
        topic = subtopic.topic
        subject = topic.subject
        description = f"Viewed subtopic: {subtopic.title}"
    elif content_type == 'note':
        note = get_object_or_404(Note, id=content_id)
        subtopic = note.subtopic
        topic = subtopic.topic
        subject = topic.subject
        description = f"Viewed note: {note.title}"
    
    # Record user activity
    UserActivity.objects.create(
        user=user,
        activity_type=activity_type,
        description=description,
        subject=subject,
        topic=topic,
        subtopic=subtopic,
        content_type=content_type,
        content_id=content_id
    )
    
    # Check for achievements
    check_content_achievements(user)


def check_content_achievements(user):
    """
    Check and award achievements based on content views.
    """
    # Get user's content views
    content_views = ContentView.objects.filter(user=user)
    
    # Achievement: First Content View
    if content_views.count() == 1:
        achievement = Achievement.objects.filter(code='first_content_view').first()
        if achievement:
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement
            )
    
    # Achievement: Content Explorer (View 50 content items)
    if content_views.count() == 50:
        achievement = Achievement.objects.filter(code='content_explorer').first()
        if achievement:
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement
            )
    
    # Achievement: Subject Completion (View all topics in a subject)
    subjects = Subject.objects.all()
    for subject in subjects:
        total_topics = Topic.objects.filter(subject=subject).count()
        viewed_topics = ContentView.objects.filter(
            user=user,
            content_type='topic',
            content_id__in=Topic.objects.filter(subject=subject).values_list('id', flat=True)
        ).values('content_id').distinct().count()
        
        if total_topics > 0 and viewed_topics == total_topics:
            achievement = Achievement.objects.filter(code='subject_completion').first()
            if achievement:
                UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement
                )


def format_time_spent(seconds):
    """
    Format time spent in seconds to a human-readable format.
    """
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes > 0:
            return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours != 1 else ''}"
