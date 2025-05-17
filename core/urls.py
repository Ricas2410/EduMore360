from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_of_service, name='terms_of_service'),
    path('faq/', views.faq, name='faq'),

    # Notification URLs
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/mark-read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/delete/<int:pk>/', views.delete_notification, name='delete_notification'),

    # User achievement URLs
    path('achievements/', views.achievement_list, name='achievement_list'),

    # Free user setup
    path('complete-setup/', views.complete_free_setup, name='complete_free_setup'),
]
