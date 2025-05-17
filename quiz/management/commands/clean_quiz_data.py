from django.core.management.base import BaseCommand
from quiz.models import Quiz, Question, QuestionChoice, ShortAnswer, QuizAttempt, QuestionAttempt
from django.db import transaction


class Command(BaseCommand):
    help = 'Cleans up quiz data by removing all quizzes, questions, and related data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--remove-id-suffix',
            action='store_true',
            help='Remove [ID:xxx] suffix from question text instead of deleting questions',
        )

    def handle(self, *args, **options):
        remove_id_suffix = options['remove_id_suffix']

        if remove_id_suffix:
            self.remove_id_suffix_from_questions()
        else:
            self.delete_all_quiz_data()

    @transaction.atomic
    def delete_all_quiz_data(self):
        """Delete all quiz-related data from the database."""
        # First, delete all quiz attempts and question attempts
        question_attempt_count = QuestionAttempt.objects.count()
        QuestionAttempt.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {question_attempt_count} question attempts'))

        quiz_attempt_count = QuizAttempt.objects.count()
        QuizAttempt.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {quiz_attempt_count} quiz attempts'))

        # Delete all quizzes
        quiz_count = Quiz.objects.count()
        Quiz.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {quiz_count} quizzes'))

        # Delete all question choices and short answers
        choice_count = QuestionChoice.objects.count()
        QuestionChoice.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {choice_count} question choices'))

        short_answer_count = ShortAnswer.objects.count()
        ShortAnswer.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {short_answer_count} short answers'))

        # Finally, delete all questions
        question_count = Question.objects.count()
        Question.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {question_count} questions'))

        self.stdout.write(self.style.SUCCESS('Successfully cleaned up all quiz data'))

    @transaction.atomic
    def remove_id_suffix_from_questions(self):
        """Remove [ID:xxx] suffix from question text."""
        import re
        
        # Regular expression to match [ID:xxx] pattern
        id_pattern = re.compile(r'\s*\[ID:[a-f0-9]{8}\].*$')
        
        # Get all questions with [ID:xxx] suffix
        questions_with_suffix = Question.objects.filter(text__contains='[ID:')
        count = questions_with_suffix.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No questions found with [ID:xxx] suffix'))
            return
        
        # Update each question to remove the suffix
        updated_count = 0
        for question in questions_with_suffix:
            original_text = question.text
            new_text = re.sub(id_pattern, '', original_text)
            
            if new_text != original_text:
                question.text = new_text
                question.save()
                updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} questions to remove [ID:xxx] suffix'))
