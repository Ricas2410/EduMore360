from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from curriculum.models import Curriculum, ClassLevel, Subject, Topic, Note, NoteCompletion
from .models import Quiz, Question, QuestionChoice, ShortAnswer, QuizAttempt, QuestionAttempt
from .services import QuestionRandomizer, QuizService
from .validators import ShortAnswerValidator


def quiz_home(request):
    """Home page for quizzes."""
    # Initialize variables
    curricula = None
    active_subscription = None
    free_plan = None
    sample_accesses = None
    is_tier_one = False  # Flag to identify Tier One users
    accessible_curricula_ids = []
    accessible_class_level_ids = []

    # Get user's subscription information
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Staff and superusers see all curricula
            curricula = Curriculum.objects.filter(is_active=True)
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
                # Check if this is a Tier One subscription (one curriculum, one class level)
                if active_subscription.plan.plan_type == 'tier_one':
                    is_tier_one = True
                    # Get the single curriculum and class level the user has access to
                    curriculum_access = active_subscription.curriculum_accesses.first()
                    if curriculum_access:
                        accessible_curricula_ids = [curriculum_access.curriculum_id]
                        accessible_class_level_ids = [curriculum_access.class_level_id]
                        curricula = Curriculum.objects.filter(id__in=accessible_curricula_ids, is_active=True)

                # If tier three, show all curricula
                elif active_subscription.plan.all_curriculums:
                    curricula = Curriculum.objects.filter(is_active=True)
                else:
                    # Get the curricula the user has access to
                    accessible_curricula_ids = list(active_subscription.curriculum_accesses.values_list('curriculum_id', flat=True).distinct())
                    accessible_class_level_ids = list(active_subscription.curriculum_accesses.values_list('class_level_id', flat=True).distinct())
                    curricula = Curriculum.objects.filter(id__in=accessible_curricula_ids, is_active=True)
            else:
                # No active subscription, show only free tier curricula
                from subscription.models import SubscriptionPlan, CurriculumAccess

                # Find a free subscription to determine what's available in free tier
                free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
                if free_plan:
                    # Find sample curriculum accesses for the free tier
                    sample_accesses = CurriculumAccess.objects.filter(
                        subscription__plan=free_plan
                    )

                    if sample_accesses.exists():
                        free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True).distinct()
                        accessible_curricula_ids = list(free_curriculum_ids)
                        accessible_class_level_ids = list(sample_accesses.values_list('class_level_id', flat=True).distinct())
                        curricula = Curriculum.objects.filter(id__in=free_curriculum_ids, is_active=True)

                        # Free tier is similar to Tier One (one curriculum, one class level)
                        is_tier_one = True
                    else:
                        curricula = Curriculum.objects.none()
                else:
                    curricula = Curriculum.objects.none()
    else:
        # Not authenticated, show only free tier curricula
        from subscription.models import SubscriptionPlan, CurriculumAccess

        # Find a free subscription to determine what's available in free tier
        free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
        if free_plan:
            # Find sample curriculum accesses for the free tier
            sample_accesses = CurriculumAccess.objects.filter(
                subscription__plan=free_plan
            )

            if sample_accesses.exists():
                free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True).distinct()
                accessible_curricula_ids = list(free_curriculum_ids)
                accessible_class_level_ids = list(sample_accesses.values_list('class_level_id', flat=True).distinct())
                curricula = Curriculum.objects.filter(id__in=free_curriculum_ids, is_active=True)

                # Free tier is similar to Tier One (one curriculum, one class level)
                is_tier_one = True
            else:
                curricula = Curriculum.objects.none()
        else:
            curricula = Curriculum.objects.none()

    # Get filter parameters
    selected_curriculum = request.GET.get('curriculum', '')
    selected_class_level = request.GET.get('class_level', '')
    selected_subject = request.GET.get('subject', '')
    selected_topic = request.GET.get('topic', '')

    # Initialize filter query
    quiz_filter = Q(is_active=True)

    # Apply filters if provided
    if selected_curriculum:
        quiz_filter &= Q(curriculum__code=selected_curriculum)

    if selected_class_level:
        quiz_filter &= Q(class_level_id=selected_class_level)

    if selected_subject:
        quiz_filter &= Q(subject__slug=selected_subject)

    if selected_topic:
        quiz_filter &= Q(topic__slug=selected_topic)

    # Get class levels, subjects, and topics based on selected filters
    class_levels = []
    subjects = []
    topics = []

    if selected_curriculum:
        class_levels = ClassLevel.objects.filter(curriculum__code=selected_curriculum, is_active=True).order_by('level_order')

    if selected_curriculum and selected_class_level:
        subjects = Subject.objects.filter(curriculum__code=selected_curriculum, class_level_id=selected_class_level, is_active=True).order_by('name')

    if selected_curriculum and selected_class_level and selected_subject:
        topics = Topic.objects.filter(subject__slug=selected_subject, subject__class_level_id=selected_class_level, subject__curriculum__code=selected_curriculum, is_active=True).order_by('order', 'name')

    # Filter quizzes based on user's subscription tier
    if request.user.is_authenticated:
        # Staff and superusers see all quizzes
        if request.user.is_staff or request.user.is_superuser:
            quizzes = Quiz.objects.filter(quiz_filter).order_by('-created_at')
            # Get featured quizzes if any, otherwise get the most recent quizzes
            featured_quizzes = Quiz.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:3]
            if not featured_quizzes.exists():
                featured_quizzes = Quiz.objects.filter(is_active=True).order_by('-created_at')[:3]
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
                # If tier three, show all quizzes
                if active_subscription.plan.all_curriculums:
                    quizzes = Quiz.objects.filter(quiz_filter).order_by('-created_at')
                    featured_quizzes = Quiz.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:3]
                else:
                    # Get the curricula and class levels the user has access to
                    accessible_curricula_ids = active_subscription.curriculum_accesses.values_list('curriculum_id', flat=True)
                    accessible_class_level_ids = active_subscription.curriculum_accesses.values_list('class_level_id', flat=True)

                    # Filter quizzes based on accessible curricula and class levels
                    quizzes = Quiz.objects.filter(
                        quiz_filter,
                        curriculum_id__in=accessible_curricula_ids,
                        class_level_id__in=accessible_class_level_ids
                    ).order_by('-created_at')

                    featured_quizzes = Quiz.objects.filter(
                        is_active=True,
                        is_featured=True,
                        curriculum_id__in=accessible_curricula_ids,
                        class_level_id__in=accessible_class_level_ids
                    ).order_by('-created_at')[:3]

                    if not featured_quizzes.exists():
                        featured_quizzes = Quiz.objects.filter(
                            is_active=True,
                            curriculum_id__in=accessible_curricula_ids,
                            class_level_id__in=accessible_class_level_ids
                        ).order_by('-created_at')[:3]
            else:
                # No active subscription, show only free tier quizzes
                from subscription.models import SubscriptionPlan, CurriculumAccess

                # Find a free subscription to determine what's available in free tier
                free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
                if free_plan:
                    # Find sample curriculum accesses for the free tier
                    sample_accesses = CurriculumAccess.objects.filter(
                        subscription__plan=free_plan
                    )

                    if sample_accesses.exists():
                        free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True).distinct()
                        free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True).distinct()

                        quizzes = Quiz.objects.filter(
                            quiz_filter,
                            curriculum_id__in=free_curriculum_ids,
                            class_level_id__in=free_class_level_ids
                        ).order_by('-created_at')

                        featured_quizzes = Quiz.objects.filter(
                            is_active=True,
                            is_featured=True,
                            curriculum_id__in=free_curriculum_ids,
                            class_level_id__in=free_class_level_ids
                        ).order_by('-created_at')[:3]

                        if not featured_quizzes.exists():
                            featured_quizzes = Quiz.objects.filter(
                                is_active=True,
                                curriculum_id__in=free_curriculum_ids,
                                class_level_id__in=free_class_level_ids
                            ).order_by('-created_at')[:3]
                    else:
                        quizzes = Quiz.objects.none()
                        featured_quizzes = Quiz.objects.none()
                else:
                    quizzes = Quiz.objects.none()
                    featured_quizzes = Quiz.objects.none()
    else:
        # Not authenticated, show only free tier quizzes
        from subscription.models import SubscriptionPlan, CurriculumAccess

        # Find a free subscription to determine what's available in free tier
        free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
        if free_plan:
            # Find sample curriculum accesses for the free tier
            sample_accesses = CurriculumAccess.objects.filter(
                subscription__plan=free_plan
            )

            if sample_accesses.exists():
                free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True).distinct()
                free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True).distinct()

                quizzes = Quiz.objects.filter(
                    quiz_filter,
                    curriculum_id__in=free_curriculum_ids,
                    class_level_id__in=free_class_level_ids
                ).order_by('-created_at')

                featured_quizzes = Quiz.objects.filter(
                    is_active=True,
                    is_featured=True,
                    curriculum_id__in=free_curriculum_ids,
                    class_level_id__in=free_class_level_ids
                ).order_by('-created_at')[:3]

                if not featured_quizzes.exists():
                    featured_quizzes = Quiz.objects.filter(
                        is_active=True,
                        curriculum_id__in=free_curriculum_ids,
                        class_level_id__in=free_class_level_ids
                    ).order_by('-created_at')[:3]
            else:
                quizzes = Quiz.objects.none()
                featured_quizzes = Quiz.objects.none()
        else:
            quizzes = Quiz.objects.none()
            featured_quizzes = Quiz.objects.none()

    # Group quizzes by subject for better organization
    from itertools import groupby
    from django.db.models import Count

    # Get all subjects the user has access to, with quiz counts
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        # Staff and superusers see all subjects
        base_query = Subject.objects.filter(is_active=True)

        # If curriculum and class level are selected, filter subjects accordingly
        if selected_curriculum and selected_class_level:
            subjects_with_quizzes = base_query.filter(
                curriculum__code=selected_curriculum,
                class_level_id=selected_class_level
            ).annotate(quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))).order_by('name')
        else:
            subjects_with_quizzes = base_query.annotate(
                quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))
            ).order_by('name')

    elif request.user.is_authenticated and active_subscription:
        # If tier three, show all subjects
        if active_subscription.plan.all_curriculums:
            base_query = Subject.objects.filter(is_active=True)

            # If curriculum and class level are selected, filter subjects accordingly
            if selected_curriculum and selected_class_level:
                subjects_with_quizzes = base_query.filter(
                    curriculum__code=selected_curriculum,
                    class_level_id=selected_class_level
                ).annotate(quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))).order_by('name')
            else:
                subjects_with_quizzes = base_query.annotate(
                    quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))
                ).order_by('name')
        else:
            # Get the curricula and class levels the user has access to
            accessible_curricula_ids = active_subscription.curriculum_accesses.values_list('curriculum_id', flat=True)
            accessible_class_level_ids = active_subscription.curriculum_accesses.values_list('class_level_id', flat=True)

            # Base query with access restrictions
            base_query = Subject.objects.filter(
                curriculum_id__in=accessible_curricula_ids,
                class_level_id__in=accessible_class_level_ids,
                is_active=True
            )

            # If curriculum and class level are selected, filter subjects accordingly
            if selected_curriculum and selected_class_level:
                subjects_with_quizzes = base_query.filter(
                    curriculum__code=selected_curriculum,
                    class_level_id=selected_class_level
                ).annotate(quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))).order_by('name')
            else:
                subjects_with_quizzes = base_query.annotate(
                    quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))
                ).order_by('name')
    else:
        # Free tier or not authenticated
        if free_plan:
            # Find sample curriculum accesses for the free tier
            free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True)
            free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True)

            # Base query with free tier restrictions
            base_query = Subject.objects.filter(
                curriculum_id__in=free_curriculum_ids,
                class_level_id__in=free_class_level_ids,
                is_active=True
            )

            # If curriculum and class level are selected, filter subjects accordingly
            if selected_curriculum and selected_class_level:
                subjects_with_quizzes = base_query.filter(
                    curriculum__code=selected_curriculum,
                    class_level_id=selected_class_level
                ).annotate(quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))).order_by('name')
            else:
                subjects_with_quizzes = base_query.annotate(
                    quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))
                ).order_by('name')
        else:
            subjects_with_quizzes = Subject.objects.none()

    # Group quizzes by subject
    quizzes_by_subject = {}
    for subject in subjects_with_quizzes:
        subject_quizzes = quizzes.filter(subject=subject)
        if subject_quizzes.exists():
            quizzes_by_subject[subject] = subject_quizzes

    # Paginate quizzes
    from django.core.paginator import Paginator
    paginator = Paginator(quizzes, 9)  # Show 9 quizzes per page
    page = request.GET.get('page')
    quizzes = paginator.get_page(page)

    # Get quiz statistics for authenticated users
    if request.user.is_authenticated:
        # Get completed and in-progress quizzes
        completed_quizzes = {}
        in_progress_quizzes = {}

        user_attempts = QuizAttempt.objects.filter(user=request.user)

        for attempt in user_attempts:
            if attempt.status == 'completed':
                completed_quizzes[attempt.quiz_id] = attempt.id
            elif attempt.status == 'in_progress':
                in_progress_quizzes[attempt.quiz_id] = attempt.id

        # Calculate average score
        completed_attempts = QuizAttempt.objects.filter(user=request.user, status='completed')
        if completed_attempts.exists():
            avg_score = int(sum(attempt.score for attempt in completed_attempts) / completed_attempts.count())
        else:
            avg_score = 0

        total_quizzes = Quiz.objects.filter(is_active=True).count()
    else:
        completed_quizzes = {}
        in_progress_quizzes = {}
        avg_score = 0
        total_quizzes = 0

    # Get curriculum and class level names for display
    selected_curriculum_name = ''
    selected_class_level_name = ''

    if selected_curriculum:
        curriculum_obj = Curriculum.objects.filter(code=selected_curriculum).first()
        if curriculum_obj:
            selected_curriculum_name = curriculum_obj.name

    if selected_class_level:
        class_level_obj = ClassLevel.objects.filter(id=selected_class_level).first()
        if class_level_obj:
            selected_class_level_name = class_level_obj.name

    # For Tier One users, if no curriculum is selected, auto-select their only curriculum and class level
    if is_tier_one and not selected_curriculum and len(accessible_curricula_ids) == 1 and len(accessible_class_level_ids) == 1:
        # Get the curriculum code
        auto_curriculum = Curriculum.objects.filter(id=accessible_curricula_ids[0]).first()
        if auto_curriculum:
            selected_curriculum = auto_curriculum.code
            selected_curriculum_name = auto_curriculum.name

        # Get the class level
        auto_class_level = ClassLevel.objects.filter(id=accessible_class_level_ids[0]).first()
        if auto_class_level:
            selected_class_level = str(auto_class_level.id)
            selected_class_level_name = auto_class_level.name

            # Update subjects based on auto-selected curriculum and class level
            subjects = Subject.objects.filter(
                curriculum__code=selected_curriculum,
                class_level_id=selected_class_level,
                is_active=True
            ).order_by('name')

            # Update subjects with quizzes
            subjects_with_quizzes = subjects.annotate(
                quiz_count=Count('quizzes', filter=Q(quizzes__is_active=True))
            ).order_by('name')

    context = {
        'curricula': curricula,
        'class_levels': class_levels,
        'subjects': subjects,
        'topics': topics,
        'selected_curriculum': selected_curriculum,
        'selected_curriculum_name': selected_curriculum_name,
        'selected_class_level': selected_class_level,
        'selected_class_level_name': selected_class_level_name,
        'selected_subject': selected_subject,
        'selected_topic': selected_topic,
        'quizzes': quizzes,
        'quizzes_by_subject': quizzes_by_subject,
        'subjects_with_quizzes': subjects_with_quizzes,
        'featured_quizzes': featured_quizzes,
        'completed_quizzes': completed_quizzes,
        'in_progress_quizzes': in_progress_quizzes,
        'avg_score': avg_score,
        'total_quizzes': total_quizzes,
        'is_tier_one': is_tier_one,
        'accessible_curricula_ids': accessible_curricula_ids,
        'accessible_class_level_ids': accessible_class_level_ids,
    }
    return render(request, 'quiz/quiz_home.html', context)


def quiz_class_level_list(request, curriculum_code):
    """View for listing all class levels for a specific curriculum."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_levels = ClassLevel.objects.filter(curriculum=curriculum, is_active=True).order_by('level_order')

    context = {
        'curriculum': curriculum,
        'class_levels': class_levels,
    }
    return render(request, 'quiz/quiz_class_level_list.html', context)


def quiz_subject_list(request, curriculum_code, class_level_id):
    """View for listing all subjects for a specific class level."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subjects = Subject.objects.filter(curriculum=curriculum, class_level=class_level, is_active=True).order_by('name')

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subjects': subjects,
    }
    return render(request, 'quiz/quiz_subject_list.html', context)


def quiz_topic_list(request, curriculum_code, class_level_id, subject_slug):
    """View for listing all topics for a specific subject."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)

    # Get all topics for this subject
    topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')

    # Get general quiz for this subject if it exists
    general_quiz = Quiz.objects.filter(
        quiz_type='general',
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        is_active=True
    ).first()

    # Get topic-specific quizzes
    topic_quizzes = Quiz.objects.filter(
        quiz_type='topic',
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        is_active=True
    )

    # Get notes count for each topic
    from django.db.models import Count
    topics = topics.annotate(notes_count=Count('notes', filter=Q(notes__is_active=True)))

    # Get quiz count for each topic
    topic_quiz_counts = {}
    for quiz in topic_quizzes:
        if quiz.topic_id in topic_quiz_counts:
            topic_quiz_counts[quiz.topic_id] += 1
        else:
            topic_quiz_counts[quiz.topic_id] = 1

    # Add quiz count to each topic
    for topic in topics:
        topic.quiz_count = topic_quiz_counts.get(topic.id, 0)

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topics': topics,
        'general_quiz': general_quiz,
        'topic_quizzes': topic_quizzes,
    }
    return render(request, 'quiz/quiz_topic_list.html', context)


@login_required
def start_general_quiz(request, curriculum_code, class_level_id, subject_slug):
    """Start a general quiz for a subject."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)

    # Get or create a general quiz for this subject
    quiz, created = Quiz.objects.get_or_create(
        quiz_type='general',
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        defaults={
            'title': f"General Quiz - {subject.name}",
            'description': f"Test your knowledge of {subject.name} with this general quiz.",
            'question_count': 10,
            'per_question_time': 15,
            'randomize_questions': True,
            'randomize_choices': True,
            'passing_score': 70,
            'is_active': True,
            'created_by': request.user if request.user.is_staff else None,
        }
    )

    # Create a new quiz attempt
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        status='in_progress',
        total_questions=quiz.question_count
    )

    # Redirect to the quiz taking page
    return redirect('quiz:take_quiz', quiz_id=quiz.id)


@login_required
def start_topic_quiz(request, curriculum_code, class_level_id, subject_slug, topic_slug):
    """Start a topic-specific quiz."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, is_active=True)

    # Get or create a topic quiz
    quiz, created = Quiz.objects.get_or_create(
        quiz_type='topic',
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        topic=topic,
        defaults={
            'title': f"Quiz - {topic.name}",
            'description': f"Test your knowledge of {topic.name} with this quiz.",
            'question_count': 10,
            'per_question_time': 15,
            'randomize_questions': True,
            'randomize_choices': True,
            'passing_score': 70,
            'is_active': True,
            'created_by': request.user if request.user.is_staff else None,
        }
    )

    # Create a new quiz attempt
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        status='in_progress',
        total_questions=quiz.question_count
    )

    # Redirect to the quiz taking page
    return redirect('quiz:take_quiz', quiz_id=quiz.id)


@login_required
def take_quiz(request, quiz_id):
    """View for taking a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    # Check if there's an in-progress attempt for this quiz
    quiz_attempt = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz,
        status='in_progress'
    ).order_by('-started_at').first()

    if not quiz_attempt:
        # Create a new quiz attempt using the QuizService
        quiz_attempt = QuizService.create_quiz_attempt(request.user, quiz)

    # Check if the quiz attempt has any questions
    if quiz_attempt.total_questions == 0:
        messages.warning(request, "No questions are available for this quiz. Please try a different subject or topic.")
        return redirect('quiz:quiz_home')

    # Get the current question ID from the URL parameter
    current_question_id = request.GET.get('question_id')

    # For practice exams, we should already have all question attempts created
    if quiz.quiz_type == 'practice':
        # Get all question attempts for this quiz attempt
        all_question_attempts = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt)

        if all_question_attempts.count() == 0:
            messages.warning(request, "No questions are available for this practice exam. Please try a different subject or topic.")
            return redirect('quiz:quiz_home')

        # If a specific question is requested, use that
        if current_question_id:
            try:
                current_question = Question.objects.get(id=current_question_id)
                question_attempt = QuestionAttempt.objects.get(
                    quiz_attempt=quiz_attempt,
                    question=current_question
                )
            except (Question.DoesNotExist, QuestionAttempt.DoesNotExist):
                # If question doesn't exist or isn't part of this quiz, get the first question
                question_attempt = all_question_attempts.first()
                current_question = question_attempt.question
        else:
            # Get the first unanswered question or the first question if all are answered
            unanswered_attempt = all_question_attempts.filter(
                Q(selected_choice__isnull=True) & Q(provided_answer='')
            ).first()

            if unanswered_attempt:
                question_attempt = unanswered_attempt
                current_question = question_attempt.question
            else:
                question_attempt = all_question_attempts.first()
                current_question = question_attempt.question
    else:
        # For regular quizzes, handle as before
        # If a specific question is requested, use that
        if current_question_id:
            try:
                current_question = Question.objects.get(id=current_question_id)
                # Verify this question belongs to this quiz attempt
                question_attempt, _ = QuestionAttempt.objects.get_or_create(
                    quiz_attempt=quiz_attempt,
                    question=current_question
                )
            except Question.DoesNotExist:
                # If question doesn't exist, get the next unanswered question
                current_question = QuizService.get_next_question(quiz_attempt)
                if current_question:
                    question_attempt, _ = QuestionAttempt.objects.get_or_create(
                        quiz_attempt=quiz_attempt,
                        question=current_question
                    )
                else:
                    messages.warning(request, "No questions are available for this quiz.")
                    return redirect('quiz:quiz_home')
        else:
            # Get the next question for this attempt
            current_question = QuizService.get_next_question(quiz_attempt)
            if current_question:
                question_attempt, _ = QuestionAttempt.objects.get_or_create(
                    quiz_attempt=quiz_attempt,
                    question=current_question
                )
            else:
                messages.warning(request, "No questions are available for this quiz.")
                return redirect('quiz:quiz_home')

    if not current_question:
        # If there are no more questions, redirect to the results page
        quiz_attempt.status = 'completed'
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()
        return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # Get all question attempts for this quiz attempt to build navigation
    all_question_attempts = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt).order_by('id')
    question_ids = list(all_question_attempts.values_list('question_id', flat=True))

    # Find previous and next question IDs for navigation
    try:
        current_index = question_ids.index(current_question.id)
        prev_question_id = question_ids[current_index - 1] if current_index > 0 else None
        next_question_id = question_ids[current_index + 1] if current_index < len(question_ids) - 1 else None
    except (ValueError, IndexError):
        prev_question_id = None
        next_question_id = None

    # Get randomized choices for multiple-choice questions
    choices = []
    if current_question.question_type == 'multiple_choice':
        choices = QuestionRandomizer.randomize_choices(current_question)

    # Calculate progress
    total_attempted = all_question_attempts.count()
    progress_percentage = int((total_attempted / quiz_attempt.total_questions) * 100)

    # Get the per-question time limit
    per_question_time = quiz.per_question_time

    # Get system settings for quiz feedback
    from core.models import SystemConfiguration
    system_settings = SystemConfiguration.get_settings()
    feedback_time = system_settings.quiz_feedback_time
    show_immediate_feedback = system_settings.quiz_show_immediate_feedback

    context = {
        'quiz': quiz_attempt.quiz,
        'quiz_attempt': quiz_attempt,
        'question_attempt': question_attempt,
        'choices': choices,
        'per_question_time': per_question_time,
        'progress_percentage': progress_percentage,
        'current_question_number': current_index + 1 if 'current_index' in locals() else 1,
        'total_questions': quiz_attempt.total_questions,
        'prev_question_id': prev_question_id,
        'next_question_id': next_question_id,
        'all_question_attempts': all_question_attempts,
        'feedback_time': feedback_time,
        'show_immediate_feedback': show_immediate_feedback,
    }
    return render(request, 'quiz/take_quiz.html', context)


@login_required
def answer_question(request, quiz_attempt_id, question_id):
    """View for answering a specific question."""
    quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id, is_active=True)

    # Check if the quiz is still in progress
    if quiz_attempt.status != 'in_progress':
        messages.warning(request, "This quiz is no longer in progress.")
        return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # Check if the quiz has timed out
    # Calculate total time limit based on per_question_time and question_count
    total_time_limit_seconds = quiz_attempt.quiz.per_question_time * quiz_attempt.quiz.question_count
    if total_time_limit_seconds > 0:
        elapsed_seconds = (timezone.now() - quiz_attempt.started_at).total_seconds()
        if elapsed_seconds > total_time_limit_seconds:
            quiz_attempt.status = 'timed_out'
            quiz_attempt.completed_at = timezone.now()
            quiz_attempt.save()
            messages.warning(request, "Time's up! Your quiz has been submitted.")
            return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # Get the question attempt or create a new one
    question_attempt, created = QuestionAttempt.objects.get_or_create(
        quiz_attempt=quiz_attempt,
        question=question
    )

    # Get the choices for the question
    if question.question_type == 'multiple_choice':
        # Use our service to randomize choices if needed
        if quiz_attempt.quiz.randomize_choices:
            # Use the quiz attempt ID as a seed for reproducible randomization
            choices = QuestionRandomizer.randomize_choices(
                question,
                seed=quiz_attempt.id
            )
        else:
            choices = list(QuestionChoice.objects.filter(question=question))
    else:
        choices = None

    # Calculate time remaining
    time_remaining = None
    # Calculate total time limit based on per_question_time and question_count
    total_time_limit_seconds = quiz_attempt.quiz.per_question_time * quiz_attempt.quiz.question_count
    if total_time_limit_seconds > 0:
        elapsed_seconds = (timezone.now() - quiz_attempt.started_at).total_seconds()
        time_remaining = max(0, total_time_limit_seconds - elapsed_seconds)

    # Calculate progress
    total_attempted = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt).count()
    progress_percentage = int((total_attempted / quiz_attempt.quiz.question_count) * 100)

    context = {
        'quiz': quiz_attempt.quiz,
        'quiz_attempt': quiz_attempt,
        'question_attempt': question_attempt,
        'choices': choices,
        'time_remaining': time_remaining,
        'progress_percentage': progress_percentage,
        'total_attempted': total_attempted,
        'total_questions': quiz_attempt.quiz.question_count,
    }
    return render(request, 'quiz/take_quiz.html', context)


@login_required
@require_POST
def submit_answer(request, quiz_attempt_id, question_id):
    """Submit an answer for a question."""
    quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id, is_active=True)

    # Check if the quiz is still in progress
    if quiz_attempt.status != 'in_progress':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': "This quiz is no longer in progress.",
                'redirect_url': f'/quiz/results/{quiz_attempt.id}/'
            })
        messages.warning(request, "This quiz is no longer in progress.")
        return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # Get the question attempt or create a new one
    question_attempt, _ = QuestionAttempt.objects.get_or_create(
        quiz_attempt=quiz_attempt,
        question=question
    )

    # Get time spent on this question
    time_spent = request.POST.get('time_spent', 0)
    try:
        time_spent = int(time_spent)
    except (ValueError, TypeError):
        time_spent = 0

    # Check if the question timed out
    timed_out = request.POST.get('timed_out') == 'true'
    question_attempt.time_spent = time_spent
    question_attempt.timed_out = timed_out

    # Process the answer based on question type
    is_correct = False
    correct_answer_text = None

    if not timed_out:  # Only check correctness if not timed out
        if question.question_type == 'multiple_choice':
            choice_id = request.POST.get('choice')
            if choice_id:
                choice = get_object_or_404(QuestionChoice, id=choice_id, question=question)
                question_attempt.selected_choice = choice
                is_correct = choice.is_correct

                # Get the correct answer text for feedback
                correct_choice = QuestionChoice.objects.filter(question=question, is_correct=True).first()
                if correct_choice:
                    correct_answer_text = correct_choice.text
        else:  # short_answer
            provided_answer = request.POST.get('answer', '').strip()
            question_attempt.provided_answer = provided_answer

            # Check if the answer is correct using our validator
            correct_answers = ShortAnswer.objects.filter(question=question)
            is_correct = ShortAnswerValidator.validate_answer(provided_answer, correct_answers)

            # Get the correct answer text for feedback
            if correct_answers.exists():
                correct_answer_text = ", ".join([ans.text for ans in correct_answers])

    # Update the question attempt
    question_attempt.is_correct = is_correct
    question_attempt.save()

    # Update the quiz attempt score
    correct_count = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt, is_correct=True).count()
    quiz_attempt.correct_answers = correct_count
    quiz_attempt.score = int((correct_count / quiz_attempt.total_questions) * 100)
    quiz_attempt.save()

    # Get the next question ID if available
    next_question_id = request.POST.get('next_question_id')

    # Get all question attempts for this quiz attempt
    all_question_attempts = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt)
    attempted_count = all_question_attempts.count()

    # Check if this was the last question
    is_last_question = attempted_count >= quiz_attempt.total_questions

    # Determine the redirect URL
    if is_last_question:
        # If this was the last question, mark the quiz as completed
        quiz_attempt.status = 'completed'
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()
        redirect_url = f'/quiz/results/{quiz_attempt.id}/'
    elif next_question_id:
        # If we have a next question ID, go to that question
        redirect_url = f'/quiz/take/{quiz_attempt.quiz.id}/?question_id={next_question_id}'
    else:
        # Otherwise, get the next unanswered question
        next_question = QuizService.get_next_question(quiz_attempt)
        if next_question:
            redirect_url = f'/quiz/take/{quiz_attempt.quiz.id}/?question_id={next_question.id}'
        else:
            # If no more questions, go to results
            quiz_attempt.status = 'completed'
            quiz_attempt.completed_at = timezone.now()
            quiz_attempt.save()
            redirect_url = f'/quiz/results/{quiz_attempt.id}/'

    # If this is an AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': correct_answer_text,
            'explanation': question.explanation,
            'redirect_url': redirect_url
        })

    # Otherwise, redirect to the appropriate page
    return redirect(redirect_url)


@login_required
def question_feedback(request, quiz_attempt_id, question_id, next_question_id=None):
    """Show feedback for a question after answering."""
    quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id, is_active=True)

    # Get the question attempt
    question_attempt = get_object_or_404(QuestionAttempt,
                                         quiz_attempt=quiz_attempt,
                                         question=question)

    # Get all choices for multiple choice questions
    choices = None
    if question.question_type == 'multiple_choice':
        choices = QuestionChoice.objects.filter(question=question)

    # Get correct answers for short answer questions
    correct_answers = None
    if question.question_type == 'short_answer':
        correct_answers = ShortAnswer.objects.filter(question=question)

    context = {
        'quiz_attempt': quiz_attempt,
        'question': question,
        'question_attempt': question_attempt,
        'choices': choices,
        'correct_answers': correct_answers,
        'next_question_id': next_question_id,
    }

    return render(request, 'quiz/question_feedback.html', context)


@login_required
def quiz_results(request, quiz_attempt_id):
    """View for showing quiz results."""
    quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=request.user)

    # Get all question attempts for this quiz
    question_attempts = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt).order_by('answered_at')

    # Calculate statistics
    total_questions = quiz_attempt.total_questions
    correct_answers = quiz_attempt.correct_answers
    incorrect_answers = total_questions - correct_answers
    score_percentage = quiz_attempt.score_percentage
    is_passed = quiz_attempt.is_passed

    # Calculate time taken
    if quiz_attempt.completed_at:
        time_taken = (quiz_attempt.completed_at - quiz_attempt.started_at).total_seconds() / 60
    else:
        time_taken = (timezone.now() - quiz_attempt.started_at).total_seconds() / 60

    context = {
        'quiz_attempt': quiz_attempt,
        'question_attempts': question_attempts,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'score_percentage': score_percentage,
        'is_passed': is_passed,
        'time_taken': time_taken,
    }
    return render(request, 'quiz/quiz_results.html', context)


@login_required
def start_quiz(request, quiz_id):
    """Start a new attempt for an existing quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    # Create a new quiz attempt
    quiz_attempt = QuizService.create_quiz_attempt(request.user, quiz)

    # Redirect to the quiz taking page
    return redirect('quiz:take_quiz', quiz_id=quiz.id)


@login_required
def resume_quiz(request, quiz_attempt_id):
    """Resume an in-progress quiz."""
    quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=request.user)

    # Check if the quiz is still in progress
    if quiz_attempt.status != 'in_progress':
        messages.warning(request, "This quiz is no longer in progress.")
        return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # Check if there are any existing question attempts
    existing_attempts = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt)

    # For practice exams, we should already have all question attempts created
    if quiz_attempt.quiz.quiz_type == 'practice' and existing_attempts.exists():
        # Find the first unanswered question
        unanswered_attempt = existing_attempts.filter(
            Q(selected_choice__isnull=True) & Q(provided_answer='')
        ).first()

        if unanswered_attempt:
            return redirect('quiz:answer_question',
                            quiz_attempt_id=quiz_attempt.id,
                            question_id=unanswered_attempt.question.id)
        else:
            # If all questions have been answered, complete the quiz
            quiz_attempt.status = 'completed'
            quiz_attempt.completed_at = timezone.now()
            quiz_attempt.save()
            return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # For other quiz types, get the next unanswered question
    next_question = QuizService.get_next_question(quiz_attempt)

    if next_question:
        # Redirect to the question
        return redirect('quiz:answer_question',
                        quiz_attempt_id=quiz_attempt.id,
                        question_id=next_question.id)
    else:
        # If all questions have been answered, complete the quiz
        quiz_attempt.status = 'completed'
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()
        return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)


@login_required
def quiz_history(request):
    """View for showing quiz history."""
    # Get all quiz attempts for the user
    quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-started_at')

    # Get filter parameters
    subject_slug = request.GET.get('subject', '')
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    # Apply filters
    if subject_slug:
        quiz_attempts = quiz_attempts.filter(quiz__subject__slug=subject_slug)

    if status:
        quiz_attempts = quiz_attempts.filter(status=status)

    if date_from:
        from datetime import datetime
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            quiz_attempts = quiz_attempts.filter(started_at__gte=date_from_obj)
        except ValueError:
            pass

    if date_to:
        from datetime import datetime
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            quiz_attempts = quiz_attempts.filter(started_at__lte=date_to_obj)
        except ValueError:
            pass

    # Get all subjects for the filter dropdown
    subjects = Subject.objects.filter(is_active=True).order_by('name')

    # Calculate statistics
    completed_quizzes = [attempt for attempt in quiz_attempts if attempt.status == 'completed']
    in_progress_quizzes = [attempt for attempt in quiz_attempts if attempt.status == 'in_progress']

    # Calculate average score
    if completed_quizzes:
        avg_score = sum(attempt.score for attempt in completed_quizzes) / len(completed_quizzes)
    else:
        avg_score = 0

    context = {
        'quiz_attempts': quiz_attempts,
        'subjects': subjects,
        'selected_subject': subject_slug,
        'selected_status': status,
        'date_from': date_from,
        'date_to': date_to,
        'completed_quizzes': completed_quizzes,
        'in_progress_quizzes': in_progress_quizzes,
        'avg_score': round(avg_score),
    }
    return render(request, 'quiz/quiz_history.html', context)


@login_required
def study_mode(request, curriculum_code, class_level_id, subject_slug, topic_slug, note_id=None):
    """Study mode view for a topic."""
    # Get curriculum, class level, subject, and topic
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, is_active=True)

    # Get all topics for this subject for the sidebar
    topics = Topic.objects.filter(subject=subject, is_active=True)

    # Get all notes for this topic
    notes = Note.objects.filter(topic=topic, is_active=True).order_by('order')

    if not notes.exists():
        messages.warning(request, "This topic doesn't have any study materials yet.")
        return redirect('curriculum:topic_detail',
                        curriculum_code=curriculum_code,
                        class_level_id=class_level_id,
                        subject_slug=subject_slug,
                        topic_slug=topic_slug)

    # If note_id is provided, get that note, otherwise get the first note
    if note_id:
        current_note = get_object_or_404(Note, id=note_id, topic=topic, is_active=True)
    else:
        current_note = notes.first()

    # Get the previous and next notes for navigation
    try:
        prev_note = notes.filter(order__lt=current_note.order).last()
    except:
        prev_note = None

    try:
        next_note = notes.filter(order__gt=current_note.order).first()
    except:
        next_note = None

    # Get the user's completed notes for this topic
    completed_notes = NoteCompletion.objects.filter(user=request.user, note__topic=topic)
    completed_note_ids = [completion.note_id for completion in completed_notes]

    # Calculate progress
    total_notes = notes.count()
    completed_notes_count = completed_notes.count()
    progress_percentage = (completed_notes_count / total_notes) * 100 if total_notes > 0 else 0

    return render(request, 'quiz/study_mode.html', {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topic': topic,
        'topics': topics,
        'notes': notes,
        'current_note': current_note,
        'prev_note': prev_note,
        'next_note': next_note,
        'completed_note_ids': completed_note_ids,
        'total_notes': total_notes,
        'completed_notes': completed_notes_count,
        'progress_percentage': progress_percentage,
    })


@login_required
def study_note(request, curriculum_code, class_level_id, subject_slug, topic_slug, note_id):
    """HTMX view for loading a note in study mode."""
    # Get curriculum, class level, subject, and topic
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, is_active=True)

    # Get the note
    current_note = get_object_or_404(Note, id=note_id, topic=topic, is_active=True)

    # Get all notes for this topic for navigation
    notes = Note.objects.filter(topic=topic, is_active=True).order_by('order')

    # Get the previous and next notes for navigation
    try:
        prev_note = notes.filter(order__lt=current_note.order).last()
    except:
        prev_note = None

    try:
        next_note = notes.filter(order__gt=current_note.order).first()
    except:
        next_note = None

    # Get the user's completed notes for this topic
    completed_notes = NoteCompletion.objects.filter(user=request.user, note__topic=topic)
    completed_note_ids = [completion.note_id for completion in completed_notes]

    return render(request, 'quiz/partials/note_content.html', {
        'current_note': current_note,
        'prev_note': prev_note,
        'next_note': next_note,
        'completed_note_ids': completed_note_ids,
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topic': topic,
    })


@login_required
@require_POST
def mark_note_completed(request, note_id):
    """Mark a note as completed or uncompleted."""
    note = get_object_or_404(Note, id=note_id)

    # Check if the note is already marked as completed
    completion, created = NoteCompletion.objects.get_or_create(user=request.user, note=note)

    if not created:
        # If it already exists, delete it (toggle off)
        completion.delete()

    return JsonResponse({'success': True})


@login_required
def check_answer(request, question_id, choice_id):
    """Check if a multiple-choice answer is correct."""
    question = get_object_or_404(Question, id=question_id)
    choice = get_object_or_404(QuestionChoice, id=choice_id, question=question)

    return JsonResponse({
        'is_correct': choice.is_correct,
        'explanation': question.explanation,
    })


@login_required
@csrf_exempt
def check_short_answer(request, question_id):
    """Check if a short answer is correct."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    import json
    data = json.loads(request.body)
    answer = data.get('answer', '').strip()

    question = get_object_or_404(Question, id=question_id)
    correct_answers = ShortAnswer.objects.filter(question=question)

    is_correct = ShortAnswerValidator.validate_answer(answer, correct_answers)

    return JsonResponse({
        'is_correct': is_correct,
        'explanation': question.explanation,
    })


def get_class_levels(request):
    """AJAX endpoint to get class levels for a curriculum."""
    curriculum_code = request.GET.get('curriculum', '')

    # Debug logging
    print(f"get_class_levels called with curriculum_code: {curriculum_code}")
    print(f"Request GET parameters: {request.GET}")
    print(f"User authenticated: {request.user.is_authenticated}")

    # Get accessible class levels based on user's subscription tier
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Staff and superusers see all class levels
            if curriculum_code:
                try:
                    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
                    class_levels = ClassLevel.objects.filter(curriculum=curriculum, is_active=True).order_by('level_order')
                    print(f"Found {class_levels.count()} class levels for curriculum {curriculum_code}")
                    for level in class_levels:
                        print(f"  - {level.id}: {level.name}")
                except Exception as e:
                    print(f"Error getting class levels: {e}")
                    class_levels = ClassLevel.objects.none()
            else:
                class_levels = ClassLevel.objects.filter(is_active=True).order_by('curriculum__name', 'level_order')
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
                # If tier three, show all class levels
                if active_subscription.plan.all_curriculums:
                    if curriculum_code:
                        curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
                        class_levels = ClassLevel.objects.filter(curriculum=curriculum, is_active=True).order_by('level_order')
                    else:
                        class_levels = ClassLevel.objects.filter(is_active=True).order_by('curriculum__name', 'level_order')
                else:
                    # Get the class levels the user has access to
                    accessible_class_level_ids = active_subscription.curriculum_accesses.values_list('class_level_id', flat=True).distinct()

                    if curriculum_code:
                        curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
                        class_levels = ClassLevel.objects.filter(
                            id__in=accessible_class_level_ids,
                            curriculum=curriculum,
                            is_active=True
                        ).order_by('level_order')
                    else:
                        class_levels = ClassLevel.objects.filter(
                            id__in=accessible_class_level_ids,
                            is_active=True
                        ).order_by('curriculum__name', 'level_order')
            else:
                # No active subscription, show only free tier class levels
                from subscription.models import SubscriptionPlan, CurriculumAccess

                # Find a free subscription to determine what's available in free tier
                free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
                if free_plan:
                    # Find sample curriculum accesses for the free tier
                    sample_accesses = CurriculumAccess.objects.filter(
                        subscription__plan=free_plan
                    )

                    if sample_accesses.exists():
                        free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True).distinct()

                        if curriculum_code:
                            curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
                            class_levels = ClassLevel.objects.filter(
                                id__in=free_class_level_ids,
                                curriculum=curriculum,
                                is_active=True
                            ).order_by('level_order')
                        else:
                            class_levels = ClassLevel.objects.filter(
                                id__in=free_class_level_ids,
                                is_active=True
                            ).order_by('curriculum__name', 'level_order')
                    else:
                        class_levels = ClassLevel.objects.none()
                else:
                    class_levels = ClassLevel.objects.none()
    else:
        # Not authenticated, show only free tier class levels
        from subscription.models import SubscriptionPlan, CurriculumAccess

        # Find a free subscription to determine what's available in free tier
        free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
        if free_plan:
            # Find sample curriculum accesses for the free tier
            sample_accesses = CurriculumAccess.objects.filter(
                subscription__plan=free_plan
            )

            if sample_accesses.exists():
                free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True).distinct()

                if curriculum_code:
                    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
                    class_levels = ClassLevel.objects.filter(
                        id__in=free_class_level_ids,
                        curriculum=curriculum,
                        is_active=True
                    ).order_by('level_order')
                else:
                    class_levels = ClassLevel.objects.filter(
                        id__in=free_class_level_ids,
                        is_active=True
                    ).order_by('curriculum__name', 'level_order')
            else:
                class_levels = ClassLevel.objects.none()
        else:
            class_levels = ClassLevel.objects.none()

    # Get the selected class level from the request, if any
    selected_class_level = request.GET.get('selected_class_level', None)

    return render(request, 'quiz/partials/class_level_options.html', {
        'class_levels': class_levels,
        'selected_class_level': selected_class_level
    })


def get_subjects(request):
    """AJAX endpoint to get subjects for a class level."""
    class_level_id = request.GET.get('class_level', '')

    # Get accessible subjects based on user's subscription tier
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Staff and superusers see all subjects
            if class_level_id:
                class_level = get_object_or_404(ClassLevel, id=class_level_id, is_active=True)
                subjects = Subject.objects.filter(class_level=class_level, is_active=True).order_by('name')
            else:
                subjects = Subject.objects.filter(is_active=True).order_by('class_level__curriculum__name', 'class_level__level_order', 'name')
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
                # If tier three, show all subjects
                if active_subscription.plan.all_curriculums:
                    if class_level_id:
                        class_level = get_object_or_404(ClassLevel, id=class_level_id, is_active=True)
                        subjects = Subject.objects.filter(class_level=class_level, is_active=True).order_by('name')
                    else:
                        subjects = Subject.objects.filter(is_active=True).order_by('class_level__curriculum__name', 'class_level__level_order', 'name')
                else:
                    # Get the curricula and class levels the user has access to
                    accessible_curricula_ids = active_subscription.curriculum_accesses.values_list('curriculum_id', flat=True).distinct()
                    accessible_class_level_ids = active_subscription.curriculum_accesses.values_list('class_level_id', flat=True).distinct()

                    if class_level_id:
                        # Check if the user has access to this class level
                        if int(class_level_id) in accessible_class_level_ids:
                            class_level = get_object_or_404(ClassLevel, id=class_level_id, is_active=True)
                            subjects = Subject.objects.filter(
                                class_level=class_level,
                                curriculum_id__in=accessible_curricula_ids,
                                is_active=True
                            ).order_by('name')
                        else:
                            subjects = Subject.objects.none()
                    else:
                        subjects = Subject.objects.filter(
                            curriculum_id__in=accessible_curricula_ids,
                            class_level_id__in=accessible_class_level_ids,
                            is_active=True
                        ).order_by('class_level__curriculum__name', 'class_level__level_order', 'name')
            else:
                # No active subscription, show only free tier subjects
                from subscription.models import SubscriptionPlan, CurriculumAccess

                # Find a free subscription to determine what's available in free tier
                free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
                if free_plan:
                    # Find sample curriculum accesses for the free tier
                    sample_accesses = CurriculumAccess.objects.filter(
                        subscription__plan=free_plan
                    )

                    if sample_accesses.exists():
                        free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True).distinct()
                        free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True).distinct()

                        if class_level_id:
                            # Check if this class level is available in the free tier
                            if int(class_level_id) in free_class_level_ids:
                                class_level = get_object_or_404(ClassLevel, id=class_level_id, is_active=True)
                                subjects = Subject.objects.filter(
                                    class_level=class_level,
                                    curriculum_id__in=free_curriculum_ids,
                                    is_active=True
                                ).order_by('name')
                            else:
                                subjects = Subject.objects.none()
                        else:
                            subjects = Subject.objects.filter(
                                curriculum_id__in=free_curriculum_ids,
                                class_level_id__in=free_class_level_ids,
                                is_active=True
                            ).order_by('class_level__curriculum__name', 'class_level__level_order', 'name')
                    else:
                        subjects = Subject.objects.none()
                else:
                    subjects = Subject.objects.none()
    else:
        # Not authenticated, show only free tier subjects
        from subscription.models import SubscriptionPlan, CurriculumAccess

        # Find a free subscription to determine what's available in free tier
        free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
        if free_plan:
            # Find sample curriculum accesses for the free tier
            sample_accesses = CurriculumAccess.objects.filter(
                subscription__plan=free_plan
            )

            if sample_accesses.exists():
                free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True).distinct()
                free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True).distinct()

                if class_level_id:
                    # Check if this class level is available in the free tier
                    if int(class_level_id) in free_class_level_ids:
                        class_level = get_object_or_404(ClassLevel, id=class_level_id, is_active=True)
                        subjects = Subject.objects.filter(
                            class_level=class_level,
                            curriculum_id__in=free_curriculum_ids,
                            is_active=True
                        ).order_by('name')
                    else:
                        subjects = Subject.objects.none()
                else:
                    subjects = Subject.objects.filter(
                        curriculum_id__in=free_curriculum_ids,
                        class_level_id__in=free_class_level_ids,
                        is_active=True
                    ).order_by('class_level__curriculum__name', 'class_level__level_order', 'name')
            else:
                subjects = Subject.objects.none()
        else:
            subjects = Subject.objects.none()

    return render(request, 'quiz/partials/subject_options.html', {
        'subjects': subjects
    })


@login_required
def practice_exam_setup(request, curriculum_code, class_level_id, subject_slug):
    """Setup page for creating a practice exam."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)

    # Get all topics for this subject
    topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')

    if request.method == 'POST':
        # Process the form and create the practice exam
        return practice_exam(request, curriculum_code, class_level_id, subject_slug)

    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topics': topics,
    }

    return render(request, 'quiz/practice_exam_setup.html', context)


@login_required
def practice_exam(request, curriculum_code, class_level_id, subject_slug):
    """Create and start a practice exam for a subject."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)

    # Get selected topics from the form
    selected_topic_ids = request.POST.getlist('topics')
    question_count = request.POST.get('question_count', 40)

    try:
        question_count = int(question_count)
        if question_count < 1:
            question_count = 40
    except (ValueError, TypeError):
        question_count = 40

    # Get topics if selected
    topics = None
    if selected_topic_ids:
        topics = Topic.objects.filter(id__in=selected_topic_ids, subject=subject, is_active=True)

    # Create a practice exam using the QuizService
    quiz_attempt = QuizService.create_practice_exam(
        user=request.user,
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        topics=topics,
        question_count=question_count
    )

    # The QuizService.create_practice_exam method now handles all of this:
    # - Getting questions for selected topics or all topics
    # - Filtering out premium questions if user is not premium
    # - Randomizing and limiting to question count
    # - Creating question attempts for each question

    # Redirect to the quiz taking page
    return redirect('quiz:take_quiz', quiz_id=quiz_attempt.quiz.id)


def subject_quizzes(request, subject_slug):
    """View for showing all quizzes for a specific subject."""
    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
    curriculum = subject.curriculum
    class_level = subject.class_level

    # Get all quizzes for this subject
    quizzes = Quiz.objects.filter(
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        is_active=True
    ).order_by('-created_at')

    # Calculate time limit for each quiz
    for quiz in quizzes:
        # Calculate time limit in minutes
        quiz.time_limit = round(quiz.question_count * quiz.per_question_time / 60)

    # Get all topics for this subject for filtering
    topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')

    # Get user's quiz attempts
    if request.user.is_authenticated:
        completed_quizzes = {}
        in_progress_quizzes = {}

        # Get all user attempts for these quizzes
        from django.db.models import Max, Count

        user_attempts = QuizAttempt.objects.filter(
            user=request.user,
            quiz__subject=subject
        )

        # Get highest score and attempt count for each quiz
        quiz_stats = {}
        for quiz in quizzes:
            # Get completed attempts for this quiz
            quiz_completed_attempts = user_attempts.filter(
                quiz_id=quiz.id,
                status='completed'
            )

            # Get highest score
            highest_score_attempt = quiz_completed_attempts.order_by('-score').first()
            if highest_score_attempt:
                quiz_stats[quiz.id] = {
                    'highest_score': highest_score_attempt.score,
                    'attempt_count': quiz_completed_attempts.count()
                }

            # Track in-progress and completed quizzes
            in_progress_attempt = user_attempts.filter(quiz_id=quiz.id, status='in_progress').first()
            if in_progress_attempt:
                in_progress_quizzes[quiz.id] = in_progress_attempt.id
            elif highest_score_attempt:
                completed_quizzes[quiz.id] = highest_score_attempt.id

        # Add stats to each quiz object
        for quiz in quizzes:
            if quiz.id in quiz_stats:
                quiz.highest_score = quiz_stats[quiz.id]['highest_score']
                quiz.attempt_count = quiz_stats[quiz.id]['attempt_count']
    else:
        completed_quizzes = {}
        in_progress_quizzes = {}

    context = {
        'subject': subject,
        'curriculum': curriculum,
        'class_level': class_level,
        'quizzes': quizzes,
        'topics': topics,
        'completed_quizzes': completed_quizzes,
        'in_progress_quizzes': in_progress_quizzes,
    }
    return render(request, 'quiz/subject_quizzes.html', context)


def get_topics(request):
    """AJAX endpoint to get topics for a subject."""
    subject_slug = request.GET.get('subject', '')

    # Get accessible topics based on user's subscription tier
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Staff and superusers see all topics
            if subject_slug:
                subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
                topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')
            else:
                topics = Topic.objects.filter(is_active=True).order_by('subject__name', 'order', 'name')
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
                # If tier three, show all topics
                if active_subscription.plan.all_curriculums:
                    if subject_slug:
                        subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
                        topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')
                    else:
                        topics = Topic.objects.filter(is_active=True).order_by('subject__name', 'order', 'name')
                else:
                    # Get the curricula and class levels the user has access to
                    accessible_curricula_ids = active_subscription.curriculum_accesses.values_list('curriculum_id', flat=True).distinct()
                    accessible_class_level_ids = active_subscription.curriculum_accesses.values_list('class_level_id', flat=True).distinct()

                    if subject_slug:
                        subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
                        # Check if the user has access to this subject's curriculum and class level
                        if subject.curriculum_id in accessible_curricula_ids and subject.class_level_id in accessible_class_level_ids:
                            topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')
                        else:
                            topics = Topic.objects.none()
                    else:
                        topics = Topic.objects.filter(
                            subject__curriculum_id__in=accessible_curricula_ids,
                            subject__class_level_id__in=accessible_class_level_ids,
                            is_active=True
                        ).order_by('subject__name', 'order', 'name')
            else:
                # No active subscription, show only free tier topics
                from subscription.models import SubscriptionPlan, CurriculumAccess

                # Find a free subscription to determine what's available in free tier
                free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
                if free_plan:
                    # Find sample curriculum accesses for the free tier
                    sample_accesses = CurriculumAccess.objects.filter(
                        subscription__plan=free_plan
                    )

                    if sample_accesses.exists():
                        free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True).distinct()
                        free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True).distinct()

                        if subject_slug:
                            subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
                            # Check if this subject is available in the free tier
                            if subject.curriculum_id in free_curriculum_ids and subject.class_level_id in free_class_level_ids:
                                topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')
                            else:
                                topics = Topic.objects.none()
                        else:
                            topics = Topic.objects.filter(
                                subject__curriculum_id__in=free_curriculum_ids,
                                subject__class_level_id__in=free_class_level_ids,
                                is_active=True
                            ).order_by('subject__name', 'order', 'name')
                    else:
                        topics = Topic.objects.none()
                else:
                    topics = Topic.objects.none()
    else:
        # Not authenticated, show only free tier topics
        from subscription.models import SubscriptionPlan, CurriculumAccess

        # Find a free subscription to determine what's available in free tier
        free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
        if free_plan:
            # Find sample curriculum accesses for the free tier
            sample_accesses = CurriculumAccess.objects.filter(
                subscription__plan=free_plan
            )

            if sample_accesses.exists():
                free_curriculum_ids = sample_accesses.values_list('curriculum_id', flat=True).distinct()
                free_class_level_ids = sample_accesses.values_list('class_level_id', flat=True).distinct()

                if subject_slug:
                    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
                    # Check if this subject is available in the free tier
                    if subject.curriculum_id in free_curriculum_ids and subject.class_level_id in free_class_level_ids:
                        topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')
                    else:
                        topics = Topic.objects.none()
                else:
                    topics = Topic.objects.filter(
                        subject__curriculum_id__in=free_curriculum_ids,
                        subject__class_level_id__in=free_class_level_ids,
                        is_active=True
                    ).order_by('subject__name', 'order', 'name')
            else:
                topics = Topic.objects.none()
        else:
            topics = Topic.objects.none()

    return render(request, 'quiz/partials/topic_options.html', {
        'topics': topics
    })
