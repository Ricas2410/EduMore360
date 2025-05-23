#!/usr/bin/env python
"""
Script to optimize database queries and reduce memory usage.
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from quiz.models import Quiz, Question
from django.db import connection


def optimize_quiz_question_counts():
    """Update quiz question counts to actual database counts."""
    print("Optimizing quiz question counts...")
    
    quizzes = Quiz.objects.all()
    
    for quiz in quizzes:
        # Count actual questions for this quiz's subject
        actual_count = Question.objects.filter(
            curriculum=quiz.curriculum,
            class_level=quiz.class_level,
            subject=quiz.subject,
            is_active=True
        ).count()
        
        # Update quiz question count to a reasonable number (max 30 for performance)
        optimal_count = min(actual_count, 30)
        
        if quiz.question_count != optimal_count:
            quiz.question_count = optimal_count
            quiz.save()
            print(f"Updated {quiz.title}: {quiz.question_count} questions")
    
    print("Quiz optimization completed!")


def show_database_stats():
    """Show current database statistics."""
    print("\n📊 Database Statistics:")
    
    # Count questions by subject
    from django.db.models import Count
    from curriculum.models import Subject
    
    subjects = Subject.objects.annotate(
        question_count=Count('questions')
    ).filter(question_count__gt=0)
    
    total_questions = 0
    for subject in subjects:
        print(f"  {subject.name} ({subject.class_level.name}): {subject.question_count} questions")
        total_questions += subject.question_count
    
    print(f"\n  Total Questions: {total_questions}")
    
    # Count quizzes
    quiz_count = Quiz.objects.count()
    print(f"  Total Quizzes: {quiz_count}")
    
    # Show database size info
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
        db_size = cursor.fetchone()[0]
        print(f"  Database Size: {db_size}")


def cleanup_inactive_questions():
    """Remove inactive questions to reduce database size."""
    print("\n🧹 Cleaning up inactive questions...")
    
    inactive_questions = Question.objects.filter(is_active=False)
    count = inactive_questions.count()
    
    if count > 0:
        inactive_questions.delete()
        print(f"Removed {count} inactive questions")
    else:
        print("No inactive questions found")


if __name__ == "__main__":
    print("🚀 Optimizing database for better performance...")
    
    show_database_stats()
    optimize_quiz_question_counts()
    cleanup_inactive_questions()
    
    print("\n✅ Database optimization completed!")
    print("💡 This should reduce memory usage on Render.")
