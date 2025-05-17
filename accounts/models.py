from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Count, Sum, F, Q


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model that uses email as the username field."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Additional fields
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    # Subscription related fields
    is_premium = models.BooleanField(default=False)
    subscription_end_date = models.DateTimeField(null=True, blank=True)

    # User preferences
    preferred_curriculum = models.ForeignKey(
        'curriculum.Curriculum',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users_with_preference'
    )
    preferred_class_level = models.ForeignKey(
        'curriculum.ClassLevel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users_with_preference'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def is_subscription_active(self):
        """Check if the user's subscription is active."""
        if not self.is_premium:
            return False

        from django.utils import timezone
        if self.subscription_end_date and self.subscription_end_date > timezone.now():
            return True

        return False

    def get_active_subscription(self):
        """Get the user's active subscription."""
        from subscription.models import Subscription
        from django.utils import timezone

        return Subscription.objects.filter(
            user=self,
            status='active',
            end_date__gt=timezone.now()
        ).first()

    def has_access_to_curriculum(self, curriculum):
        """Check if the user has access to a specific curriculum."""
        # Staff and superusers have access to everything
        if self.is_staff or self.is_superuser:
            return True

        # Get the user's active subscription
        subscription = self.get_active_subscription()
        if not subscription:
            return False

        return subscription.has_access_to_curriculum(curriculum)

    def has_access_to_class_level(self, curriculum, class_level):
        """Check if the user has access to a specific class level within a curriculum."""
        # Staff and superusers have access to everything
        if self.is_staff or self.is_superuser:
            return True

        # Get the user's active subscription
        subscription = self.get_active_subscription()
        if not subscription:
            return False

        return subscription.has_access_to_class_level(curriculum, class_level)

    def has_access_to_content(self, note):
        """Check if the user has access to a specific note."""
        # Staff and superusers have access to everything
        if self.is_staff or self.is_superuser:
            return True

        # Get the user's active subscription
        subscription = self.get_active_subscription()
        if not subscription:
            return False

        return subscription.has_access_to_content(note)

    def get_quiz_stats(self):
        """Get the user's quiz statistics."""
        from quiz.models import QuizAttempt

        # Get all completed quiz attempts
        completed_attempts = QuizAttempt.objects.filter(
            user=self,
            status='completed'
        )

        # Calculate statistics
        total_attempts = completed_attempts.count()
        if total_attempts == 0:
            return {
                'total_attempts': 0,
                'average_score': 0,
                'total_questions': 0,
                'correct_answers': 0,
                'pass_rate': 0,
                'subjects': [],
            }

        average_score = completed_attempts.aggregate(Avg('score'))['score__avg'] or 0
        total_questions = completed_attempts.aggregate(Sum('total_questions'))['total_questions__sum'] or 0
        correct_answers = completed_attempts.aggregate(Sum('correct_answers'))['correct_answers__sum'] or 0

        # Calculate passed attempts by comparing score to passing score for each attempt
        passed_attempts = 0
        for attempt in completed_attempts:
            if attempt.score_percentage >= attempt.quiz.passing_score:
                passed_attempts += 1

        pass_rate = (passed_attempts / total_attempts) * 100 if total_attempts > 0 else 0

        # Get subject-specific statistics
        subject_stats = []
        from curriculum.models import Subject
        from quiz.models import Quiz

        # Get all subjects that have quizzes attempted by this user
        subject_ids = set()
        for attempt in completed_attempts:
            if hasattr(attempt.quiz, 'subject') and attempt.quiz.subject:
                subject_ids.add(attempt.quiz.subject.id)

        # Get the actual subject objects
        subjects = Subject.objects.filter(id__in=subject_ids)

        for subject in subjects:
            # Get attempts for quizzes in this subject
            subject_attempts = completed_attempts.filter(quiz__subject=subject)

            if subject_attempts.count() > 0:
                # Calculate pass rate manually
                passed_subject_attempts = 0
                for attempt in subject_attempts:
                    if attempt.score_percentage >= attempt.quiz.passing_score:
                        passed_subject_attempts += 1

                pass_rate = (passed_subject_attempts / subject_attempts.count()) * 100 if subject_attempts.count() > 0 else 0

                subject_stats.append({
                    'subject': subject,
                    'attempts': subject_attempts.count(),
                    'average_score': subject_attempts.aggregate(Avg('score'))['score__avg'] or 0,
                    'pass_rate': pass_rate,
                })

        return {
            'total_attempts': total_attempts,
            'average_score': average_score,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'pass_rate': pass_rate,
            'subjects': subject_stats,
        }

    def get_study_progress(self):
        """Get the user's study progress."""
        from curriculum.models import Note, NoteCompletion, Topic

        # Get all topics with notes
        topics_with_notes = Topic.objects.filter(notes__isnull=False).distinct()

        # Calculate overall progress
        total_notes = Note.objects.filter(is_active=True).count()
        completed_notes = NoteCompletion.objects.filter(user=self).count()
        overall_progress = (completed_notes / total_notes) * 100 if total_notes > 0 else 0

        # Calculate topic-specific progress
        topic_progress = []

        for topic in topics_with_notes:
            topic_notes = Note.objects.filter(topic=topic, is_active=True)
            topic_note_count = topic_notes.count()

            if topic_note_count == 0:
                continue

            completed_topic_notes = NoteCompletion.objects.filter(
                user=self,
                note__topic=topic
            ).count()

            topic_progress.append({
                'topic': topic,
                'subject': topic.subject,
                'total_notes': topic_note_count,
                'completed_notes': completed_topic_notes,
                'progress_percentage': (completed_topic_notes / topic_note_count) * 100 if topic_note_count > 0 else 0,
            })

        return {
            'total_notes': total_notes,
            'completed_notes': completed_notes,
            'overall_progress': overall_progress,
            'topics': topic_progress,
        }

    def get_recent_activity(self, limit=10):
        """Get the user's recent activity."""
        from quiz.models import QuizAttempt
        from curriculum.models import NoteCompletion

        # Get recent quiz attempts
        recent_quizzes = QuizAttempt.objects.filter(
            user=self
        ).order_by('-started_at')[:limit]

        # Get recent note completions
        recent_notes = NoteCompletion.objects.filter(
            user=self
        ).order_by('-created_at')[:limit]

        # Combine and sort by date
        activity = []

        for quiz in recent_quizzes:
            activity.append({
                'type': 'quiz',
                'date': quiz.started_at,
                'object': quiz,
                'details': f"Took quiz: {quiz.quiz.title} - Score: {quiz.score}%"
            })

        for note in recent_notes:
            activity.append({
                'type': 'note',
                'date': note.created_at,
                'object': note,
                'details': f"Completed note: {note.note.title}"
            })

        # Sort by date (newest first) and limit
        activity.sort(key=lambda x: x['date'], reverse=True)
        return activity[:limit]


class UserGroup(models.Model):
    """Model for family and enterprise subscription groups."""

    GROUP_TYPE_CHOICES = (
        ('family', 'Family'),
        ('enterprise', 'Enterprise'),
    )

    name = models.CharField(max_length=100)
    group_type = models.CharField(max_length=20, choices=GROUP_TYPE_CHOICES)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_groups')
    members = models.ManyToManyField(User, related_name='member_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_group_type_display()})"

    @property
    def member_count(self):
        return self.members.count()

    @property
    def max_members(self):
        if self.group_type == 'family':
            return 5
        return None  # Enterprise has unlimited members
