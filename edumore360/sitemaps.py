from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from curriculum.models import Subject, Topic, Note
from quiz.models import Quiz

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about', 'contact', 'courses', 'pricing']

    def location(self, item):
        return reverse(item)

class SubjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Subject.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

class TopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Topic.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

class NoteSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Note.objects.filter(is_published=True, is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

class QuizSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Quiz.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
