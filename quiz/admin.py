from django.contrib import admin
from .models import (
    Question, QuestionChoice, ShortAnswer,
    Quiz, QuizAttempt, QuestionAttempt
)


class QuestionChoiceInline(admin.TabularInline):
    model = QuestionChoice
    extra = 4
    max_num = 6


class ShortAnswerInline(admin.TabularInline):
    model = ShortAnswer
    extra = 1
    max_num = 5


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'question_type', 'curriculum', 'class_level', 'subject', 'topic', 'difficulty', 'is_active')
    list_filter = (
        'question_type', 'difficulty', 'is_active', 'is_premium',
        'curriculum', 'class_level', 'subject', 'branch', 'topic'
    )
    search_fields = ('text',)
    inlines = [QuestionChoiceInline, ShortAnswerInline]

    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Question Text'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'quiz_type', 'curriculum', 'class_level', 'subject', 'topic', 'question_count', 'per_question_time', 'is_active')
    list_filter = ('quiz_type', 'is_active', 'is_premium', 'curriculum', 'class_level', 'subject')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'quiz_type')
        }),
        ('Curriculum', {
            'fields': ('curriculum', 'class_level', 'subject', 'branch', 'topic')
        }),
        ('Settings', {
            'fields': ('question_count', 'per_question_time', 'randomize_questions', 'randomize_choices', 'passing_score')
        }),
        ('Status', {
            'fields': ('is_active', 'is_premium', 'created_by')
        }),
    )


class QuestionAttemptInline(admin.TabularInline):
    model = QuestionAttempt
    extra = 0
    readonly_fields = ('question', 'selected_choice', 'provided_answer', 'is_correct', 'answered_at', 'time_spent', 'timed_out')
    can_delete = False
    max_num = 0


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'status', 'score_percentage', 'started_at', 'completed_at', 'duration')
    list_filter = ('status', 'quiz__curriculum', 'quiz__class_level', 'quiz__subject', 'started_at')
    search_fields = ('user__email', 'quiz__title')
    readonly_fields = ('user', 'quiz', 'status', 'started_at', 'completed_at', 'score', 'total_questions', 'correct_answers')
    inlines = [QuestionAttemptInline]

    def has_add_permission(self, request):
        return False
