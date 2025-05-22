#!/usr/bin/env python
"""
Script to check what questions remain in the database after cleanup.
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from quiz.models import Question
from curriculum.models import Subject


def check_remaining_questions():
    """Check what questions remain in the database."""
    print("Checking remaining questions in the database...")
    
    total_questions = Question.objects.count()
    print(f"Total questions: {total_questions}")
    
    if total_questions == 0:
        print("No questions found in the database.")
        return
    
    print("\nSample of remaining questions:")
    for i, question in enumerate(Question.objects.all()[:10], 1):
        print(f"{i}. {question.text[:80]}...")
        print(f"   Subject: {question.subject.name} ({question.class_level.name})")
        print(f"   Topic: {question.topic.name if question.topic else 'No topic'}")
        print()
    
    if total_questions > 10:
        print(f"... and {total_questions - 10} more questions")
    
    print("\nQuestions by subject:")
    subjects_with_questions = Subject.objects.filter(questions__isnull=False).distinct()
    for subject in subjects_with_questions:
        question_count = subject.questions.count()
        print(f"- {subject.name} ({subject.class_level.name}): {question_count} questions")


if __name__ == "__main__":
    check_remaining_questions()
