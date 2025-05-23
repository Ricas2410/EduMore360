#!/usr/bin/env python
"""
Script to reorganize ICT topics by merging Database, SQL, Excel, and Data Analysis
into one comprehensive "Database and Data Management" topic.
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from quiz.models import Question, QuestionChoice


def reorganize_ict_topics():
    """Reorganize ICT topics to merge database-related topics."""
    try:
        # Get the Ghana curriculum and class levels
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary5 = ClassLevel.objects.get(name='Primary 5', curriculum=ghana_curriculum)
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        
        print("Reorganizing ICT topics...")
        
        # Topics to merge into "Database and Data Management"
        topics_to_merge = [
            'Database Fundamentals',
            'SQL Commands', 
            'Microsoft Excel',
            'Data Analysis and Manipulation'
        ]
        
        # Process both Primary 5 and Primary 6
        for class_level in [primary5, primary6]:
            print(f"\nProcessing {class_level.name}...")
            
            # Get ICT subject
            ict_subject = Subject.objects.get(name='ICT', class_level=class_level)
            
            # Create or get the new comprehensive topic
            new_topic, created = Topic.objects.get_or_create(
                name='Database and Data Management',
                subject=ict_subject,
                defaults={
                    'description': 'Comprehensive coverage of databases, SQL commands, Excel spreadsheets, and data analysis techniques for modern ICT education'
                }
            )
            
            if created:
                print(f"  Created new topic: {new_topic.name}")
            else:
                print(f"  Found existing topic: {new_topic.name}")
            
            # Find all questions from topics to merge
            questions_to_move = []
            topics_to_delete = []
            
            for topic_name in topics_to_merge:
                try:
                    old_topic = Topic.objects.get(name=topic_name, subject=ict_subject)
                    topic_questions = Question.objects.filter(topic=old_topic)
                    questions_to_move.extend(list(topic_questions))
                    topics_to_delete.append(old_topic)
                    print(f"    Found {topic_questions.count()} questions in {topic_name}")
                except Topic.DoesNotExist:
                    print(f"    Topic {topic_name} not found, skipping...")
            
            # Move all questions to the new topic
            questions_moved = 0
            for question in questions_to_move:
                question.topic = new_topic
                question.save()
                questions_moved += 1
            
            print(f"  Moved {questions_moved} questions to {new_topic.name}")
            
            # Delete the old topics (this will not delete questions since we moved them)
            for old_topic in topics_to_delete:
                old_topic.delete()
                print(f"    Deleted old topic: {old_topic.name}")
            
            # Count final questions in the new topic
            final_count = Question.objects.filter(topic=new_topic).count()
            print(f"  Final question count in {new_topic.name}: {final_count}")
        
        print("\nICT topic reorganization completed successfully!")
        
        # Show final ICT topic structure
        print("\nFinal ICT topic structure:")
        for class_level in [primary5, primary6]:
            ict_subject = Subject.objects.get(name='ICT', class_level=class_level)
            topics = Topic.objects.filter(subject=ict_subject).order_by('name')
            
            print(f"\n{class_level.name} ICT Topics:")
            for topic in topics:
                question_count = Question.objects.filter(topic=topic).count()
                print(f"  - {topic.name}: {question_count} questions")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def update_quiz_descriptions():
    """Update quiz descriptions to reflect the new topic structure."""
    try:
        print("\nUpdating quiz descriptions...")
        
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary5 = ClassLevel.objects.get(name='Primary 5', curriculum=ghana_curriculum)
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        
        for class_level in [primary5, primary6]:
            ict_subject = Subject.objects.get(name='ICT', class_level=class_level)
            
            # Update main ICT quiz
            from quiz.models import Quiz
            try:
                main_quiz = Quiz.objects.get(
                    title=f"ICT Quiz - {class_level.name}",
                    subject=ict_subject
                )
                main_quiz.description = f'Comprehensive ICT knowledge test covering computer basics, databases, Excel, data analysis, internet skills, and digital literacy for {class_level.name} level'
                main_quiz.save()
                print(f"  Updated main ICT quiz for {class_level.name}")
            except Quiz.DoesNotExist:
                print(f"  Main ICT quiz not found for {class_level.name}")
            
            # Update advanced ICT quiz
            try:
                advanced_quiz = Quiz.objects.get(
                    title=f"Advanced ICT & Digital Skills - {class_level.name}",
                    subject=ict_subject
                )
                advanced_quiz.description = f'Advanced ICT quiz focusing on database management, SQL commands, Excel data analysis, and future digital skills for {class_level.name}'
                advanced_quiz.save()
                print(f"  Updated advanced ICT quiz for {class_level.name}")
            except Quiz.DoesNotExist:
                print(f"  Advanced ICT quiz not found for {class_level.name}")
        
        return True
        
    except Exception as e:
        print(f"Error updating quiz descriptions: {str(e)}")
        return False


if __name__ == "__main__":
    print("🔄 Reorganizing ICT topics for better structure...")
    print("Merging: Database Fundamentals + SQL Commands + Microsoft Excel + Data Analysis")
    print("Into: Database and Data Management")
    
    success = reorganize_ict_topics()
    
    if success:
        print("\n✅ ICT topics reorganized successfully!")
        
        # Update quiz descriptions
        if update_quiz_descriptions():
            print("✅ Quiz descriptions updated!")
        
        print("\n🎯 Your ICT curriculum now has a more logical structure!")
        print("📊 Students will learn databases, SQL, Excel, and data analysis together!")
    else:
        print("\n❌ Failed to reorganize ICT topics.")
