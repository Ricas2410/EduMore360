"""
URL configuration for minimal health check app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.health, name='health'),
]
