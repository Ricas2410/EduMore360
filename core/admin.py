from django.contrib import admin
from .models import (
    SystemConfiguration, Notification, UserProgress,
    UserAchievement, HeroSection, KidFriendlyTheme
)


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    """Admin configuration for the SystemConfiguration model."""

    fieldsets = (
        ('General Settings', {
            'fields': ('site_name', 'site_description', 'maintenance_mode')
        }),
        ('Email Settings', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_use_tls', 'smtp_username', 'smtp_password', 'default_from_email')
        }),
        ('Session Settings', {
            'fields': ('enforce_single_session', 'session_timeout_minutes')
        }),
        ('Registration Settings', {
            'fields': ('allow_registration', 'require_email_verification')
        }),
        ('Social Login Settings', {
            'fields': ('enable_google_login',)
        }),
        ('Payment Settings', {
            'fields': ('paystack_secret_key', 'paystack_public_key', 'currency')
        }),
        ('Metadata', {
            'fields': ('updated_at', 'updated_by')
        }),
    )
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Only allow one instance of SystemConfiguration
        return SystemConfiguration.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the SystemConfiguration
        return False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin configuration for the Notification model."""

    list_display = ('user', 'title', 'notification_type', 'category', 'is_read', 'created_at')
    list_filter = ('notification_type', 'category', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('created_at',)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    """Admin configuration for the UserProgress model."""

    list_display = ('user', 'curriculum', 'class_level', 'subject', 'topic', 'completion_percentage', 'last_activity')
    list_filter = ('curriculum', 'class_level', 'subject', 'completion_percentage', 'last_activity')
    search_fields = ('user__email', 'topic__name', 'subtopic__name')
    readonly_fields = ('last_activity',)
    filter_horizontal = ('notes_viewed',)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """Admin configuration for the UserAchievement model."""

    list_display = ('user', 'title', 'achievement_type', 'points', 'earned_at')
    list_filter = ('achievement_type', 'earned_at')
    search_fields = ('user__email', 'title', 'description')
    readonly_fields = ('earned_at',)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    """Admin configuration for the HeroSection model."""

    list_display = ('title', 'position', 'target_audience', 'is_active', 'display_order')
    list_filter = ('position', 'target_audience', 'is_active', 'animation_enabled', 'use_bright_colors')
    search_fields = ('title', 'subtitle', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Visual Elements', {
            'fields': ('background_image', 'foreground_image', 'mascot_image', 'mascot_name')
        }),
        ('Call to Action', {
            'fields': ('cta_text', 'cta_url')
        }),
        ('Display Settings', {
            'fields': ('position', 'target_audience', 'animation_enabled', 'use_bright_colors',
                      'is_active', 'display_order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(KidFriendlyTheme)
class KidFriendlyThemeAdmin(admin.ModelAdmin):
    """Admin configuration for the KidFriendlyTheme model."""

    list_display = ('name', 'theme_type', 'min_grade', 'max_grade', 'is_active', 'is_default')
    list_filter = ('theme_type', 'is_active', 'is_default', 'min_grade', 'max_grade')
    search_fields = ('name', 'mascot_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'theme_type', 'is_active', 'is_default')
        }),
        ('Color Scheme', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        ('Visual Elements', {
            'fields': ('background_image', 'header_image', 'footer_image', 'mascot_image', 'mascot_name')
        }),
        ('UI Settings', {
            'fields': ('use_rounded_corners', 'use_animations', 'use_sound_effects')
        }),
        ('Grade Level Targeting', {
            'fields': ('min_grade', 'max_grade')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
