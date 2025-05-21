"""
URL configuration for edumore360 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from .sitemaps import StaticViewSitemap, SubjectSitemap, TopicSitemap, NoteSitemap, QuizSitemap

# Define sitemaps dictionary
sitemaps = {
    'static': StaticViewSitemap,
    'subjects': SubjectSitemap,
    'topics': TopicSitemap,
    'notes': NoteSitemap,
    'quizzes': QuizSitemap,
}

urlpatterns = [
    # Health check
    path('health/', include('minimal_health.urls')),  # Use the minimal health check app

    # Admin
    path('admin/', admin.site.urls),
    path('my-admin/', include('my_admin.urls')),

    # Authentication
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),

    # Third-party
    path('summernote/', include('django_summernote.urls')),

    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    # Main app URLs
    path('', include('core.urls')),
    path('curriculum/', include('curriculum.urls')),
    path('quiz/', include('quiz.urls')),
    path('subscription/', include('subscription.urls')),
    path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
