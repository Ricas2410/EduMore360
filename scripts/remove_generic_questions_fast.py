#!/usr/bin/env python
"""
Fast script to remove generic sample questions from the database using raw SQL.
"""

import os
import sys
import django
from django.db import connection

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

# No imports needed - using raw SQL


def remove_generic_questions():
    """Remove generic questions using efficient SQL queries."""
    print("Starting to remove generic questions...")

    # First, let's see what we have
    with connection.cursor() as cursor:
        # Count total questions
        cursor.execute("SELECT COUNT(*) FROM quiz_question")
        total_questions = cursor.fetchone()[0]
        print(f"Total questions in database: {total_questions}")

        # Count generic questions
        cursor.execute("SELECT COUNT(*) FROM quiz_question WHERE text LIKE '%Sample question%'")
        generic_questions = cursor.fetchone()[0]
        print(f"Generic questions to remove: {generic_questions}")

        if generic_questions == 0:
            print("No generic questions found. Nothing to do.")
            return

        # Get the IDs of generic questions for efficient deletion
        cursor.execute("SELECT id FROM quiz_question WHERE text LIKE '%Sample question%'")
        question_ids = [row[0] for row in cursor.fetchall()]

        print(f"Found {len(question_ids)} generic question IDs")

        # Delete in batches to avoid memory issues
        batch_size = 50
        total_deleted_attempts = 0
        total_deleted_choices = 0
        total_deleted_questions = 0

        for i in range(0, len(question_ids), batch_size):
            batch_ids = question_ids[i:i + batch_size]
            id_list = ','.join(map(str, batch_ids))

            # First, delete question attempts that reference these questions
            cursor.execute(f"DELETE FROM quiz_questionattempt WHERE question_id IN ({id_list})")
            deleted_attempts = cursor.rowcount
            total_deleted_attempts += deleted_attempts

            # Then delete question choices
            cursor.execute(f"DELETE FROM quiz_questionchoice WHERE question_id IN ({id_list})")
            deleted_choices = cursor.rowcount
            total_deleted_choices += deleted_choices

            # Finally delete the questions
            cursor.execute(f"DELETE FROM quiz_question WHERE id IN ({id_list})")
            deleted_questions = cursor.rowcount
            total_deleted_questions += deleted_questions

            print(f"Batch {i//batch_size + 1}: Deleted {deleted_questions} questions, {deleted_choices} choices, and {deleted_attempts} attempts")

        print(f"\nTotal deleted: {total_deleted_questions} questions, {total_deleted_choices} choices, and {total_deleted_attempts} attempts")

        # Count remaining questions
        cursor.execute("SELECT COUNT(*) FROM quiz_question")
        remaining_questions = cursor.fetchone()[0]
        print(f"Remaining questions in database: {remaining_questions}")

        # Show breakdown by subject
        print("\nRemaining questions by subject:")
        cursor.execute("""
            SELECT s.name, COUNT(q.id) as question_count
            FROM curriculum_subject s
            LEFT JOIN quiz_question q ON s.id = q.subject_id
            GROUP BY s.name, s.id
            HAVING COUNT(q.id) > 0
            ORDER BY s.name
        """)

        for row in cursor.fetchall():
            subject_name, count = row
            print(f"  - {subject_name}: {count} questions")


if __name__ == "__main__":
    try:
        remove_generic_questions()
        print("\nGeneric questions removed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
