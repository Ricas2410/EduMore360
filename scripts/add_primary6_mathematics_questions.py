#!/usr/bin/env python
"""
Script to add comprehensive Mathematics questions for Primary 6 Ghana Curriculum.
Based on the Ghana Education Service (GES) Mathematics curriculum for Primary 6.
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


def get_mathematics_questions_data():
    """Return comprehensive Mathematics questions for Primary 6 based on GES curriculum."""
    return {
        'Numbers and Operations': [
            {
                'text': 'What is 456 + 789?',
                'choices': [
                    {'text': '1245', 'is_correct': True},
                    {'text': '1235', 'is_correct': False},
                    {'text': '1345', 'is_correct': False},
                    {'text': '1145', 'is_correct': False}
                ],
                'explanation': 'To add 456 + 789: 6+9=15 (write 5, carry 1), 5+8+1=14 (write 4, carry 1), 4+7+1=12. So the answer is 1245.'
            },
            {
                'text': 'What is 1000 - 347?',
                'choices': [
                    {'text': '653', 'is_correct': True},
                    {'text': '663', 'is_correct': False},
                    {'text': '643', 'is_correct': False},
                    {'text': '753', 'is_correct': False}
                ],
                'explanation': 'To subtract 1000 - 347: Start from the right: 0-7 (borrow), 10-7=3. 0-4 (borrow), 9-4=5. 9-3=6. Answer is 653.'
            },
            {
                'text': 'What is 25 × 4?',
                'choices': [
                    {'text': '90', 'is_correct': False},
                    {'text': '100', 'is_correct': True},
                    {'text': '110', 'is_correct': False},
                    {'text': '80', 'is_correct': False}
                ],
                'explanation': '25 × 4 = 100. You can think of it as 25 × 4 = (20 × 4) + (5 × 4) = 80 + 20 = 100.'
            },
            {
                'text': 'What is 144 ÷ 12?',
                'choices': [
                    {'text': '11', 'is_correct': False},
                    {'text': '12', 'is_correct': True},
                    {'text': '13', 'is_correct': False},
                    {'text': '14', 'is_correct': False}
                ],
                'explanation': '144 ÷ 12 = 12. You can check this by multiplying: 12 × 12 = 144.'
            },
            {
                'text': 'Which number is the largest?',
                'choices': [
                    {'text': '9,876', 'is_correct': False},
                    {'text': '10,234', 'is_correct': True},
                    {'text': '9,999', 'is_correct': False},
                    {'text': '9,987', 'is_correct': False}
                ],
                'explanation': '10,234 is the largest because it has 5 digits while the others have 4 digits. Any 5-digit number is larger than any 4-digit number.'
            },
            {
                'text': 'What is the place value of 7 in 47,356?',
                'choices': [
                    {'text': 'Ones', 'is_correct': False},
                    {'text': 'Tens', 'is_correct': False},
                    {'text': 'Hundreds', 'is_correct': False},
                    {'text': 'Thousands', 'is_correct': True}
                ],
                'explanation': 'In 47,356, the 7 is in the thousands place. From right to left: 6 (ones), 5 (tens), 3 (hundreds), 7 (thousands), 4 (ten thousands).'
            }
        ],

        'Fractions and Decimals': [
            {
                'text': 'What is 1/4 + 1/2?',
                'choices': [
                    {'text': '1/6', 'is_correct': False},
                    {'text': '2/6', 'is_correct': False},
                    {'text': '3/4', 'is_correct': True},
                    {'text': '1', 'is_correct': False}
                ],
                'explanation': 'To add fractions with different denominators, find a common denominator. 1/4 + 1/2 = 1/4 + 2/4 = 3/4.'
            },
            {
                'text': 'Which fraction is equivalent to 2/4?',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False}
                ],
                'explanation': '2/4 = 1/2 because both the numerator and denominator can be divided by 2. 2÷2 = 1 and 4÷2 = 2, so 2/4 = 1/2.'
            },
            {
                'text': 'What is 0.5 as a fraction?',
                'choices': [
                    {'text': '1/5', 'is_correct': False},
                    {'text': '1/2', 'is_correct': True},
                    {'text': '5/10', 'is_correct': False},
                    {'text': '1/4', 'is_correct': False}
                ],
                'explanation': '0.5 = 5/10 = 1/2. The decimal 0.5 means 5 tenths, which simplifies to 1/2.'
            },
            {
                'text': 'Which decimal is larger: 0.7 or 0.65?',
                'choices': [
                    {'text': '0.65', 'is_correct': False},
                    {'text': '0.7', 'is_correct': True},
                    {'text': 'They are equal', 'is_correct': False},
                    {'text': 'Cannot tell', 'is_correct': False}
                ],
                'explanation': '0.7 is larger than 0.65. You can think of 0.7 as 0.70, and 0.70 > 0.65.'
            },
            {
                'text': 'What is 3/5 of 20?',
                'choices': [
                    {'text': '10', 'is_correct': False},
                    {'text': '12', 'is_correct': True},
                    {'text': '15', 'is_correct': False},
                    {'text': '8', 'is_correct': False}
                ],
                'explanation': 'To find 3/5 of 20: First find 1/5 of 20 = 20÷5 = 4. Then 3/5 = 3×4 = 12.'
            }
        ],

        'Geometry and Shapes': [
            {
                'text': 'How many sides does a triangle have?',
                'choices': [
                    {'text': '2', 'is_correct': False},
                    {'text': '3', 'is_correct': True},
                    {'text': '4', 'is_correct': False},
                    {'text': '5', 'is_correct': False}
                ],
                'explanation': 'A triangle has 3 sides and 3 angles. The prefix "tri" means three.'
            },
            {
                'text': 'What is the perimeter of a rectangle with length 8 cm and width 5 cm?',
                'choices': [
                    {'text': '13 cm', 'is_correct': False},
                    {'text': '26 cm', 'is_correct': True},
                    {'text': '40 cm', 'is_correct': False},
                    {'text': '18 cm', 'is_correct': False}
                ],
                'explanation': 'Perimeter of a rectangle = 2 × (length + width) = 2 × (8 + 5) = 2 × 13 = 26 cm.'
            },
            {
                'text': 'What is the area of a square with side length 6 cm?',
                'choices': [
                    {'text': '24 cm²', 'is_correct': False},
                    {'text': '36 cm²', 'is_correct': True},
                    {'text': '12 cm²', 'is_correct': False},
                    {'text': '18 cm²', 'is_correct': False}
                ],
                'explanation': 'Area of a square = side × side = 6 × 6 = 36 cm². We write cm² to show it\'s a square measurement.'
            },
            {
                'text': 'Which shape has 4 equal sides and 4 right angles?',
                'choices': [
                    {'text': 'Rectangle', 'is_correct': False},
                    {'text': 'Triangle', 'is_correct': False},
                    {'text': 'Square', 'is_correct': True},
                    {'text': 'Circle', 'is_correct': False}
                ],
                'explanation': 'A square has 4 equal sides and 4 right angles (90° each). A rectangle has 4 right angles but opposite sides are equal, not all sides.'
            },
            {
                'text': 'How many vertices does a cube have?',
                'choices': [
                    {'text': '6', 'is_correct': False},
                    {'text': '8', 'is_correct': True},
                    {'text': '12', 'is_correct': False},
                    {'text': '4', 'is_correct': False}
                ],
                'explanation': 'A cube has 8 vertices (corners). It also has 6 faces and 12 edges.'
            }
        ],

        'Measurement': [
            {
                'text': 'How many centimeters are in 1 meter?',
                'choices': [
                    {'text': '10', 'is_correct': False},
                    {'text': '100', 'is_correct': True},
                    {'text': '1000', 'is_correct': False},
                    {'text': '50', 'is_correct': False}
                ],
                'explanation': 'There are 100 centimeters in 1 meter. The prefix "centi" means one hundredth.'
            },
            {
                'text': 'What is 2 hours and 30 minutes in minutes?',
                'choices': [
                    {'text': '120 minutes', 'is_correct': False},
                    {'text': '150 minutes', 'is_correct': True},
                    {'text': '130 minutes', 'is_correct': False},
                    {'text': '140 minutes', 'is_correct': False}
                ],
                'explanation': '2 hours = 2 × 60 = 120 minutes. Add 30 minutes: 120 + 30 = 150 minutes.'
            },
            {
                'text': 'How many grams are in 2 kilograms?',
                'choices': [
                    {'text': '200 grams', 'is_correct': False},
                    {'text': '2000 grams', 'is_correct': True},
                    {'text': '20 grams', 'is_correct': False},
                    {'text': '20000 grams', 'is_correct': False}
                ],
                'explanation': '1 kilogram = 1000 grams. So 2 kilograms = 2 × 1000 = 2000 grams.'
            },
            {
                'text': 'What time is shown when the hour hand is on 3 and the minute hand is on 6?',
                'choices': [
                    {'text': '3:30', 'is_correct': True},
                    {'text': '6:15', 'is_correct': False},
                    {'text': '3:06', 'is_correct': False},
                    {'text': '6:30', 'is_correct': False}
                ],
                'explanation': 'When the minute hand is on 6, it shows 30 minutes (6 × 5 = 30). The hour hand on 3 means 3 o\'clock. So the time is 3:30.'
            },
            {
                'text': 'Which is the best unit to measure the length of a pencil?',
                'choices': [
                    {'text': 'Kilometers', 'is_correct': False},
                    {'text': 'Meters', 'is_correct': False},
                    {'text': 'Centimeters', 'is_correct': True},
                    {'text': 'Millimeters', 'is_correct': False}
                ],
                'explanation': 'Centimeters is the best unit for measuring a pencil because pencils are usually about 15-20 cm long. Kilometers and meters are too big, millimeters would give a very large number.'
            }
        ],

        'Data Handling': [
            {
                'text': 'What is the mode in this set of numbers: 2, 3, 3, 4, 5, 3, 6?',
                'choices': [
                    {'text': '2', 'is_correct': False},
                    {'text': '3', 'is_correct': True},
                    {'text': '4', 'is_correct': False},
                    {'text': '5', 'is_correct': False}
                ],
                'explanation': 'The mode is the number that appears most often. In this set, 3 appears three times, which is more than any other number.'
            },
            {
                'text': 'In a bar graph, what does the height of each bar represent?',
                'choices': [
                    {'text': 'The color of the data', 'is_correct': False},
                    {'text': 'The frequency or amount of data', 'is_correct': True},
                    {'text': 'The width of the data', 'is_correct': False},
                    {'text': 'The type of data', 'is_correct': False}
                ],
                'explanation': 'In a bar graph, the height (or length) of each bar shows how much or how many of that item there are. This is called the frequency.'
            },
            {
                'text': 'What is the range of these numbers: 10, 15, 8, 20, 12?',
                'choices': [
                    {'text': '10', 'is_correct': False},
                    {'text': '12', 'is_correct': True},
                    {'text': '15', 'is_correct': False},
                    {'text': '20', 'is_correct': False}
                ],
                'explanation': 'Range = highest number - lowest number = 20 - 8 = 12. The range shows how spread out the numbers are.'
            },
            {
                'text': 'If you roll a dice, what is the probability of getting a number greater than 4?',
                'choices': [
                    {'text': '1/6', 'is_correct': False},
                    {'text': '2/6 or 1/3', 'is_correct': True},
                    {'text': '3/6 or 1/2', 'is_correct': False},
                    {'text': '4/6 or 2/3', 'is_correct': False}
                ],
                'explanation': 'Numbers greater than 4 on a dice are 5 and 6. That\'s 2 numbers out of 6 possible outcomes. So probability = 2/6 = 1/3.'
            }
        ]
    }


def create_mathematics_questions():
    """Create Mathematics questions for Primary 6."""
    try:
        # Get the Ghana curriculum and Primary 6 class level
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        math_subject = Subject.objects.get(name='Mathematics', class_level=primary6)

        print(f"Found Mathematics subject: {math_subject.name} - {math_subject.class_level.name}")

        questions_data = get_mathematics_questions_data()
        total_questions_created = 0

        for topic_name, topic_questions in questions_data.items():
            try:
                topic = Topic.objects.get(name=topic_name, subject=math_subject)
                print(f"\nProcessing topic: {topic.name}")

                # Remove existing questions for this topic to avoid duplicates
                existing_questions = Question.objects.filter(topic=topic)
                if existing_questions.exists():
                    print(f"  Removing {existing_questions.count()} existing questions...")
                    existing_questions.delete()

                questions_created = 0
                for question_data in topic_questions:
                    # Create the question
                    question = Question.objects.create(
                        text=question_data['text'],
                        question_type='multiple_choice',
                        difficulty='easy',  # Primary 6 level
                        explanation=question_data['explanation'],
                        curriculum=ghana_curriculum,
                        class_level=primary6,
                        subject=math_subject,
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

                    questions_created += 1

                print(f"  Created {questions_created} questions for {topic.name}")
                total_questions_created += questions_created

            except Topic.DoesNotExist:
                print(f"  Topic '{topic_name}' not found, skipping...")

        print(f"\nTotal Mathematics questions created: {total_questions_created}")

        # Create or update the Mathematics quiz
        quiz, created = Quiz.objects.get_or_create(
            title="Mathematics Quiz - Primary 6",
            curriculum=ghana_curriculum,
            class_level=primary6,
            subject=math_subject,
            defaults={
                'description': 'Test your knowledge of Mathematics concepts for Primary 6 level',
                'quiz_type': 'general',
                'question_count': total_questions_created,
                'per_question_time': 60,  # 60 seconds per question for Primary 6 math
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 60,  # 60% passing score for Primary 6
                'is_active': True,
                'is_featured': True
            }
        )

        if created:
            print(f"Created quiz: {quiz.title}")
        else:
            # Update question count
            quiz.question_count = total_questions_created
            quiz.save()
            print(f"Updated quiz: {quiz.title}")

        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("Adding comprehensive Mathematics questions for Primary 6...")
    success = create_mathematics_questions()

    if success:
        print("\nMathematics questions added successfully!")
    else:
        print("\nFailed to add Mathematics questions.")
