from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard, name='dashboard'),
    path('real-time/', views.real_time_analytics, name='real_time'),
    path('countries/', views.country_analytics, name='countries'),
]
