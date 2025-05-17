"""
Script to analyze and fix questions in a CSV file.

This script helps identify duplicate questions in your CSV file and provides options to:
1. Show all questions with their IDs from the database
2. Check for duplicates in your CSV file
3. Fix duplicates by adding a unique suffix

Usage:
    python analyze_questions.py [command] [arguments]

Commands:
    show_db_questions - Show all questions in the database for a specific curriculum/class/subject/topic
    check_csv - Check a CSV file for potential duplicates
    fix_csv - Fix duplicates in a CSV file by adding a unique suffix
"""

import os
import sys
import csv
import django
from datetime import datetime

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from quiz.models import Question
from curriculum.models import Curriculum, ClassLevel, Subject, Topic

def show_db_questions(curriculum_code=None, class_level_name=None, subject_name=None, topic_name=None):
    """
    Show all questions in the database for a specific curriculum/class/subject/topic.
    """
    questions = Question.objects.all()
    
    if curriculum_code:
        try:
            curriculum = Curriculum.objects.get(code=curriculum_code)
            questions = questions.filter(curriculum=curriculum)
            print(f"Filtering by curriculum: {curriculum.name} ({curriculum.code})")
        except Curriculum.DoesNotExist:
            print(f"Error: Curriculum with code '{curriculum_code}' does not exist.")
            return
    
    if class_level_name and curriculum_code:
        try:
            class_level = ClassLevel.objects.get(curriculum__code=curriculum_code, name=class_level_name)
            questions = questions.filter(class_level=class_level)
            print(f"Filtering by class level: {class_level.name}")
        except ClassLevel.DoesNotExist:
            print(f"Error: Class level '{class_level_name}' does not exist for curriculum '{curriculum_code}'.")
            return
    
    if subject_name and curriculum_code and class_level_name:
        try:
            subject = Subject.objects.get(
                curriculum__code=curriculum_code, 
                class_level__name=class_level_name,
                name=subject_name
            )
            questions = questions.filter(subject=subject)
            print(f"Filtering by subject: {subject.name}")
        except Subject.DoesNotExist:
            print(f"Error: Subject '{subject_name}' does not exist for curriculum '{curriculum_code}' and class level '{class_level_name}'.")
            return
    
    if topic_name and curriculum_code and class_level_name and subject_name:
        try:
            subject = Subject.objects.get(
                curriculum__code=curriculum_code, 
                class_level__name=class_level_name,
                name=subject_name
            )
            topic = Topic.objects.get(subject=subject, name=topic_name)
            questions = questions.filter(topic=topic)
            print(f"Filtering by topic: {topic.name}")
        except Topic.DoesNotExist:
            print(f"Error: Topic '{topic_name}' does not exist for subject '{subject_name}'.")
            return
    
    print(f"\nFound {questions.count()} questions:")
    for q in questions:
        print(f"ID: {q.id} - {q.text[:50]}{'...' if len(q.text) > 50 else ''}")

def check_csv_duplicates(csv_file):
    """
    Check a CSV file for potential duplicates.
    """
    try:
        # Try different encodings
        encodings = ['utf-8-sig', 'cp1252', 'latin-1', 'iso-8859-1']
        data = None
        
        for encoding in encodings:
            try:
                with open(csv_file, 'r', encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                break
            except UnicodeDecodeError:
                continue
        
        if data is None:
            print(f"Error: Could not read the CSV file with any of the supported encodings.")
            return
        
        # Check for required columns
        required_columns = ['curriculum_code', 'class_level_name', 'subject_name', 'topic_name', 'question_text']
        missing_columns = [col for col in required_columns if col not in data[0]]
        if missing_columns:
            print(f"Error: CSV file is missing required columns: {', '.join(missing_columns)}")
            return
        
        # Group questions by curriculum, class level, subject, topic, and question text
        question_groups = {}
        for i, row in enumerate(data, start=2):  # Start from 2 to account for header row
            key = (
                row.get('curriculum_code', '').strip(),
                row.get('class_level_name', '').strip(),
                row.get('subject_name', '').strip(),
                row.get('topic_name', '').strip(),
                row.get('question_text', '').strip()
            )
            
            if key in question_groups:
                question_groups[key].append(i)
            else:
                question_groups[key] = [i]
        
        # Check for duplicates in the CSV file
        duplicates_found = False
        for key, rows in question_groups.items():
            if len(rows) > 1:
                duplicates_found = True
                print(f"\nDuplicate question found in rows {', '.join(map(str, rows))}:")
                print(f"Curriculum: {key[0]}")
                print(f"Class Level: {key[1]}")
                print(f"Subject: {key[2]}")
                print(f"Topic: {key[3]}")
                print(f"Question Text: {key[4][:100]}{'...' if len(key[4]) > 100 else ''}")
        
        if not duplicates_found:
            print("No duplicates found within the CSV file.")
        
        # Check for potential duplicates with the database
        print("\nChecking for potential duplicates with the database...")
        for row in data:
            curriculum_code = row.get('curriculum_code', '').strip()
            class_level_name = row.get('class_level_name', '').strip()
            subject_name = row.get('subject_name', '').strip()
            topic_name = row.get('topic_name', '').strip()
            question_text = row.get('question_text', '').strip()
            question_type = row.get('question_type', '').strip()
            
            try:
                curriculum = Curriculum.objects.get(code=curriculum_code)
                class_level = ClassLevel.objects.get(curriculum=curriculum, name=class_level_name)
                subject = Subject.objects.get(curriculum=curriculum, class_level=class_level, name=subject_name)
                topic = Topic.objects.get(subject=subject, name=topic_name)
                
                existing_question = Question.objects.filter(
                    text=question_text,
                    question_type=question_type,
                    curriculum=curriculum,
                    class_level=class_level,
                    subject=subject,
                    topic=topic
                ).first()
                
                if existing_question:
                    print(f"\nPotential duplicate with database question (ID: {existing_question.id}):")
                    print(f"Question Text: {question_text[:100]}{'...' if len(question_text) > 100 else ''}")
            except (Curriculum.DoesNotExist, ClassLevel.DoesNotExist, Subject.DoesNotExist, Topic.DoesNotExist):
                # Skip if any of the related objects don't exist
                continue
    
    except Exception as e:
        print(f"Error: {str(e)}")

def fix_csv_duplicates(input_file, output_file):
    """
    Fix duplicates in a CSV file by adding a unique suffix.
    """
    # Generate a timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    try:
        # Try different encodings
        encodings = ['utf-8-sig', 'cp1252', 'latin-1', 'iso-8859-1']
        data = None
        
        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    fieldnames = reader.fieldnames
                break
            except UnicodeDecodeError:
                continue
        
        if data is None:
            print(f"Error: Could not read the CSV file with any of the supported encodings.")
            return False
        
        # Add a unique suffix to each question text
        for i, row in enumerate(data):
            # Add a unique suffix to the question text
            # Format: [original text] (v{timestamp}-{row_number})
            original_text = row.get('question_text', '')
            row['question_text'] = f"{original_text} (v{timestamp}-{i+1})"
        
        # Write the modified data to the output file
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Success! Modified questions saved to {output_file}")
        print(f"Added unique suffix '(v{timestamp}-X)' to each question text.")
        return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def print_usage():
    """Print usage instructions."""
    print("Usage: python analyze_questions.py [command] [arguments]")
    print("\nCommands:")
    print("  show_db_questions [curriculum_code] [class_level_name] [subject_name] [topic_name]")
    print("    - Show all questions in the database for a specific curriculum/class/subject/topic")
    print("  check_csv [csv_file]")
    print("    - Check a CSV file for potential duplicates")
    print("  fix_csv [input_csv] [output_csv]")
    print("    - Fix duplicates in a CSV file by adding a unique suffix")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
    else:
        command = sys.argv[1]
        
        if command == "show_db_questions":
            curriculum_code = sys.argv[2] if len(sys.argv) > 2 else None
            class_level_name = sys.argv[3] if len(sys.argv) > 3 else None
            subject_name = sys.argv[4] if len(sys.argv) > 4 else None
            topic_name = sys.argv[5] if len(sys.argv) > 5 else None
            show_db_questions(curriculum_code, class_level_name, subject_name, topic_name)
        
        elif command == "check_csv":
            if len(sys.argv) < 3:
                print("Error: Missing CSV file argument.")
                print("Usage: python analyze_questions.py check_csv [csv_file]")
            else:
                csv_file = sys.argv[2]
                if not os.path.exists(csv_file):
                    print(f"Error: CSV file '{csv_file}' does not exist.")
                else:
                    check_csv_duplicates(csv_file)
        
        elif command == "fix_csv":
            if len(sys.argv) < 4:
                print("Error: Missing input or output CSV file arguments.")
                print("Usage: python analyze_questions.py fix_csv [input_csv] [output_csv]")
            else:
                input_file = sys.argv[2]
                output_file = sys.argv[3]
                if not os.path.exists(input_file):
                    print(f"Error: Input file '{input_file}' does not exist.")
                else:
                    fix_csv_duplicates(input_file, output_file)
        
        else:
            print(f"Error: Unknown command '{command}'.")
            print_usage()
