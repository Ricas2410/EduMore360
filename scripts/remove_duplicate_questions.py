#!/usr/bin/env python
"""
Script to remove duplicate questions from the database.
Keeps the most recent version of each duplicate question.
"""

import os
import sys
import django
from collections import defaultdict

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from quiz.models import Question, QuestionChoice
from django.db.models import Count


def find_duplicate_questions():
    """Find questions with identical text within the same subject."""
    print("🔍 Finding duplicate questions...")
    
    # Group questions by subject and text
    duplicates = defaultdict(list)
    
    # Get all questions
    questions = Question.objects.all().order_by('subject', 'text', '-created_at')
    
    for question in questions:
        key = (question.subject.id, question.text.strip().lower())
        duplicates[key].append(question)
    
    # Filter to only groups with duplicates
    duplicate_groups = {k: v for k, v in duplicates.items() if len(v) > 1}
    
    print(f"Found {len(duplicate_groups)} groups of duplicate questions")
    
    return duplicate_groups


def remove_duplicates(duplicate_groups, dry_run=True):
    """Remove duplicate questions, keeping the most recent one."""
    total_removed = 0
    
    for (subject_id, text), questions in duplicate_groups.items():
        if len(questions) <= 1:
            continue
        
        # Sort by creation date (most recent first)
        questions.sort(key=lambda q: q.created_at, reverse=True)
        
        # Keep the first (most recent) question
        keep_question = questions[0]
        remove_questions = questions[1:]
        
        print(f"\n📝 Subject ID {subject_id}: '{text[:50]}...'")
        print(f"   Keeping: Question ID {keep_question.id} (created: {keep_question.created_at})")
        
        for question in remove_questions:
            print(f"   {'[DRY RUN] ' if dry_run else ''}Removing: Question ID {question.id} (created: {question.created_at})")
            
            if not dry_run:
                # Delete the question (choices will be deleted automatically due to CASCADE)
                question.delete()
                total_removed += 1
    
    return total_removed


def find_questions_with_identical_choices():
    """Find questions that have identical choices (potential duplicates)."""
    print("\n🔍 Finding questions with identical choice patterns...")
    
    # Group questions by their choice texts
    choice_patterns = defaultdict(list)
    
    questions = Question.objects.prefetch_related('choices').all()
    
    for question in questions:
        choices = question.choices.all().order_by('text')
        choice_texts = tuple(choice.text.strip().lower() for choice in choices)
        
        if len(choice_texts) >= 2:  # Only consider questions with at least 2 choices
            key = (question.subject.id, choice_texts)
            choice_patterns[key].append(question)
    
    # Filter to only groups with potential duplicates
    potential_duplicates = {k: v for k, v in choice_patterns.items() if len(v) > 1}
    
    print(f"Found {len(potential_duplicates)} groups with identical choice patterns")
    
    return potential_duplicates


def analyze_database_health():
    """Analyze the overall health of the question database."""
    print("\n📊 Database Health Analysis:")
    
    total_questions = Question.objects.count()
    active_questions = Question.objects.filter(is_active=True).count()
    inactive_questions = total_questions - active_questions
    
    print(f"   Total Questions: {total_questions}")
    print(f"   Active Questions: {active_questions}")
    print(f"   Inactive Questions: {inactive_questions}")
    
    # Questions by subject
    from django.db.models import Count
    subject_counts = (
        Question.objects
        .values('subject__name', 'subject__class_level__name')
        .annotate(count=Count('id'))
        .order_by('subject__class_level__name', 'subject__name')
    )
    
    print(f"\n📚 Questions by Subject:")
    for item in subject_counts:
        subject_name = item['subject__name']
        class_name = item['subject__class_level__name']
        count = item['count']
        print(f"   {class_name} - {subject_name}: {count} questions")
    
    # Questions without choices
    questions_without_choices = Question.objects.filter(choices__isnull=True).count()
    if questions_without_choices > 0:
        print(f"\n⚠️  Warning: {questions_without_choices} questions have no choices!")
    
    # Questions with only one choice
    questions_with_one_choice = (
        Question.objects
        .annotate(choice_count=Count('choices'))
        .filter(choice_count=1)
        .count()
    )
    if questions_with_one_choice > 0:
        print(f"⚠️  Warning: {questions_with_one_choice} questions have only one choice!")
    
    # Questions without correct answers
    questions_without_correct = (
        Question.objects
        .filter(choices__is_correct=False)
        .exclude(choices__is_correct=True)
        .distinct()
        .count()
    )
    if questions_without_correct > 0:
        print(f"⚠️  Warning: {questions_without_correct} questions have no correct answer!")


def main():
    """Main function to run the deduplication process."""
    print("🧹 Question Deduplication Tool")
    print("=" * 50)
    
    # Analyze database health first
    analyze_database_health()
    
    # Find exact text duplicates
    duplicate_groups = find_duplicate_questions()
    
    if not duplicate_groups:
        print("✅ No exact duplicate questions found!")
    else:
        print(f"\n🔍 Found {len(duplicate_groups)} groups of duplicate questions")
        
        # Show preview of what would be removed
        print("\n📋 Preview of duplicates to be removed:")
        total_to_remove = remove_duplicates(duplicate_groups, dry_run=True)
        
        if total_to_remove > 0:
            print(f"\n⚠️  This will remove {total_to_remove} duplicate questions.")
            
            # Ask for confirmation
            response = input("\nDo you want to proceed with removing duplicates? (yes/no): ").lower().strip()
            
            if response in ['yes', 'y']:
                print("\n🗑️  Removing duplicates...")
                actual_removed = remove_duplicates(duplicate_groups, dry_run=False)
                print(f"✅ Successfully removed {actual_removed} duplicate questions!")
            else:
                print("❌ Operation cancelled.")
    
    # Find questions with identical choices (potential duplicates)
    choice_duplicates = find_questions_with_identical_choices()
    
    if choice_duplicates:
        print(f"\n🔍 Found {len(choice_duplicates)} groups with identical choice patterns")
        print("   (These might be duplicates with slightly different question text)")
        
        # Show a few examples
        count = 0
        for (subject_id, choices), questions in choice_duplicates.items():
            if count >= 3:  # Show only first 3 examples
                break
            
            print(f"\n   Example {count + 1}:")
            for q in questions[:2]:  # Show first 2 questions in group
                print(f"     - ID {q.id}: '{q.text[:60]}...'")
            count += 1
        
        if len(choice_duplicates) > 3:
            print(f"     ... and {len(choice_duplicates) - 3} more groups")
    
    print("\n✅ Deduplication analysis complete!")


if __name__ == "__main__":
    main()
