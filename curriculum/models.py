from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django_summernote.fields import SummernoteTextField
from django.conf import settings


class Curriculum(models.Model):
    """Model representing a curriculum standard (e.g., US, Ghana)."""

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Curricula"
        ordering = ['name']

    def __str__(self):
        return self.name


class ClassLevel(models.Model):
    """Model representing a grade or class level (e.g., Grade 1, SHS 2)."""

    name = models.CharField(max_length=100)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='class_levels')
    level_order = models.PositiveIntegerField(help_text="Order of this class level within the curriculum")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['curriculum', 'level_order']
        unique_together = ['curriculum', 'level_order']

    def __str__(self):
        return f"{self.curriculum.name} - {self.name}"


class Subject(models.Model):
    """Model representing a subject (e.g., Mathematics, Science)."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='subjects')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='subject_icons/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['curriculum', 'class_level', 'name']

    def __str__(self):
        return f"{self.name} ({self.class_level.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.class_level.name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for this subject."""
        return reverse('curriculum:subject_detail', kwargs={
            'curriculum_code': self.curriculum.code,
            'class_level_id': self.class_level.id,
            'subject_slug': self.slug,
        })


class Branch(models.Model):
    """Model representing a branch of a subject (e.g., Biology, Chemistry for Science)."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='branches')
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='branch_icons/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['subject', 'name']
        verbose_name_plural = "Branches"

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.subject.slug}-{self.name}")
        super().save(*args, **kwargs)


class Topic(models.Model):
    """Model representing a topic within a subject or branch."""

    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='topics', null=True, blank=True)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    order = models.PositiveIntegerField(default=0, help_text="Order of this topic within the subject/branch")
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='postrequisites')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        unique_together = ['subject', 'branch', 'name']

    def __str__(self):
        if self.branch:
            return f"{self.subject.name} - {self.branch.name} - {self.name}"
        return f"{self.subject.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.branch:
                self.slug = slugify(f"{self.branch.slug}-{self.name}")
            else:
                self.slug = slugify(f"{self.subject.slug}-{self.name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for this topic."""
        return reverse('curriculum:topic_detail', kwargs={
            'curriculum_code': self.subject.curriculum.code,
            'class_level_id': self.subject.class_level.id,
            'subject_slug': self.subject.slug,
            'topic_slug': self.slug,
        })

    def get_difficulty_badge(self):
        """Get the badge color for the difficulty level."""
        if self.difficulty == 'beginner':
            return 'success'
        elif self.difficulty == 'intermediate':
            return 'warning'
        else:  # advanced
            return 'error'


class SubTopic(models.Model):
    """Model representing a sub-topic within a topic."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of this sub-topic within the topic")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        unique_together = ['topic', 'name']
        verbose_name = "Sub-Topic"
        verbose_name_plural = "Sub-Topics"

    def __str__(self):
        return f"{self.topic.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.topic.slug}-{self.name}")
        super().save(*args, **kwargs)


class Note(models.Model):
    """Model representing educational notes/lessons for a topic or sub-topic."""

    FILE_TYPE_CHOICES = (
        ('none', 'No File'),
        ('pdf', 'PDF Document'),
        ('ppt', 'PowerPoint Presentation'),
        ('doc', 'Word Document'),
        ('other', 'Other Document'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    content = SummernoteTextField()
    summary = models.TextField(blank=True, help_text="A brief summary of the note content")

    # File fields
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='none')
    pdf_document = models.FileField(upload_to='notes/pdfs/', null=True, blank=True,
                                   help_text="Upload a PDF document for this note")
    ppt_document = models.FileField(upload_to='notes/ppts/', null=True, blank=True,
                                   help_text="Upload a PowerPoint presentation for this note")
    doc_document = models.FileField(upload_to='notes/docs/', null=True, blank=True,
                                   help_text="Upload a Word document for this note")
    other_document = models.FileField(upload_to='notes/others/', null=True, blank=True,
                                     help_text="Upload any other document for this note")

    extracted_text = models.TextField(blank=True, help_text="Text extracted from uploaded documents")
    allow_download = models.BooleanField(default=False,
                                        help_text="If checked, users will be able to download the document")
    is_premium = models.BooleanField(default=False, help_text="Whether this note is only available to premium users")
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of this note within the topic/subtopic")
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_notes')
    updated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='updated_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ['topic', 'subtopic', 'title']

    def __str__(self):
        if self.subtopic:
            return f"{self.topic.name} - {self.subtopic.name} - {self.title}"
        return f"{self.topic.name} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.subtopic:
                self.slug = slugify(f"{self.subtopic.slug}-{self.title}")
            else:
                self.slug = slugify(f"{self.topic.slug}-{self.title}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for this note."""
        return reverse('quiz:study_mode', kwargs={
            'curriculum_code': self.topic.subject.curriculum.code,
            'class_level_id': self.topic.subject.class_level.id,
            'subject_slug': self.topic.subject.slug,
            'topic_slug': self.topic.slug,
            'note_id': self.id,
        })

    @property
    def has_file(self):
        """Check if the note has any document attached."""
        return self.file_type != 'none'

    @property
    def document_url(self):
        """Get the URL of the attached document based on file type."""
        if self.file_type == 'pdf' and self.pdf_document:
            return self.pdf_document.url
        elif self.file_type == 'ppt' and self.ppt_document:
            return self.ppt_document.url
        elif self.file_type == 'doc' and self.doc_document:
            return self.doc_document.url
        elif self.file_type == 'other' and self.other_document:
            return self.other_document.url
        return None

    @property
    def has_pdf(self):
        """Check if this note has a PDF document attached."""
        return bool(self.pdf_document)


class Attachment(models.Model):
    """Model for file attachments to notes."""

    FILE_TYPE_CHOICES = (
        ('pdf', 'PDF Document'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    )

    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='attachments')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='note_attachments/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note.title} - {self.title}"


class NoteCompletion(models.Model):
    """Model to track which notes a user has completed."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='completed_notes')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='completions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'note']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.note.title}"
