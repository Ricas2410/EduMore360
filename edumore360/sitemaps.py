from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from curriculum.models import Course, Lesson
from quiz.models import Quiz

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about', 'contact', 'courses', 'pricing']

    def location(self, item):
        return reverse(item)

class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Course.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

class LessonSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Lesson.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

class QuizSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Quiz.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
