from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Profile management
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),

    # Preferences
    path('preferences/', views.preferences, name='preferences'),
    path('preferences/curriculum/', views.set_curriculum_preference, name='set_curriculum_preference'),
    path('preferences/class-level/', views.set_class_level_preference, name='set_class_level_preference'),
    path('preferences/get-class-levels/', views.get_class_levels, name='get_class_levels'),
    path('preferences/set-notification-preferences/', views.set_notification_preferences, name='set_notification_preferences'),
    path('preferences/set-subject-preferences/', views.set_subject_preferences, name='set_subject_preferences'),

    # Progress tracking
    path('progress/', views.progress_overview, name='progress_overview'),
    path('progress/subject/<slug:subject_slug>/', views.subject_progress, name='subject_progress'),
    path('progress/topic/<slug:topic_slug>/', views.topic_progress, name='topic_progress'),
]
