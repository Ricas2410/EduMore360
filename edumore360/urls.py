"""
URL configuration for edumore360 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-admin/', include('my_admin.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('', include('core.urls')),
    path('curriculum/', include('curriculum.urls')),
    path('quiz/', include('quiz.urls')),
    path('subscription/', include('subscription.urls')),
    path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
