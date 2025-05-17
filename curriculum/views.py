from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Curriculum, ClassLevel, Subject, Branch, Topic, SubTopic, Note


def curriculum_list(request):
    """View for listing all available curricula."""
    curricula = Curriculum.objects.filter(is_active=True)

    # If user is authenticated, filter curricula based on subscription
    if request.user.is_authenticated:
        # Staff and superusers see everything
        if request.user.is_staff or request.user.is_superuser:
            pass  # No filtering needed
        else:
            # Get user's active subscription
            from subscription.models import Subscription
            from django.utils import timezone

            active_subscription = Subscription.objects.filter(
                user=request.user,
                status='active',
                end_date__gt=timezone.now()
            ).first()

            if active_subscription:
                # If tier three, show all curricula
                if active_subscription.plan.all_curriculums:
                    pass  # No filtering needed
                else:
                    # Get the curricula the user has access to
                    accessible_curricula_ids = active_subscription.curriculum_accesses.values_list('curriculum_id', flat=True)
                    curricula = curricula.filter(id__in=accessible_curricula_ids)
            else:
                # No active subscription, show only free tier curriculum
                from subscription.models import SubscriptionPlan, CurriculumAccess

                # Find a free subscription to determine what's available in free tier
                free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
                if free_plan:
                    # Find a sample curriculum access for the free tier
                    sample_access = CurriculumAccess.objects.filter(
                        subscription__plan=free_plan
                    ).first()

                    if sample_access:
                        free_curriculum = sample_access.curriculum
                        curricula = curricula.filter(id=free_curriculum.id)
                    else:
                        curricula = curricula.none()  # No free curriculum defined
                else:
                    curricula = curricula.none()  # No free plan defined

    context = {
        'curricula': curricula,
    }
    return render(request, 'curriculum/curriculum_list.html', context)


def class_level_list(request, curriculum_code):
    """View for listing all class levels for a specific curriculum."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_levels = ClassLevel.objects.filter(curriculum=curriculum, is_active=True).order_by('level_order')

    # If user is authenticated, filter class levels based on subscription
    if request.user.is_authenticated:
        # Staff and superusers see everything
        if request.user.is_staff or request.user.is_superuser:
            pass  # No filtering needed
        else:
            # Get user's active subscription
            from subscription.models import Subscription
            from django.utils import timezone

            active_subscription = Subscription.objects.filter(
                user=request.user,
                status='active',
                end_date__gt=timezone.now()
            ).first()

            if active_subscription:
                # If tier three or tier two, show all class levels for this curriculum
                if active_subscription.plan.all_curriculums or active_subscription.plan.all_grade_levels:
                    # Check if user has access to this curriculum
                    if active_subscription.has_access_to_curriculum(curriculum):
                        pass  # No filtering needed
                    else:
                        class_levels = class_levels.none()  # No access to this curriculum
                else:
                    # Get the class levels the user has access to
                    accessible_class_level_ids = active_subscription.curriculum_accesses.filter(
                        curriculum=curriculum
                    ).values_list('class_level_id', flat=True)
                    class_levels = class_levels.filter(id__in=accessible_class_level_ids)
            else:
                # No active subscription, show only free tier class level
                from subscription.models import SubscriptionPlan, CurriculumAccess

                # Find a free subscription to determine what's available in free tier
                free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
                if free_plan:
                    # Find a sample curriculum access for the free tier
                    sample_access = CurriculumAccess.objects.filter(
                        subscription__plan=free_plan,
                        curriculum=curriculum
                    ).first()

                    if sample_access and sample_access.class_level:
                        free_class_level = sample_access.class_level
                        class_levels = class_levels.filter(id=free_class_level.id)
                    else:
                        class_levels = class_levels.none()  # No free class level defined
                else:
                    class_levels = class_levels.none()  # No free plan defined

    context = {
        'curriculum': curriculum,
        'class_levels': class_levels,
    }
    return render(request, 'curriculum/class_level_list.html', context)


def subject_list(request, curriculum_code, class_level_id):
    """View for listing all subjects for a specific class level."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subjects = Subject.objects.filter(curriculum=curriculum, class_level=class_level, is_active=True).order_by('name')

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subjects': subjects,
    }
    return render(request, 'curriculum/subject_list.html', context)


def subject_detail(request, curriculum_code, class_level_id, subject_slug):
    """View for showing details of a specific subject."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)

    # Get branches if any
    branches = Branch.objects.filter(subject=subject, is_active=True).order_by('name')

    # Get topics that don't belong to any branch
    topics = Topic.objects.filter(subject=subject, branch=None, is_active=True).order_by('order', 'name')

    # Get quizzes for this subject
    from quiz.models import Quiz
    quizzes = Quiz.objects.filter(
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        is_active=True
    )[:5]  # Limit to 5 quizzes for the sidebar

    # Get user progress if authenticated
    progress = None
    completed_topics = 0
    total_topics = topics.count()

    if request.user.is_authenticated:
        from core.models import UserProgress
        progress = UserProgress.objects.filter(
            user=request.user,
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            subtopic=None
        ).first()

        # Count completed topics
        if progress:
            completed_topics = UserProgress.objects.filter(
                user=request.user,
                curriculum=curriculum,
                class_level=class_level,
                subject=subject,
                topic__isnull=False
            ).count()

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'branches': branches,
        'topics': topics,
        'quizzes': quizzes,
        'progress': progress,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
    }
    return render(request, 'curriculum/subject_detail.html', context)


def branch_detail(request, curriculum_code, class_level_id, subject_slug, branch_slug):
    """View for showing details of a specific branch."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    branch = get_object_or_404(Branch, slug=branch_slug, subject=subject, is_active=True)

    # Get topics for this branch
    topics = Topic.objects.filter(subject=subject, branch=branch, is_active=True).order_by('order', 'name')

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'branch': branch,
        'topics': topics,
    }
    return render(request, 'curriculum/branch_detail.html', context)


def topic_detail(request, curriculum_code, class_level_id, subject_slug, topic_slug):
    """View for showing details of a specific topic (without branch)."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, branch=None, is_active=True)

    # Get subtopics if any
    subtopics = SubTopic.objects.filter(topic=topic, is_active=True).order_by('order', 'name')

    # Get notes directly associated with this topic (not with subtopics)
    notes = Note.objects.filter(topic=topic, subtopic=None, is_published=True).order_by('-updated_at')

    # Get quizzes for this topic
    from quiz.models import Quiz
    quizzes = Quiz.objects.filter(
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        topic=topic,
        is_active=True
    )[:5]  # Limit to 5 quizzes for the sidebar

    # Get previous and next topics for navigation
    prev_topic = Topic.objects.filter(
        subject=subject,
        branch=None,
        order__lt=topic.order,
        is_active=True
    ).order_by('-order').first()

    next_topic = Topic.objects.filter(
        subject=subject,
        branch=None,
        order__gt=topic.order,
        is_active=True
    ).order_by('order').first()

    # Get user progress if authenticated
    progress = None
    if request.user.is_authenticated:
        from core.models import UserProgress
        progress = UserProgress.objects.filter(
            user=request.user,
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            topic=topic,
            subtopic=None
        ).first()

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topic': topic,
        'subtopics': subtopics,
        'notes': notes,
        'quizzes': quizzes,
        'prev_topic': prev_topic,
        'next_topic': next_topic,
        'progress': progress,
    }
    return render(request, 'curriculum/topic_detail_simplified.html', context)


def branch_topic_detail(request, curriculum_code, class_level_id, subject_slug, branch_slug, topic_slug):
    """View for showing details of a specific topic (with branch)."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    branch = get_object_or_404(Branch, slug=branch_slug, subject=subject, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, branch=branch, is_active=True)

    # Get subtopics if any
    subtopics = SubTopic.objects.filter(topic=topic, is_active=True).order_by('order', 'name')

    # Get notes directly associated with this topic (not with subtopics)
    notes = Note.objects.filter(topic=topic, subtopic=None, is_published=True).order_by('-updated_at')

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'branch': branch,
        'topic': topic,
        'subtopics': subtopics,
        'notes': notes,
    }
    return render(request, 'curriculum/branch_topic_detail_simplified.html', context)


def subtopic_detail(request, curriculum_code, class_level_id, subject_slug, topic_slug, subtopic_slug):
    """View for showing details of a specific subtopic (without branch)."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, branch=None, is_active=True)
    subtopic = get_object_or_404(SubTopic, slug=subtopic_slug, topic=topic, is_active=True)

    # Get notes associated with this subtopic
    notes = Note.objects.filter(topic=topic, subtopic=subtopic, is_published=True).order_by('-updated_at')

    # Get quizzes for this topic
    from quiz.models import Quiz
    quizzes = Quiz.objects.filter(
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        topic=topic,
        is_active=True
    )[:5]  # Limit to 5 quizzes for the sidebar

    # Get next and previous subtopics for navigation
    next_subtopic = SubTopic.objects.filter(
        topic=topic,
        order__gt=subtopic.order,
        is_active=True
    ).order_by('order').first()

    prev_subtopic = SubTopic.objects.filter(
        topic=topic,
        order__lt=subtopic.order,
        is_active=True
    ).order_by('-order').first()

    # Get user progress if authenticated
    progress = None
    if request.user.is_authenticated:
        from core.models import UserProgress
        progress = UserProgress.objects.filter(
            user=request.user,
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            topic=topic,
            subtopic=subtopic
        ).first()

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topic': topic,
        'subtopic': subtopic,
        'notes': notes,
        'quizzes': quizzes,
        'next_subtopic': next_subtopic,
        'prev_subtopic': prev_subtopic,
        'progress': progress,
    }
    return render(request, 'curriculum/subtopic_detail.html', context)


def note_detail(request, curriculum_code, class_level_id, subject_slug, topic_slug, note_slug):
    """View for showing a specific note (without subtopic)."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, is_active=True)
    note = get_object_or_404(Note, slug=note_slug, topic=topic, subtopic=None, is_published=True)

    # Check if premium content is accessible
    if note.is_premium and not request.user.is_authenticated:
        return render(request, 'curriculum/premium_content.html', {'note': note})

    if note.is_premium and not request.user.is_premium:
        return render(request, 'curriculum/premium_content.html', {'note': note})

    # Get attachments for this note
    attachments = note.attachments.all()

    # Get quizzes for this topic
    from quiz.models import Quiz
    quizzes = Quiz.objects.filter(
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        topic=topic,
        is_active=True
    )[:5]  # Limit to 5 quizzes for the sidebar

    # Get next and previous notes for navigation
    next_note = Note.objects.filter(
        topic=topic,
        subtopic=None,
        order__gt=note.order,
        is_published=True
    ).order_by('order').first()

    prev_note = Note.objects.filter(
        topic=topic,
        subtopic=None,
        order__lt=note.order,
        is_published=True
    ).order_by('-order').first()

    # Update user progress if authenticated
    progress = None
    if request.user.is_authenticated:
        from core.models import UserProgress
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            topic=topic,
            subtopic=None
        )
        progress.notes_viewed.add(note)
        progress.update_activity()

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topic': topic,
        'note': note,
        'attachments': attachments,
        'quizzes': quizzes,
        'next_note': next_note,
        'prev_note': prev_note,
        'progress': progress,
    }
    return render(request, 'curriculum/note_detail.html', context)


def subtopic_note_detail(request, curriculum_code, class_level_id, subject_slug, topic_slug, subtopic_slug, note_slug):
    """View for showing a specific note (with subtopic)."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, is_active=True)
    subtopic = get_object_or_404(SubTopic, slug=subtopic_slug, topic=topic, is_active=True)
    note = get_object_or_404(Note, slug=note_slug, topic=topic, subtopic=subtopic, is_published=True)

    # Check if premium content is accessible
    if note.is_premium and not request.user.is_authenticated:
        return render(request, 'curriculum/premium_content.html', {'note': note})

    if note.is_premium and not request.user.is_premium:
        return render(request, 'curriculum/premium_content.html', {'note': note})

    # Get attachments for this note
    attachments = note.attachments.all()

    # Get quizzes for this topic
    from quiz.models import Quiz
    quizzes = Quiz.objects.filter(
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        topic=topic,
        is_active=True
    )[:5]  # Limit to 5 quizzes for the sidebar

    # Get next and previous notes for navigation
    next_note = Note.objects.filter(
        topic=topic,
        subtopic=subtopic,
        order__gt=note.order,
        is_published=True
    ).order_by('order').first()

    prev_note = Note.objects.filter(
        topic=topic,
        subtopic=subtopic,
        order__lt=note.order,
        is_published=True
    ).order_by('-order').first()

    # Update user progress if authenticated
    progress = None
    if request.user.is_authenticated:
        from core.models import UserProgress
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            topic=topic,
            subtopic=subtopic
        )
        progress.notes_viewed.add(note)
        progress.update_activity()

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topic': topic,
        'subtopic': subtopic,
        'note': note,
        'attachments': attachments,
        'quizzes': quizzes,
        'next_note': next_note,
        'prev_note': prev_note,
        'progress': progress,
    }
    return render(request, 'curriculum/subtopic_note_detail.html', context)


@login_required
def mark_topic_started(request, topic_id):
    """Mark a topic as started for the current user."""
    from django.http import HttpResponse
    from django.template.loader import render_to_string

    topic = get_object_or_404(Topic, id=topic_id, is_active=True)

    # Get curriculum, class level, and subject
    subject = topic.subject
    class_level = subject.class_level
    curriculum = subject.curriculum

    # Create or update user progress
    if request.user.is_authenticated:
        from core.models import UserProgress
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            topic=topic,
            subtopic=None
        )
        progress.update_activity()

        # Render the updated progress card
        context = {
            'progress': progress,
            'topic': topic,
            'curriculum': curriculum,
            'class_level': class_level,
            'subject': subject,
        }
        html = render_to_string('curriculum/partials/progress_card.html', context, request)
        return HttpResponse(html)

    return HttpResponse("You must be logged in to track progress.")


@login_required
def mark_subtopic_started(request, subtopic_id):
    """Mark a subtopic as started for the current user."""
    from django.http import HttpResponse
    from django.template.loader import render_to_string

    subtopic = get_object_or_404(SubTopic, id=subtopic_id, is_active=True)
    topic = subtopic.topic

    # Get curriculum, class level, and subject
    subject = topic.subject
    class_level = subject.class_level
    curriculum = subject.curriculum

    # Create or update user progress
    if request.user.is_authenticated:
        from core.models import UserProgress
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            topic=topic,
            subtopic=subtopic
        )
        progress.update_activity()

        # Render the updated progress card
        context = {
            'progress': progress,
            'topic': topic,
            'subtopic': subtopic,
            'curriculum': curriculum,
            'class_level': class_level,
            'subject': subject,
        }
        html = render_to_string('curriculum/partials/progress_card.html', context, request)
        return HttpResponse(html)

    return HttpResponse("You must be logged in to track progress.")
