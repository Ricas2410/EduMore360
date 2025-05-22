#!/usr/bin/env python
"""
Script to copy all Primary 6 questions to Primary 5 for core subjects.
This ensures both classes have the same comprehensive question sets.
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from quiz.models import Question, QuestionChoice, Quiz


def copy_questions_to_primary5():
    """Copy all Primary 6 questions to Primary 5 for core subjects."""
    try:
        # Get the Ghana curriculum and class levels
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary5 = ClassLevel.objects.get(name='Primary 5', curriculum=ghana_curriculum)
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        
        print(f"Copying questions from {primary6.name} to {primary5.name}...")
        
        # Core subjects to copy
        core_subjects = ['English', 'Mathematics', 'Science', 'ICT', 'Social Studies']
        
        total_questions_copied = 0
        
        for subject_name in core_subjects:
            try:
                # Get subjects for both classes
                subject_p6 = Subject.objects.get(name=subject_name, class_level=primary6)
                subject_p5 = Subject.objects.get(name=subject_name, class_level=primary5)
                
                print(f"\nProcessing {subject_name}...")
                print(f"  Source: {subject_p6.name} - {subject_p6.class_level.name}")
                print(f"  Target: {subject_p5.name} - {subject_p5.class_level.name}")
                
                # Get all topics from Primary 6 subject
                topics_p6 = Topic.objects.filter(subject=subject_p6)
                subject_questions_copied = 0
                
                for topic_p6 in topics_p6:
                    # Create or get corresponding topic in Primary 5
                    topic_p5, created = Topic.objects.get_or_create(
                        name=topic_p6.name,
                        subject=subject_p5,
                        defaults={
                            'description': topic_p6.description
                        }
                    )
                    
                    if created:
                        print(f"    Created topic: {topic_p5.name}")
                    else:
                        print(f"    Found existing topic: {topic_p5.name}")
                    
                    # Remove existing questions in Primary 5 topic to avoid duplicates
                    existing_questions = Question.objects.filter(topic=topic_p5)
                    if existing_questions.exists():
                        print(f"      Removing {existing_questions.count()} existing questions...")
                        existing_questions.delete()
                    
                    # Get all questions from Primary 6 topic
                    questions_p6 = Question.objects.filter(topic=topic_p6)
                    topic_questions_copied = 0
                    
                    for question_p6 in questions_p6:
                        # Create new question for Primary 5
                        question_p5 = Question.objects.create(
                            text=question_p6.text,
                            question_type=question_p6.question_type,
                            difficulty=question_p6.difficulty,
                            explanation=question_p6.explanation,
                            curriculum=ghana_curriculum,
                            class_level=primary5,
                            subject=subject_p5,
                            topic=topic_p5,
                            is_active=question_p6.is_active
                        )
                        
                        # Copy all choices
                        choices_p6 = QuestionChoice.objects.filter(question=question_p6)
                        for choice_p6 in choices_p6:
                            QuestionChoice.objects.create(
                                question=question_p5,
                                text=choice_p6.text,
                                is_correct=choice_p6.is_correct
                            )
                        
                        topic_questions_copied += 1
                    
                    print(f"      Copied {topic_questions_copied} questions to {topic_p5.name}")
                    subject_questions_copied += topic_questions_copied
                
                print(f"  Total questions copied for {subject_name}: {subject_questions_copied}")
                total_questions_copied += subject_questions_copied
                
                # Create or update quiz for Primary 5
                if subject_questions_copied > 0:
                    quiz, created = Quiz.objects.get_or_create(
                        title=f"{subject_name} Quiz - Primary 5",
                        curriculum=ghana_curriculum,
                        class_level=primary5,
                        subject=subject_p5,
                        defaults={
                            'description': f'Test your knowledge of {subject_name} concepts for Primary 5 level',
                            'quiz_type': 'general',
                            'question_count': subject_questions_copied,
                            'per_question_time': 45 if subject_name != 'Mathematics' else 60,  # Math gets more time
                            'randomize_questions': True,
                            'randomize_choices': True,
                            'show_immediate_feedback': True,
                            'passing_score': 60,  # 60% passing score
                            'is_active': True,
                            'is_featured': True
                        }
                    )
                    
                    if created:
                        print(f"  Created quiz: {quiz.title}")
                    else:
                        # Update question count
                        quiz.question_count = subject_questions_copied
                        quiz.save()
                        print(f"  Updated quiz: {quiz.title}")
                
            except Subject.DoesNotExist:
                print(f"  Subject '{subject_name}' not found in one of the classes, skipping...")
            except Exception as e:
                print(f"  Error processing {subject_name}: {str(e)}")
        
        print(f"\nTotal questions copied to Primary 5: {total_questions_copied}")
        
        # Summary of questions by class
        print(f"\nFinal question count summary:")
        for class_level in [primary5, primary6]:
            total_class_questions = Question.objects.filter(class_level=class_level).count()
            print(f"{class_level.name}: {total_class_questions} questions")
            
            # Breakdown by subject
            subjects = Subject.objects.filter(class_level=class_level)
            for subject in subjects:
                subject_questions = Question.objects.filter(subject=subject).count()
                if subject_questions > 0:
                    print(f"  - {subject.name}: {subject_questions} questions")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def ensure_primary5_subjects():
    """Ensure Primary 5 has all the core subjects with topics."""
    try:
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary5 = ClassLevel.objects.get(name='Primary 5', curriculum=ghana_curriculum)
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        
        print("Ensuring Primary 5 has all core subjects...")
        
        # Core subjects to ensure exist
        core_subjects = ['English', 'Mathematics', 'Science', 'ICT', 'Social Studies']
        
        for subject_name in core_subjects:
            try:
                # Get Primary 6 subject as template
                subject_p6 = Subject.objects.get(name=subject_name, class_level=primary6)
                
                # Create or get Primary 5 subject
                subject_p5, created = Subject.objects.get_or_create(
                    name=subject_name,
                    class_level=primary5,
                    defaults={
                        'description': subject_p6.description.replace('Primary 6', 'Primary 5') if subject_p6.description else f'{subject_name} for Primary 5 students',
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"  Created subject: {subject_p5.name} for Primary 5")
                else:
                    print(f"  Found existing subject: {subject_p5.name} for Primary 5")
                    
            except Subject.DoesNotExist:
                print(f"  Warning: {subject_name} not found in Primary 6")
        
        return True
        
    except Exception as e:
        print(f"Error ensuring subjects: {str(e)}")
        return False


if __name__ == "__main__":
    print("Setting up Primary 5 with comprehensive questions...")
    
    # First ensure Primary 5 has all subjects
    if ensure_primary5_subjects():
        print("\nSubjects setup completed.")
        
        # Then copy questions
        success = copy_questions_to_primary5()
        
        if success:
            print("\nQuestions successfully copied to Primary 5!")
        else:
            print("\nFailed to copy questions to Primary 5.")
    else:
        print("\nFailed to setup subjects for Primary 5.")
