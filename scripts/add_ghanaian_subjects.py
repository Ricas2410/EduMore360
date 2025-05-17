"""
Script to add History, Twi, RME, RMS, and Creative Arts subjects to all Ghanaian curriculum class levels.
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from django.utils.text import slugify
from curriculum.models import Curriculum, ClassLevel, Subject


def add_subjects_to_ghana_curriculum():
    """Add new subjects to all Ghanaian curriculum class levels."""
    try:
        # Get the Ghana curriculum
        ghana_curriculum = Curriculum.objects.get(code='GH')
        print(f"Found Ghana Curriculum: {ghana_curriculum.name}")

        # Get all class levels for Ghana curriculum
        class_levels = ClassLevel.objects.filter(curriculum=ghana_curriculum, is_active=True)
        print(f"Found {class_levels.count()} class levels for Ghana Curriculum")

        # Define the new subjects to add
        new_subjects = [
            {
                'name': 'History',
                'description': 'Study of past events, particularly in human affairs.'
            },
            {
                'name': 'Twi',
                'description': 'Study of the Twi language, one of the major languages spoken in Ghana.'
            },
            {
                'name': 'RME',
                'description': 'Religious and Moral Education - Study of religious beliefs, practices, and moral values.'
            },
            {
                'name': 'RMS',
                'description': 'Religious and Moral Studies - Advanced study of religious beliefs, practices, and moral values.'
            },
            {
                'name': 'Creative Arts',
                'description': 'Study of visual arts, performing arts, and other creative disciplines.'
            }
        ]

        # Add each subject to each class level
        subjects_added = 0
        subjects_skipped = 0

        for class_level in class_levels:
            print(f"\nProcessing class level: {class_level.name}")
            
            for subject_data in new_subjects:
                # Check if subject already exists for this class level
                subject_exists = Subject.objects.filter(
                    name=subject_data['name'],
                    curriculum=ghana_curriculum,
                    class_level=class_level
                ).exists()
                
                if subject_exists:
                    print(f"  - Subject '{subject_data['name']}' already exists for {class_level.name}, skipping...")
                    subjects_skipped += 1
                    continue
                
                # Create the subject
                subject = Subject.objects.create(
                    name=subject_data['name'],
                    slug=slugify(f"{subject_data['name']}-{class_level.name}"),
                    curriculum=ghana_curriculum,
                    class_level=class_level,
                    description=subject_data['description'],
                    is_active=True
                )
                
                print(f"  + Added '{subject.name}' to {class_level.name}")
                subjects_added += 1
        
        print(f"\nSummary: Added {subjects_added} new subjects, skipped {subjects_skipped} existing subjects")
        return True
    
    except Curriculum.DoesNotExist:
        print("Error: Ghana Curriculum not found!")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("Starting to add subjects to Ghana Curriculum...")
    success = add_subjects_to_ghana_curriculum()
    
    if success:
        print("Successfully added subjects to Ghana Curriculum!")
    else:
        print("Failed to add subjects to Ghana Curriculum.")
