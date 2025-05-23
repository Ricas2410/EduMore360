"""
Services for the quiz app.
This module contains business logic for the quiz app.
"""

import random
from django.db.models import Count, Q, F, Case, When, Value, IntegerField
from django.utils import timezone

from .models import Question, Quiz, QuizAttempt, QuestionAttempt


class QuestionRandomizer:
    """Service for randomizing questions for quizzes."""

    @staticmethod
    def get_questions_for_quiz(quiz, user, question_count=None):
        """
        Get randomized questions for a quiz based on quiz settings and user's history.

        Args:
            quiz: The Quiz object
            user: The User object
            question_count: Optional override for the number of questions

        Returns:
            A queryset of Question objects
        """
        if question_count is None:
            question_count = quiz.question_count

        # Limit questions to prevent memory issues (max 30)
        question_count = min(question_count, 30)

        # Base query to get questions for this quiz
        if quiz.quiz_type == 'general':
            # For general quizzes, get questions from the subject
            questions = Question.objects.filter(
                curriculum=quiz.curriculum,
                class_level=quiz.class_level,
                subject=quiz.subject,
                is_active=True
            )
        else:
            # For topic quizzes, get questions from the specific topic
            questions = Question.objects.filter(
                curriculum=quiz.curriculum,
                class_level=quiz.class_level,
                subject=quiz.subject,
                topic=quiz.topic,
                is_active=True
            )

        # Filter out premium questions if user is not premium
        if not user.is_premium:
            questions = questions.filter(is_premium=False)

        # If there aren't enough questions, return all available
        if questions.count() <= question_count:
            return questions

        # Get user's question history
        user_attempts = QuestionAttempt.objects.filter(
            quiz_attempt__user=user,
            question__in=questions
        ).select_related('question')

        # Get questions the user has attempted before
        attempted_question_ids = user_attempts.values_list('question_id', flat=True)

        # Get questions the user has answered incorrectly
        incorrect_question_ids = user_attempts.filter(is_correct=False).values_list('question_id', flat=True)

        # Calculate weights for each question
        # 1. Prioritize questions the user has never seen
        # 2. Then questions the user has answered incorrectly
        # 3. Then questions by difficulty (if user is doing well, give harder questions)

        # Get user's overall performance
        correct_count = user_attempts.filter(is_correct=True).count()
        total_count = user_attempts.count()
        success_rate = correct_count / total_count if total_count > 0 else 0.5

        # Annotate questions with weights
        questions = questions.annotate(
            # Has the user attempted this question before?
            attempted=Case(
                When(id__in=attempted_question_ids, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
            # Has the user answered this question incorrectly?
            incorrect=Case(
                When(id__in=incorrect_question_ids, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
            # Difficulty weight
            difficulty_weight=Case(
                When(difficulty='easy', then=Value(1)),
                When(difficulty='medium', then=Value(2)),
                When(difficulty='hard', then=Value(3)),
                default=Value(2),
                output_field=IntegerField()
            )
        )

        # Calculate the final weight for each question
        # This is a complex formula that balances:
        # - Showing new questions
        # - Reviewing incorrect questions
        # - Adjusting difficulty based on performance

        # If user is doing well (>70% correct), prioritize harder questions and new questions
        # If user is struggling (<50% correct), prioritize easier questions and review incorrect ones
        if success_rate > 0.7:
            # User is doing well, prioritize harder questions and new content
            questions = questions.order_by('attempted', '-difficulty_weight', '?')
        elif success_rate < 0.5:
            # User is struggling, prioritize easier questions and review incorrect ones
            questions = questions.order_by('-incorrect', 'difficulty_weight', '?')
        else:
            # Balanced approach
            questions = questions.order_by('attempted', '-incorrect', '?')

        # Return the requested number of questions
        return questions[:question_count]

    @staticmethod
    def randomize_choices(question, seed=None):
        """
        Randomize the choices for a multiple-choice question.

        Args:
            question: The Question object
            seed: Optional random seed for reproducible randomization

        Returns:
            A list of QuestionChoice objects in random order
        """
        if question.question_type != 'multiple_choice':
            return []

        choices = list(question.choices.all())

        if seed is not None:
            random.seed(seed)

        random.shuffle(choices)
        return choices


class QuizService:
    """Service for managing quizzes."""

    @staticmethod
    def create_quiz_attempt(user, quiz):
        """
        Create a new quiz attempt for a user.

        Args:
            user: The User object
            quiz: The Quiz object

        Returns:
            A new QuizAttempt object
        """
        # Get randomized questions with memory optimization
        questions = QuestionRandomizer.get_questions_for_quiz(quiz, user)

        # Limit questions to prevent memory issues (max 30 questions)
        max_questions = min(quiz.question_count, 30, questions.count())

        # Create the quiz attempt
        quiz_attempt = QuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            status='in_progress',
            total_questions=max_questions
        )

        return quiz_attempt

    @staticmethod
    def get_next_question(quiz_attempt):
        """
        Get the next unanswered question for a quiz attempt.

        Args:
            quiz_attempt: The QuizAttempt object

        Returns:
            A Question object or None if all questions have been answered
        """
        # Get the quiz
        quiz = quiz_attempt.quiz

        # Find questions that haven't been attempted yet
        attempted_questions = QuestionAttempt.objects.filter(
            quiz_attempt=quiz_attempt
        ).values_list('question_id', flat=True)

        # Get all questions for this quiz that haven't been attempted yet
        if quiz.quiz_type == 'general':
            # For general quizzes, get questions from the subject
            unattempted_questions = Question.objects.filter(
                curriculum=quiz.curriculum,
                class_level=quiz.class_level,
                subject=quiz.subject,
                is_active=True
            ).exclude(id__in=attempted_questions)
        elif quiz.quiz_type == 'practice':
            # For practice exams, we've already created question attempts for all questions
            # So if there are no unattempted questions, return None
            return None
        else:
            # For topic quizzes, get questions from the specific topic
            unattempted_questions = Question.objects.filter(
                curriculum=quiz.curriculum,
                class_level=quiz.class_level,
                subject=quiz.subject,
                topic=quiz.topic,
                is_active=True
            ).exclude(id__in=attempted_questions)

        # Filter out premium questions if user is not premium
        if not quiz_attempt.user.is_premium:
            unattempted_questions = unattempted_questions.filter(is_premium=False)

        # Limit to the number of questions needed
        total_needed = quiz_attempt.total_questions - QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt).count()
        if total_needed <= 0:
            return None

        if unattempted_questions.exists():
            # If randomize_questions is True, return a random question
            if quiz.randomize_questions:
                return unattempted_questions.order_by('?').first()
            else:
                return unattempted_questions.first()

        return None

    @staticmethod
    def create_practice_exam(user, curriculum, class_level, subject, topics=None, question_count=40):
        """
        Create a practice exam for a user.

        Args:
            user: The User object
            curriculum: The Curriculum object
            class_level: The ClassLevel object
            subject: The Subject object
            topics: Optional list of Topic objects to include
            question_count: Number of questions to include

        Returns:
            A new QuizAttempt object
        """
        # Create a practice exam quiz
        quiz = Quiz.objects.create(
            title=f"Practice Exam - {subject.name}",
            description=f"Practice exam for {subject.name}",
            quiz_type='practice',
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            question_count=question_count,
            per_question_time=30,  # 30 seconds per question
            randomize_questions=True,
            randomize_choices=True,
            show_immediate_feedback=True,
            passing_score=70,
            is_active=True,
            created_by=user if user.is_staff else None,
        )

        # Create a new quiz attempt
        quiz_attempt = QuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            status='in_progress',
            total_questions=question_count
        )

        # Get questions for the practice exam
        if topics:
            # Get questions from selected topics
            topic_ids = [topic.id for topic in topics]
            questions = Question.objects.filter(
                curriculum=curriculum,
                class_level=class_level,
                subject=subject,
                topic_id__in=topic_ids,
                is_active=True
            )
        else:
            # Get questions from all topics in the subject
            questions = Question.objects.filter(
                curriculum=curriculum,
                class_level=class_level,
                subject=subject,
                is_active=True
            )

        # Filter out premium questions if user is not premium
        if not user.is_premium:
            questions = questions.filter(is_premium=False)

        # Randomize and limit to question count
        questions = list(questions.order_by('?')[:question_count])

        # If no questions are available, adjust the total_questions
        if not questions:
            quiz_attempt.total_questions = 0
            quiz_attempt.save()
            return quiz_attempt

        # Update total_questions to match actual number of questions
        quiz_attempt.total_questions = len(questions)
        quiz_attempt.save()

        # Create question attempts for each question
        for question in questions:
            QuestionAttempt.objects.create(
                quiz_attempt=quiz_attempt,
                question=question
            )

        return quiz_attempt
