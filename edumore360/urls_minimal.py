"""
Minimal URL configuration for edumore360 project.
"""

from django.urls import path, include

urlpatterns = [
    path('health/', include('minimal_health.urls')),
]
