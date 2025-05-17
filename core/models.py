from django.db import models
from django.utils import timezone


class SystemConfiguration(models.Model):
    """Model for storing system-wide configuration settings."""

    # General settings
    site_name = models.CharField(max_length=100, default="EduMore360")
    site_description = models.TextField(blank=True)
    maintenance_mode = models.BooleanField(default=False)

    # Email settings
    smtp_host = models.CharField(max_length=100, default="smtp.gmail.com")
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_use_tls = models.BooleanField(default=True)
    smtp_username = models.CharField(max_length=100, default="skillnetservices@gmail.com")
    smtp_password = models.CharField(max_length=100, default="tdms ckdk tmgo fado")
    default_from_email = models.EmailField(default="skillnetservices@gmail.com")

    # Session settings
    enforce_single_session = models.BooleanField(default=False, help_text="If enabled, users can only be logged in from one device at a time")
    session_timeout_minutes = models.PositiveIntegerField(default=30, help_text="Session timeout in minutes")

    # Registration settings
    allow_registration = models.BooleanField(default=True)
    require_email_verification = models.BooleanField(default=True)

    # Social login settings
    enable_google_login = models.BooleanField(default=True)

    # Payment settings
    paystack_secret_key = models.CharField(max_length=100, blank=True)
    paystack_public_key = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=3, default="USD")
    enable_test_mode = models.BooleanField(default=True, help_text="Process payments in test mode")

    # Quiz settings
    quiz_feedback_time = models.PositiveIntegerField(default=7, help_text="Time in seconds to show feedback after answering a quiz question")
    quiz_show_immediate_feedback = models.BooleanField(default=True, help_text="Show immediate feedback after answering a quiz question")
    quiz_randomize_questions = models.BooleanField(default=True, help_text="Randomize the order of questions in quizzes")
    quiz_randomize_choices = models.BooleanField(default=True, help_text="Randomize the order of choices in multiple-choice questions")

    # Meta fields
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='system_config_updates')

    class Meta:
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configuration"

    def __str__(self):
        return "System Configuration"

    @classmethod
    def get_settings(cls):
        """Get the system settings, creating default settings if none exist."""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class Notification(models.Model):
    """Model for storing user notifications."""

    TYPE_CHOICES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )

    CATEGORY_CHOICES = (
        ('system', 'System'),
        ('subscription', 'Subscription'),
        ('content', 'Content'),
        ('quiz', 'Quiz'),
        ('account', 'Account'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    url = models.CharField(max_length=200, blank=True, help_text="URL to redirect to when notification is clicked")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        self.save()


class UserProgress(models.Model):
    """Model for tracking user progress through curriculum content."""

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='progress')

    # Curriculum relationships
    curriculum = models.ForeignKey('curriculum.Curriculum', on_delete=models.CASCADE, related_name='user_progress')
    class_level = models.ForeignKey('curriculum.ClassLevel', on_delete=models.CASCADE, related_name='user_progress')
    subject = models.ForeignKey('curriculum.Subject', on_delete=models.CASCADE, related_name='user_progress')
    topic = models.ForeignKey('curriculum.Topic', on_delete=models.CASCADE, related_name='user_progress')
    subtopic = models.ForeignKey('curriculum.SubTopic', on_delete=models.CASCADE, related_name='user_progress', null=True, blank=True)

    # Progress tracking
    notes_viewed = models.ManyToManyField('curriculum.Note', related_name='viewed_by')
    completion_percentage = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'curriculum', 'class_level', 'subject', 'topic', 'subtopic']
        ordering = ['-last_activity']

    def __str__(self):
        if self.subtopic:
            return f"{self.user.email} - {self.topic.name} - {self.subtopic.name}"
        return f"{self.user.email} - {self.topic.name}"

    def update_activity(self):
        """Update the last activity timestamp."""
        self.last_activity = timezone.now()
        self.save()


class UserAchievement(models.Model):
    """Model for tracking user achievements and badges."""

    ACHIEVEMENT_TYPE_CHOICES = (
        ('completion', 'Content Completion'),
        ('quiz', 'Quiz Performance'),
        ('streak', 'Learning Streak'),
        ('milestone', 'Learning Milestone'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES)
    icon = models.ImageField(upload_to='achievement_icons/', null=True, blank=True)
    points = models.PositiveIntegerField(default=0)
    earned_at = models.DateTimeField(auto_now_add=True)

    # Related content (optional)
    curriculum = models.ForeignKey('curriculum.Curriculum', on_delete=models.SET_NULL, null=True, blank=True)
    class_level = models.ForeignKey('curriculum.ClassLevel', on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey('curriculum.Subject', on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey('curriculum.Topic', on_delete=models.SET_NULL, null=True, blank=True)
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.email} - {self.title}"


class HeroSection(models.Model):
    """Model for customizable hero sections on the website."""

    POSITION_CHOICES = (
        ('home', 'Home Page'),
        ('dashboard', 'Student Dashboard'),
        ('subscription', 'Subscription Page'),
        ('curriculum', 'Curriculum Page'),
        ('quiz', 'Quiz Page'),
    )

    AUDIENCE_CHOICES = (
        ('all', 'All Users'),
        ('elementary', 'Elementary School (Grades 1-5)'),
        ('middle', 'Middle School (Grades 6-8)'),
        ('high', 'High School (Grades 9-12)'),
        ('parents', 'Parents'),
        ('teachers', 'Teachers'),
    )

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

    # Visual elements
    background_image = models.ImageField(upload_to='hero_backgrounds/', null=True, blank=True)
    foreground_image = models.ImageField(upload_to='hero_foregrounds/', null=True, blank=True)

    # Character/mascot for younger students
    mascot_image = models.ImageField(upload_to='mascots/', null=True, blank=True)
    mascot_name = models.CharField(max_length=50, blank=True)

    # Call to action
    cta_text = models.CharField(max_length=50, blank=True, help_text="Call to action button text")
    cta_url = models.CharField(max_length=200, blank=True, help_text="URL for the call to action button")

    # Positioning and audience
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='home')
    target_audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='all')

    # Animation and style options
    animation_enabled = models.BooleanField(default=True)
    use_bright_colors = models.BooleanField(default=True, help_text="Use bright, kid-friendly colors")

    # Status and ordering
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=1)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position', 'display_order']
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return f"{self.title} ({self.get_position_display()})"

    @classmethod
    def get_for_position(cls, position, audience='all'):
        """Get active hero sections for a specific position and audience."""
        return cls.objects.filter(
            position=position,
            is_active=True
        ).filter(
            models.Q(target_audience='all') | models.Q(target_audience=audience)
        ).order_by('display_order')


class NotificationPreferences(models.Model):
    """Model for storing user notification preferences."""

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='notification_preferences')

    # Email notification settings
    email_notifications = models.BooleanField(default=True, help_text="Receive notifications via email")
    quiz_reminders = models.BooleanField(default=True, help_text="Receive reminders for incomplete quizzes")
    new_content_notifications = models.BooleanField(default=True, help_text="Receive notifications when new content is added")
    achievement_notifications = models.BooleanField(default=True, help_text="Receive notifications when you earn new achievements")
    subscription_notifications = models.BooleanField(default=True, help_text="Receive notifications about your subscription status")

    # Push notification settings (for future mobile app)
    push_notifications = models.BooleanField(default=True, help_text="Receive push notifications on mobile devices")

    # Notification frequency
    notification_frequency = models.CharField(
        max_length=20,
        choices=(
            ('immediate', 'Immediate'),
            ('daily', 'Daily Digest'),
            ('weekly', 'Weekly Digest'),
        ),
        default='immediate'
    )

    # Meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notification Preferences"
        verbose_name_plural = "Notification Preferences"

    def __str__(self):
        return f"Notification Preferences for {self.user.email}"


class KidFriendlyTheme(models.Model):
    """Model for storing kid-friendly theme settings."""

    THEME_CHOICES = (
        ('default', 'Default Theme'),
        ('space', 'Space Adventure'),
        ('ocean', 'Ocean Explorer'),
        ('jungle', 'Jungle Safari'),
        ('dinosaur', 'Dinosaur World'),
        ('fantasy', 'Fantasy Kingdom'),
        ('science', 'Science Lab'),
    )

    name = models.CharField(max_length=100)
    theme_type = models.CharField(max_length=20, choices=THEME_CHOICES, default='default')

    # Color scheme
    primary_color = models.CharField(max_length=20, default="#4A6FFF")
    secondary_color = models.CharField(max_length=20, default="#FF6B6B")
    accent_color = models.CharField(max_length=20, default="#FFD166")

    # Background and elements
    background_image = models.ImageField(upload_to='theme_backgrounds/', null=True, blank=True)
    header_image = models.ImageField(upload_to='theme_headers/', null=True, blank=True)
    footer_image = models.ImageField(upload_to='theme_footers/', null=True, blank=True)

    # Mascot/character
    mascot_image = models.ImageField(upload_to='theme_mascots/', null=True, blank=True)
    mascot_name = models.CharField(max_length=50, blank=True)

    # Icons and UI elements
    use_rounded_corners = models.BooleanField(default=True)
    use_animations = models.BooleanField(default=True)
    use_sound_effects = models.BooleanField(default=False)

    # Grade level targeting
    min_grade = models.PositiveIntegerField(default=1)
    max_grade = models.PositiveIntegerField(default=12)

    # Status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Kid-Friendly Theme"
        verbose_name_plural = "Kid-Friendly Themes"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # If this theme is set as default, unset any other default themes
        if self.is_default:
            KidFriendlyTheme.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_theme_for_grade(cls, grade):
        """Get appropriate theme for a specific grade level."""
        return cls.objects.filter(
            is_active=True,
            min_grade__lte=grade,
            max_grade__gte=grade
        ).first() or cls.objects.filter(is_default=True, is_active=True).first()
