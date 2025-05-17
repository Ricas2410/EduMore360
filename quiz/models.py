from django.db import models
from django.utils import timezone
from django_summernote.fields import SummernoteTextField


class Question(models.Model):
    """Model representing a quiz question."""

    QUESTION_TYPE_CHOICES = (
        ('multiple_choice', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
    )

    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    # Temporarily using TextField instead of SummernoteTextField
    text = models.TextField(verbose_name="Question Text")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='multiple_choice')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    # Temporarily using TextField instead of SummernoteTextField
    explanation = models.TextField(verbose_name="Explanation", help_text="Explanation shown when the answer is incorrect")

    # Curriculum relationships
    curriculum = models.ForeignKey('curriculum.Curriculum', on_delete=models.CASCADE, related_name='questions')
    class_level = models.ForeignKey('curriculum.ClassLevel', on_delete=models.CASCADE, related_name='questions')
    subject = models.ForeignKey('curriculum.Subject', on_delete=models.CASCADE, related_name='questions')
    branch = models.ForeignKey('curriculum.Branch', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    topic = models.ForeignKey('curriculum.Topic', on_delete=models.CASCADE, related_name='questions')
    subtopic = models.ForeignKey('curriculum.SubTopic', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)

    # Meta fields
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.text[:50] + ('...' if len(self.text) > 50 else '')

    @property
    def correct_answer(self):
        """Return the correct answer for this question."""
        if self.question_type == 'multiple_choice':
            try:
                return self.choices.get(is_correct=True)
            except (self.choices.model.DoesNotExist, self.choices.model.MultipleObjectsReturned):
                return None
        else:  # short_answer
            try:
                return self.short_answers.first()
            except AttributeError:
                return None


class QuestionChoice(models.Model):
    """Model representing a choice for a multiple-choice question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"


class ShortAnswer(models.Model):
    """Model representing acceptable answers for a short-answer question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='short_answers')
    text = models.CharField(max_length=255)
    is_exact_match = models.BooleanField(default=True, help_text="If true, the answer must match exactly. If false, fuzzy matching is used.")

    def __str__(self):
        return self.text


class Quiz(models.Model):
    """Model representing a quiz configuration."""

    QUIZ_TYPE_CHOICES = (
        ('general', 'General Quiz'),
        ('topic', 'Topic-Based Quiz'),
        ('practice', 'Practice Exam'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES, default='general')

    # Curriculum relationships (for filtering questions)
    curriculum = models.ForeignKey('curriculum.Curriculum', on_delete=models.CASCADE, related_name='quizzes')
    class_level = models.ForeignKey('curriculum.ClassLevel', on_delete=models.CASCADE, related_name='quizzes')
    subject = models.ForeignKey('curriculum.Subject', on_delete=models.CASCADE, related_name='quizzes')
    branch = models.ForeignKey('curriculum.Branch', on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    topic = models.ForeignKey('curriculum.Topic', on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)

    # Quiz settings
    question_count = models.PositiveIntegerField(default=40, help_text="Number of questions to include in the quiz (default: 40)")
    per_question_time = models.PositiveIntegerField(default=30, help_text="Time limit in seconds per question (default: 30 seconds)")
    randomize_questions = models.BooleanField(default=True, help_text="Randomize the order of questions")
    randomize_choices = models.BooleanField(default=True, help_text="Randomize the order of answer choices")
    show_immediate_feedback = models.BooleanField(default=True, help_text="Show immediate feedback after each question")
    passing_score = models.PositiveIntegerField(default=70, help_text="Passing score percentage")

    # Meta fields
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False, help_text="Featured quizzes are shown on the home page")
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class QuizAttempt(models.Model):
    """Model representing a user's attempt at a quiz."""

    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('timed_out', 'Timed Out'),
        ('abandoned', 'Abandoned'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    # Timing information
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Results
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} ({self.started_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def score_percentage(self):
        """Calculate the score as a percentage."""
        if self.total_questions == 0:
            return 0
        return round((self.correct_answers / self.total_questions) * 100)

    @property
    def is_passed(self):
        """Check if the quiz attempt is passed."""
        return self.score_percentage >= self.quiz.passing_score

    @property
    def duration(self):
        """Calculate the duration of the quiz attempt."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds() // 60
        return (timezone.now() - self.started_at).total_seconds() // 60

    def complete(self):
        """Mark the quiz attempt as completed."""
        if self.status == 'in_progress':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()


class QuestionAttempt(models.Model):
    """Model representing a user's attempt at a specific question within a quiz."""

    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='question_attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempts')

    # For multiple-choice questions
    selected_choice = models.ForeignKey(QuestionChoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='selections')

    # For short-answer questions
    provided_answer = models.CharField(max_length=255, blank=True)

    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.PositiveIntegerField(default=0, help_text="Time spent on this question in seconds")
    timed_out = models.BooleanField(default=False, help_text="Whether the user ran out of time for this question")

    class Meta:
        ordering = ['answered_at']

    def __str__(self):
        return f"{self.quiz_attempt.user.email} - {self.question.text[:30]}"
