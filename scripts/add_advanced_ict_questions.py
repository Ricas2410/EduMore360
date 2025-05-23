#!/usr/bin/env python
"""
Script to add advanced ICT questions for Primary 5 and Primary 6.
Covers Databases, SQL Commands, Excel, Data Manipulation, and modern ICT concepts.
Making this the best international educational system.
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


def get_advanced_ict_questions_data():
    """Return advanced ICT questions for international competitiveness."""
    return {
        'Database Fundamentals': [
            {
                'text': 'What is a database?',
                'choices': [
                    {'text': 'A collection of organized data stored electronically', 'is_correct': True},
                    {'text': 'A type of computer game', 'is_correct': False},
                    {'text': 'A word processing document', 'is_correct': False},
                    {'text': 'A computer virus', 'is_correct': False}
                ],
                'explanation': 'A database is a collection of organized data that is stored electronically in a computer system. It allows us to store, retrieve, and manage large amounts of information efficiently.'
            },
            {
                'text': 'What is a table in a database?',
                'choices': [
                    {'text': 'A piece of furniture', 'is_correct': False},
                    {'text': 'A structure that organizes data in rows and columns', 'is_correct': True},
                    {'text': 'A type of chart', 'is_correct': False},
                    {'text': 'A computer screen', 'is_correct': False}
                ],
                'explanation': 'In a database, a table is a structure that organizes data in rows and columns. Each row represents a record (like a student), and each column represents a field (like name, age, or grade).'
            },
            {
                'text': 'What is a record in a database?',
                'choices': [
                    {'text': 'A single row of data in a table', 'is_correct': True},
                    {'text': 'A music file', 'is_correct': False},
                    {'text': 'A column in a table', 'is_correct': False},
                    {'text': 'A database name', 'is_correct': False}
                ],
                'explanation': 'A record is a single row of data in a database table. For example, in a student database, one record would contain all the information about one student (name, age, class, etc.).'
            },
            {
                'text': 'What is a field in a database?',
                'choices': [
                    {'text': 'An open area of land', 'is_correct': False},
                    {'text': 'A single piece of information in a record', 'is_correct': True},
                    {'text': 'A complete table', 'is_correct': False},
                    {'text': 'A database file', 'is_correct': False}
                ],
                'explanation': 'A field is a single piece of information in a record, represented by a column in a table. Examples include "Name", "Age", "Email", or "Phone Number".'
            },
            {
                'text': 'What is a primary key in a database?',
                'choices': [
                    {'text': 'The most important table', 'is_correct': False},
                    {'text': 'A unique identifier for each record', 'is_correct': True},
                    {'text': 'The first column in a table', 'is_correct': False},
                    {'text': 'A password for the database', 'is_correct': False}
                ],
                'explanation': 'A primary key is a unique identifier for each record in a table. It ensures that no two records are exactly the same and helps us find specific records quickly.'
            },
            {
                'text': 'Why are databases important in modern life?',
                'choices': [
                    {'text': 'They are not important', 'is_correct': False},
                    {'text': 'They help organize and manage large amounts of information', 'is_correct': True},
                    {'text': 'They only store pictures', 'is_correct': False},
                    {'text': 'They replace computers', 'is_correct': False}
                ],
                'explanation': 'Databases are crucial in modern life because they help organizations store, organize, and manage vast amounts of information efficiently. They are used in schools, hospitals, banks, and many other places.'
            }
        ],

        'SQL Commands': [
            {
                'text': 'What does SQL stand for?',
                'choices': [
                    {'text': 'Structured Query Language', 'is_correct': True},
                    {'text': 'Simple Question Language', 'is_correct': False},
                    {'text': 'Standard Quality Language', 'is_correct': False},
                    {'text': 'System Query Logic', 'is_correct': False}
                ],
                'explanation': 'SQL stands for Structured Query Language. It is a programming language designed for managing and manipulating data in relational databases.'
            },
            {
                'text': 'Which SQL command is used to retrieve data from a database?',
                'choices': [
                    {'text': 'GET', 'is_correct': False},
                    {'text': 'SELECT', 'is_correct': True},
                    {'text': 'FIND', 'is_correct': False},
                    {'text': 'SHOW', 'is_correct': False}
                ],
                'explanation': 'The SELECT command is used to retrieve (get) data from a database. For example, "SELECT name FROM students" would get all the names from a students table.'
            },
            {
                'text': 'Which SQL command is used to add new data to a database?',
                'choices': [
                    {'text': 'ADD', 'is_correct': False},
                    {'text': 'INSERT', 'is_correct': True},
                    {'text': 'PUT', 'is_correct': False},
                    {'text': 'CREATE', 'is_correct': False}
                ],
                'explanation': 'The INSERT command is used to add new data (records) to a database table. For example, "INSERT INTO students (name, age) VALUES (\'John\', 12)" adds a new student.'
            },
            {
                'text': 'Which SQL command is used to modify existing data?',
                'choices': [
                    {'text': 'CHANGE', 'is_correct': False},
                    {'text': 'MODIFY', 'is_correct': False},
                    {'text': 'UPDATE', 'is_correct': True},
                    {'text': 'EDIT', 'is_correct': False}
                ],
                'explanation': 'The UPDATE command is used to modify (change) existing data in a database. For example, "UPDATE students SET age = 13 WHERE name = \'John\'" changes John\'s age to 13.'
            },
            {
                'text': 'Which SQL command is used to remove data from a database?',
                'choices': [
                    {'text': 'REMOVE', 'is_correct': False},
                    {'text': 'DELETE', 'is_correct': True},
                    {'text': 'ERASE', 'is_correct': False},
                    {'text': 'CLEAR', 'is_correct': False}
                ],
                'explanation': 'The DELETE command is used to remove data from a database. For example, "DELETE FROM students WHERE age < 10" would remove all students younger than 10.'
            },
            {
                'text': 'What does the WHERE clause do in SQL?',
                'choices': [
                    {'text': 'It specifies the location of the database', 'is_correct': False},
                    {'text': 'It filters data based on specific conditions', 'is_correct': True},
                    {'text': 'It creates a new table', 'is_correct': False},
                    {'text': 'It deletes the entire database', 'is_correct': False}
                ],
                'explanation': 'The WHERE clause filters data based on specific conditions. It helps you select only the records that meet certain criteria, like "WHERE age > 12" to find students older than 12.'
            }
        ],

        'Microsoft Excel': [
            {
                'text': 'What is Microsoft Excel?',
                'choices': [
                    {'text': 'A word processing program', 'is_correct': False},
                    {'text': 'A spreadsheet application for data analysis', 'is_correct': True},
                    {'text': 'A web browser', 'is_correct': False},
                    {'text': 'A photo editing software', 'is_correct': False}
                ],
                'explanation': 'Microsoft Excel is a powerful spreadsheet application used for organizing, analyzing, and visualizing data. It uses rows and columns to organize information and can perform calculations.'
            },
            {
                'text': 'What is a cell in Excel?',
                'choices': [
                    {'text': 'A prison room', 'is_correct': False},
                    {'text': 'The intersection of a row and column', 'is_correct': True},
                    {'text': 'A phone device', 'is_correct': False},
                    {'text': 'A type of formula', 'is_correct': False}
                ],
                'explanation': 'A cell in Excel is the intersection of a row and column where you can enter data, formulas, or functions. Each cell has a unique address like A1, B2, etc.'
            },
            {
                'text': 'What symbol do you use to start a formula in Excel?',
                'choices': [
                    {'text': '#', 'is_correct': False},
                    {'text': '=', 'is_correct': True},
                    {'text': '+', 'is_correct': False},
                    {'text': '*', 'is_correct': False}
                ],
                'explanation': 'In Excel, you start a formula with the equals sign (=). For example, =A1+B1 adds the values in cells A1 and B1.'
            },
            {
                'text': 'Which Excel function adds up a range of numbers?',
                'choices': [
                    {'text': 'ADD', 'is_correct': False},
                    {'text': 'SUM', 'is_correct': True},
                    {'text': 'TOTAL', 'is_correct': False},
                    {'text': 'PLUS', 'is_correct': False}
                ],
                'explanation': 'The SUM function adds up a range of numbers. For example, =SUM(A1:A10) adds all the numbers from cell A1 to A10.'
            },
            {
                'text': 'Which Excel function finds the average of a range of numbers?',
                'choices': [
                    {'text': 'MEAN', 'is_correct': False},
                    {'text': 'AVERAGE', 'is_correct': True},
                    {'text': 'AVG', 'is_correct': False},
                    {'text': 'MEDIAN', 'is_correct': False}
                ],
                'explanation': 'The AVERAGE function calculates the average (mean) of a range of numbers. For example, =AVERAGE(A1:A10) finds the average of numbers in cells A1 to A10.'
            },
            {
                'text': 'What is a chart in Excel?',
                'choices': [
                    {'text': 'A map', 'is_correct': False},
                    {'text': 'A visual representation of data', 'is_correct': True},
                    {'text': 'A list of rules', 'is_correct': False},
                    {'text': 'A type of cell', 'is_correct': False}
                ],
                'explanation': 'A chart in Excel is a visual representation of data that makes it easier to understand patterns and trends. Examples include bar charts, pie charts, and line graphs.'
            },
            {
                'text': 'Why is Excel important for students to learn?',
                'choices': [
                    {'text': 'It\'s only for accountants', 'is_correct': False},
                    {'text': 'It helps organize data and solve problems in many subjects', 'is_correct': True},
                    {'text': 'It\'s not important', 'is_correct': False},
                    {'text': 'It only works with numbers', 'is_correct': False}
                ],
                'explanation': 'Excel is important for students because it helps organize data, perform calculations, create charts, and solve problems in many subjects like math, science, and social studies.'
            }
        ],

        'Data Analysis and Manipulation': [
            {
                'text': 'What is data analysis?',
                'choices': [
                    {'text': 'Deleting data from computers', 'is_correct': False},
                    {'text': 'Examining data to find patterns and make decisions', 'is_correct': True},
                    {'text': 'Creating new data', 'is_correct': False},
                    {'text': 'Copying data to different computers', 'is_correct': False}
                ],
                'explanation': 'Data analysis is the process of examining data to discover patterns, trends, and insights that can help us make informed decisions and solve problems.'
            },
            {
                'text': 'What is data sorting?',
                'choices': [
                    {'text': 'Arranging data in a specific order', 'is_correct': True},
                    {'text': 'Deleting unwanted data', 'is_correct': False},
                    {'text': 'Creating backup copies', 'is_correct': False},
                    {'text': 'Changing data types', 'is_correct': False}
                ],
                'explanation': 'Data sorting is arranging data in a specific order, such as alphabetical order for names or numerical order for numbers. This makes it easier to find and analyze information.'
            },
            {
                'text': 'What is data filtering?',
                'choices': [
                    {'text': 'Cleaning dirty data', 'is_correct': False},
                    {'text': 'Showing only data that meets certain criteria', 'is_correct': True},
                    {'text': 'Converting data to different formats', 'is_correct': False},
                    {'text': 'Backing up data', 'is_correct': False}
                ],
                'explanation': 'Data filtering is showing only the data that meets certain criteria while hiding the rest. For example, filtering a student list to show only students in Grade 6.'
            },
            {
                'text': 'What is a pivot table?',
                'choices': [
                    {'text': 'A rotating table', 'is_correct': False},
                    {'text': 'A tool that summarizes and analyzes large amounts of data', 'is_correct': True},
                    {'text': 'A type of chart', 'is_correct': False},
                    {'text': 'A database table', 'is_correct': False}
                ],
                'explanation': 'A pivot table is a powerful tool that summarizes and analyzes large amounts of data. It can quickly group, count, and calculate totals to help you understand your data better.'
            },
            {
                'text': 'Why is data visualization important?',
                'choices': [
                    {'text': 'It makes data look pretty', 'is_correct': False},
                    {'text': 'It helps people understand data more easily', 'is_correct': True},
                    {'text': 'It takes up more space', 'is_correct': False},
                    {'text': 'It\'s not important', 'is_correct': False}
                ],
                'explanation': 'Data visualization (like charts and graphs) is important because it helps people understand complex data more easily. Visual representations make patterns and trends clearer than just looking at numbers.'
            },
            {
                'text': 'What is the difference between data and information?',
                'choices': [
                    {'text': 'There is no difference', 'is_correct': False},
                    {'text': 'Data are raw facts; information is processed data with meaning', 'is_correct': True},
                    {'text': 'Information is always bigger than data', 'is_correct': False},
                    {'text': 'Data is newer than information', 'is_correct': False}
                ],
                'explanation': 'Data are raw facts and figures without context. Information is data that has been processed, organized, and given meaning. For example, "25" is data, but "25 students in the class" is information.'
            }
        ],

        'Digital Literacy and Future Skills': [
            {
                'text': 'What is cloud computing?',
                'choices': [
                    {'text': 'Computing done in the sky', 'is_correct': False},
                    {'text': 'Storing and accessing data over the internet', 'is_correct': True},
                    {'text': 'A type of weather prediction', 'is_correct': False},
                    {'text': 'A computer game', 'is_correct': False}
                ],
                'explanation': 'Cloud computing means storing and accessing data and programs over the internet instead of on your computer\'s hard drive. Examples include Google Drive, iCloud, and OneDrive.'
            },
            {
                'text': 'What is artificial intelligence (AI)?',
                'choices': [
                    {'text': 'Fake intelligence', 'is_correct': False},
                    {'text': 'Computer systems that can perform tasks that typically require human intelligence', 'is_correct': True},
                    {'text': 'A type of robot', 'is_correct': False},
                    {'text': 'A computer virus', 'is_correct': False}
                ],
                'explanation': 'Artificial Intelligence (AI) refers to computer systems that can perform tasks that typically require human intelligence, such as recognizing speech, making decisions, or solving problems.'
            },
            {
                'text': 'What is coding/programming?',
                'choices': [
                    {'text': 'Writing secret messages', 'is_correct': False},
                    {'text': 'Writing instructions for computers to follow', 'is_correct': True},
                    {'text': 'Fixing broken computers', 'is_correct': False},
                    {'text': 'Installing software', 'is_correct': False}
                ],
                'explanation': 'Coding or programming is writing step-by-step instructions (called code) that tell computers what to do. It\'s like giving directions to a computer to solve problems or create applications.'
            },
            {
                'text': 'Why is digital literacy important for students today?',
                'choices': [
                    {'text': 'It\'s not important', 'is_correct': False},
                    {'text': 'It prepares students for future careers and helps them succeed in a digital world', 'is_correct': True},
                    {'text': 'It\'s only for computer science students', 'is_correct': False},
                    {'text': 'It\'s just for entertainment', 'is_correct': False}
                ],
                'explanation': 'Digital literacy is crucial because we live in a digital world. It prepares students for future careers, helps them solve problems efficiently, and enables them to be productive citizens in the 21st century.'
            },
            {
                'text': 'What is data privacy?',
                'choices': [
                    {'text': 'Keeping data secret from everyone', 'is_correct': False},
                    {'text': 'Protecting personal information from unauthorized access', 'is_correct': True},
                    {'text': 'Making data public', 'is_correct': False},
                    {'text': 'Deleting all data', 'is_correct': False}
                ],
                'explanation': 'Data privacy means protecting personal information from unauthorized access or use. It\'s important to keep personal data safe and only share it with trusted sources.'
            },
            {
                'text': 'What skills will be most important for future jobs?',
                'choices': [
                    {'text': 'Only traditional skills', 'is_correct': False},
                    {'text': 'Digital skills combined with critical thinking and creativity', 'is_correct': True},
                    {'text': 'Only computer programming', 'is_correct': False},
                    {'text': 'Only manual labor skills', 'is_correct': False}
                ],
                'explanation': 'Future jobs will require a combination of digital skills (like data analysis, programming, and digital communication) along with human skills like critical thinking, creativity, and problem-solving.'
            }
        ]
    }


def create_advanced_ict_questions():
    """Create advanced ICT questions for both Primary 5 and Primary 6."""
    try:
        # Get the Ghana curriculum and class levels
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary5 = ClassLevel.objects.get(name='Primary 5', curriculum=ghana_curriculum)
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)

        # Get ICT subjects for both classes
        ict_subject_p5 = Subject.objects.get(name='ICT', class_level=primary5)
        ict_subject_p6 = Subject.objects.get(name='ICT', class_level=primary6)

        print(f"Found ICT subjects:")
        print(f"- {ict_subject_p5.name} - {ict_subject_p5.class_level.name}")
        print(f"- {ict_subject_p6.name} - {ict_subject_p6.class_level.name}")

        questions_data = get_advanced_ict_questions_data()
        total_questions_created = 0

        # Create questions for both Primary 5 and Primary 6
        for class_level, ict_subject in [(primary5, ict_subject_p5), (primary6, ict_subject_p6)]:
            print(f"\nProcessing {class_level.name}...")

            class_questions_created = 0

            for topic_name, topic_questions in questions_data.items():
                # Create or get the topic
                topic, created = Topic.objects.get_or_create(
                    name=topic_name,
                    subject=ict_subject,
                    defaults={
                        'description': f'Advanced {topic_name} concepts for modern ICT education'
                    }
                )

                if created:
                    print(f"  Created new topic: {topic.name}")
                else:
                    print(f"  Found existing topic: {topic.name}")
                    # Remove existing questions to avoid duplicates
                    existing_questions = Question.objects.filter(topic=topic)
                    if existing_questions.exists():
                        print(f"    Removing {existing_questions.count()} existing questions...")
                        existing_questions.delete()

                topic_questions_created = 0

                for question_data in topic_questions:
                    # Create the question
                    question = Question.objects.create(
                        text=question_data['text'],
                        question_type='multiple_choice',
                        difficulty='medium',  # Advanced content
                        explanation=question_data['explanation'],
                        curriculum=ghana_curriculum,
                        class_level=class_level,
                        subject=ict_subject,
                        topic=topic,
                        is_active=True
                    )

                    # Create the choices
                    for choice_data in question_data['choices']:
                        QuestionChoice.objects.create(
                            question=question,
                            text=choice_data['text'],
                            is_correct=choice_data['is_correct']
                        )

                    topic_questions_created += 1

                print(f"    Added {topic_questions_created} questions to {topic.name}")
                class_questions_created += topic_questions_created

            print(f"  Total advanced ICT questions created for {class_level.name}: {class_questions_created}")
            total_questions_created += class_questions_created

            # Update the existing ICT quiz with new question count
            try:
                quiz = Quiz.objects.get(
                    title=f"ICT Quiz - {class_level.name}",
                    curriculum=ghana_curriculum,
                    class_level=class_level,
                    subject=ict_subject
                )

                # Count all ICT questions for this class
                total_ict_questions = Question.objects.filter(subject=ict_subject).count()
                quiz.question_count = total_ict_questions
                quiz.description = f'Comprehensive ICT knowledge test including databases, Excel, SQL, and modern digital skills for {class_level.name} level'
                quiz.per_question_time = 60  # More time for advanced questions
                quiz.save()

                print(f"  Updated quiz: {quiz.title} (Total questions: {total_ict_questions})")

            except Quiz.DoesNotExist:
                print(f"  Warning: ICT Quiz for {class_level.name} not found")

        print(f"\nTotal advanced ICT questions created: {total_questions_created}")

        # Create a special Advanced ICT Quiz
        for class_level, ict_subject in [(primary5, ict_subject_p5), (primary6, ict_subject_p6)]:
            advanced_questions_count = Question.objects.filter(
                subject=ict_subject,
                difficulty='medium'
            ).count()

            if advanced_questions_count > 0:
                advanced_quiz, created = Quiz.objects.get_or_create(
                    title=f"Advanced ICT & Digital Skills - {class_level.name}",
                    curriculum=ghana_curriculum,
                    class_level=class_level,
                    subject=ict_subject,
                    defaults={
                        'description': f'Advanced ICT quiz covering databases, SQL, Excel, data analysis, and future digital skills for {class_level.name}',
                        'quiz_type': 'advanced',
                        'question_count': advanced_questions_count,
                        'per_question_time': 75,  # More time for complex questions
                        'randomize_questions': True,
                        'randomize_choices': True,
                        'show_immediate_feedback': True,
                        'passing_score': 70,  # Higher passing score for advanced content
                        'is_active': True,
                        'is_featured': True
                    }
                )

                if created:
                    print(f"  Created advanced quiz: {advanced_quiz.title}")
                else:
                    advanced_quiz.question_count = advanced_questions_count
                    advanced_quiz.save()
                    print(f"  Updated advanced quiz: {advanced_quiz.title}")

        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("Adding advanced ICT questions for international competitiveness...")
    print("Topics: Databases, SQL Commands, Excel, Data Analysis, Digital Literacy")

    success = create_advanced_ict_questions()

    if success:
        print("\n🎉 Advanced ICT questions added successfully!")
        print("🌍 Your students now have world-class ICT education!")
    else:
        print("\n❌ Failed to add advanced ICT questions.")
