from django.contrib import admin
from .models import (
    Curriculum, ClassLevel, Subject, Branch,
    Topic, SubTopic, Note, Attachment
)


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)


@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'curriculum', 'level_order', 'is_active')
    list_filter = ('curriculum', 'is_active')
    search_fields = ('name',)
    ordering = ('curriculum', 'level_order')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'curriculum', 'class_level', 'is_active')
    list_filter = ('curriculum', 'class_level', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'is_active')
    list_filter = ('subject__curriculum', 'subject__class_level', 'subject', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'branch', 'difficulty', 'order', 'is_active')
    list_filter = ('subject__curriculum', 'subject__class_level', 'subject', 'branch', 'difficulty', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('prerequisites',)


@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'order', 'is_active')
    list_filter = ('topic__subject__curriculum', 'topic__subject__class_level', 'topic__subject', 'topic', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'subtopic', 'is_premium', 'is_published', 'created_by', 'updated_at')
    list_filter = (
        'topic__subject__curriculum',
        'topic__subject__class_level',
        'topic__subject',
        'topic',
        'is_premium',
        'is_published'
    )
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AttachmentInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'note', 'file_type', 'is_premium')
    list_filter = ('file_type', 'is_premium')
    search_fields = ('title', 'description', 'note__title')
