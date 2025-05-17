from django.core.management.base import BaseCommand
from curriculum.models import Curriculum, ClassLevel, Subject


class Command(BaseCommand):
    help = 'Add ICT subject to all Ghanaian curriculum class levels'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding ICT subject to all Ghanaian curriculum class levels...'))

        # Get Ghana curriculum
        try:
            gh_curriculum = Curriculum.objects.get(code='GH')
        except Curriculum.DoesNotExist:
            self.stdout.write(self.style.ERROR('Ghana curriculum not found!'))
            return

        # Get all class levels for Ghana curriculum
        class_levels = ClassLevel.objects.filter(curriculum=gh_curriculum)

        if not class_levels.exists():
            self.stdout.write(self.style.ERROR('No class levels found for Ghana curriculum!'))
            return

        # Add ICT subject to each class level
        for class_level in class_levels:
            # Check if ICT subject already exists for this class level
            if Subject.objects.filter(curriculum=gh_curriculum, class_level=class_level, name='ICT').exists():
                self.stdout.write(self.style.WARNING(f'ICT subject already exists for {class_level.name}'))
                continue

            # Create ICT subject with a unique slug
            class_level_slug = class_level.name.lower().replace(' ', '-')
            unique_slug = f'ict-{class_level_slug}'

            Subject.objects.create(
                name='ICT',
                slug=unique_slug,
                description='Information and Communication Technology',
                curriculum=gh_curriculum,
                class_level=class_level,
                is_active=True
            )

            self.stdout.write(self.style.SUCCESS(f'Added ICT subject to {class_level.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully added ICT subject to all Ghanaian curriculum class levels!'))
