from django.core.management.base import BaseCommand
from quiz.models import Question, QuestionChoice, ShortAnswer
from django.db import transaction
import re


class Command(BaseCommand):
    help = 'Identifies and removes duplicate questions based on the first few words'

    def add_arguments(self, parser):
        parser.add_argument(
            '--word-count',
            type=int,
            default=5,
            help='Number of words to compare for identifying duplicates (default: 5)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Only identify duplicates without removing them',
        )
        parser.add_argument(
            '--curriculum',
            type=str,
            help='Filter by curriculum code (e.g., GH)',
        )
        parser.add_argument(
            '--class-level',
            type=str,
            help='Filter by class level name (e.g., SHS 2)',
        )
        parser.add_argument(
            '--subject',
            type=str,
            help='Filter by subject name (e.g., Mathematics)',
        )

    def handle(self, *args, **options):
        word_count = options['word_count']
        dry_run = options['dry_run']
        curriculum = options['curriculum']
        class_level = options['class_level']
        subject = options['subject']

        # Start with all questions
        questions = Question.objects.all()

        # Apply filters if provided
        if curriculum:
            questions = questions.filter(curriculum__code=curriculum)
        if class_level:
            questions = questions.filter(class_level__name=class_level)
        if subject:
            questions = questions.filter(subject__name=subject)

        # Get total count for reporting
        total_questions = questions.count()
        self.stdout.write(f"Processing {total_questions} questions...")

        # Group questions by their first N words
        question_groups = {}
        for question in questions:
            # Clean the text (remove HTML tags, extra spaces, etc.)
            clean_text = self.clean_text(question.text)

            # Use the entire question text instead of just the first few words
            # This ensures only exact duplicates are removed

            # Add to the appropriate group
            key = (
                question.curriculum_id,
                question.class_level_id,
                question.subject_id,
                question.topic_id,
                clean_text.lower()  # Use lowercase for case-insensitive comparison
            )

            if key not in question_groups:
                question_groups[key] = []

            question_groups[key].append(question)

        # Find groups with duplicates
        duplicate_groups = {k: v for k, v in question_groups.items() if len(v) > 1}

        # Report findings
        duplicate_count = sum(len(group) - 1 for group in duplicate_groups.values())
        self.stdout.write(f"Found {len(duplicate_groups)} groups with duplicates, totaling {duplicate_count} duplicate questions")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN: No questions were removed"))

            # Print some examples of duplicates
            self.stdout.write("\nExamples of duplicate questions:")
            for i, (key, group) in enumerate(list(duplicate_groups.items())[:5]):
                self.stdout.write(f"\nGroup {i+1} (based on: '{key[4]}')")
                for j, q in enumerate(group):
                    self.stdout.write(f"  {j+1}. {q.text[:100]}{'...' if len(q.text) > 100 else ''}")

            return

        # Remove duplicates
        removed_count = 0
        with transaction.atomic():
            for key, group in duplicate_groups.items():
                # Keep the first question, remove the rest
                keep = group[0]
                remove = group[1:]

                for question in remove:
                    # Delete related choices and answers
                    QuestionChoice.objects.filter(question=question).delete()
                    ShortAnswer.objects.filter(question=question).delete()

                    # Delete the question
                    question.delete()
                    removed_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully removed {removed_count} duplicate questions"))
        self.stdout.write(f"Remaining questions: {total_questions - removed_count}")

    def clean_text(self, text):
        """Clean text by removing HTML tags, extra spaces, and special characters."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Remove special characters and extra spaces
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Remove any [ID:xxx] suffixes
        text = re.sub(r'\s*\[ID:[a-f0-9]{8}\].*$', '', text)

        return text.lower()  # Convert to lowercase for better matching
