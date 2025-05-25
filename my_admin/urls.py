from django.urls import path, include
from . import views

app_name = 'my_admin'

urlpatterns = [
    # Authentication URLs
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('quiz/', views.quiz_management, name='quiz_management'),
    path('quiz/', include('quiz.admin_urls', namespace='quiz_admin')),
    path('users/', views.user_management, name='user_management'),
    path('curriculum/', views.curriculum_management, name='curriculum_management'),
    path('curriculum/add-curriculum/', views.add_curriculum, name='add_curriculum'),
    path('curriculum/add-class-level/', views.add_class_level, name='add_class_level'),
    path('curriculum/add-subject/', views.add_subject, name='add_subject'),
    path('curriculum/add-topic/', views.add_topic, name='add_topic'),
    path('curriculum/edit-curriculum/<int:curriculum_id>/', views.edit_curriculum, name='edit_curriculum'),
    path('subscriptions/', views.subscription_management, name='subscription_management'),
    path('subscriptions/add/', views.add_subscription, name='add_subscription'),
    path('subscriptions/edit/<int:subscription_id>/', views.edit_subscription, name='edit_subscription'),
    path('subscriptions/renew/<int:subscription_id>/', views.renew_subscription, name='renew_subscription'),

    # Notes Management URLs
    path('notes/', views.notes_management, name='notes_management'),
    path('notes/add/', views.add_note_page, name='add_note_page'),
    path('notes/create/', views.add_note, name='add_note'),
    path('notes/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('notes/upload-file/<int:note_id>/', views.upload_note_file, name='upload_note_file'),
    path('notes/get-topics/', views.get_topics_for_notes, name='get_topics_for_notes'),
    path('notes/get-subtopics/', views.get_subtopics_for_notes, name='get_subtopics_for_notes'),

    # Analytics URLs
    path('analytics/', include('analytics.urls')),

    # Help Center
    path('help/', views.help_center, name='help_center'),

    # Site Settings URLs
    path('settings/general/', views.site_settings_general, name='site_settings_general'),
    path('settings/email/', views.site_settings_email, name='site_settings_email'),
    path('settings/email/test/', views.site_settings_test_email, name='site_settings_test_email'),
    path('settings/quiz/', views.site_settings_quiz, name='site_settings_quiz'),
    path('settings/payment/', views.site_settings_payment, name='site_settings_payment'),
]
