from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class PageView(models.Model):
    """Track page views and user behavior."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    # Page information
    path = models.CharField(max_length=500)
    page_title = models.CharField(max_length=200, blank=True)
    referrer = models.URLField(blank=True, null=True)
    
    # User information
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # Location information (will be populated by IP lookup)
    country = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    
    # Device information
    device_type = models.CharField(max_length=20, blank=True)  # mobile, tablet, desktop
    browser = models.CharField(max_length=50, blank=True)
    operating_system = models.CharField(max_length=50, blank=True)
    
    # Timing
    timestamp = models.DateTimeField(default=timezone.now)
    time_on_page = models.PositiveIntegerField(null=True, blank=True)  # seconds
    
    class Meta:
        db_table = 'analytics_pageview'
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['user']),
            models.Index(fields=['path']),
            models.Index(fields=['country']),
            models.Index(fields=['ip_address']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.path} - {self.timestamp}"


class QuizAnalytics(models.Model):
    """Track quiz-specific analytics."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE)
    
    # Quiz performance
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField(default=0)
    
    # User information
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'analytics_quiz'
        indexes = [
            models.Index(fields=['started_at']),
            models.Index(fields=['quiz']),
            models.Index(fields=['user']),
        ]
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.quiz.title} - {self.started_at}"


class UserSession(models.Model):
    """Track user sessions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, unique=True)
    
    # Session information
    started_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    # User information
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Session metrics
    page_views = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(null=True, blank=True)  # seconds
    
    class Meta:
        db_table = 'analytics_session'
        indexes = [
            models.Index(fields=['started_at']),
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
        ]
        ordering = ['-started_at']

    def __str__(self):
        return f"Session {self.session_key} - {self.started_at}"


class DailyStats(models.Model):
    """Daily aggregated statistics."""
    date = models.DateField(unique=True)
    
    # User metrics
    total_users = models.PositiveIntegerField(default=0)
    new_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    
    # Page metrics
    total_page_views = models.PositiveIntegerField(default=0)
    unique_page_views = models.PositiveIntegerField(default=0)
    
    # Quiz metrics
    quizzes_started = models.PositiveIntegerField(default=0)
    quizzes_completed = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(null=True, blank=True)
    
    # Geographic data (top countries)
    top_countries = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_daily_stats'
        ordering = ['-date']

    def __str__(self):
        return f"Stats for {self.date}"
