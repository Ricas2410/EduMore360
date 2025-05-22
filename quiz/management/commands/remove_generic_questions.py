from django.core.management.base import BaseCommand
from django.db import transaction
from quiz.models import Question, QuestionChoice


class Command(BaseCommand):
    help = 'Remove generic sample questions from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete without confirmation prompt',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be deleted'))

        # Find generic questions (those that contain "Sample question" in their text)
        generic_questions = Question.objects.filter(text__icontains='Sample question')

        self.stdout.write(f'Found {generic_questions.count()} generic questions to remove')

        if dry_run:
            # Show some examples of what would be deleted
            for question in generic_questions[:5]:
                self.stdout.write(f'  - Would delete: "{question.text[:50]}..."')
            if generic_questions.count() > 5:
                self.stdout.write(f'  - ... and {generic_questions.count() - 5} more')
            return

        # Confirm deletion
        if generic_questions.count() > 0 and not force:
            confirm = input(f'Are you sure you want to delete {generic_questions.count()} generic questions? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Operation cancelled'))
                return

        # Delete the generic questions
        with transaction.atomic():
            # First, delete the question choices (they should cascade, but let's be explicit)
            choice_count = 0
            for question in generic_questions:
                choice_count += question.choices.count()
                question.choices.all().delete()

            # Then delete the questions
            deleted_count = generic_questions.count()
            generic_questions.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_count} generic questions and {choice_count} associated choices'
                )
            )

        # Show remaining question count
        remaining_questions = Question.objects.count()
        self.stdout.write(f'Remaining questions in database: {remaining_questions}')

        # Show breakdown by subject
        self.stdout.write('\nRemaining questions by subject:')
        from django.db.models import Count
        subjects = Question.objects.values('subject__name').annotate(count=Count('id')).order_by('subject__name')
        for subject in subjects:
            self.stdout.write(f'  - {subject["subject__name"]}: {subject["count"]} questions')
