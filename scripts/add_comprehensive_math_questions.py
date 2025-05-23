#!/usr/bin/env python
"""
Script to add comprehensive Mathematics questions for Primary 5 and Primary 6.
Based on GES Mathematics curriculum with international standards.
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


def get_comprehensive_math_questions_data():
    """Return comprehensive Mathematics questions based on GES curriculum."""
    return {
        'Numbers and Operations': [
            {
                'text': 'What is the place value of 7 in the number 47,832?',
                'choices': [
                    {'text': 'Ones', 'is_correct': False},
                    {'text': 'Tens', 'is_correct': False},
                    {'text': 'Thousands', 'is_correct': True},
                    {'text': 'Ten thousands', 'is_correct': False}
                ],
                'explanation': 'In 47,832, the digit 7 is in the thousands place. From right to left: 2 (ones), 3 (tens), 8 (hundreds), 7 (thousands), 4 (ten thousands).'
            },
            {
                'text': 'Round 3,847 to the nearest hundred.',
                'choices': [
                    {'text': '3,800', 'is_correct': True},
                    {'text': '3,850', 'is_correct': False},
                    {'text': '3,900', 'is_correct': False},
                    {'text': '4,000', 'is_correct': False}
                ],
                'explanation': 'To round to the nearest hundred, look at the tens digit. Since 4 is less than 5, we round down to 3,800.'
            },
            {
                'text': 'What is 456 × 23?',
                'choices': [
                    {'text': '10,488', 'is_correct': True},
                    {'text': '10,388', 'is_correct': False},
                    {'text': '10,588', 'is_correct': False},
                    {'text': '9,488', 'is_correct': False}
                ],
                'explanation': '456 × 23 = 456 × 20 + 456 × 3 = 9,120 + 1,368 = 10,488'
            },
            {
                'text': 'What is 2,484 ÷ 12?',
                'choices': [
                    {'text': '207', 'is_correct': True},
                    {'text': '206', 'is_correct': False},
                    {'text': '208', 'is_correct': False},
                    {'text': '205', 'is_correct': False}
                ],
                'explanation': '2,484 ÷ 12 = 207. You can check: 207 × 12 = 2,484'
            },
            {
                'text': 'Which number is a prime number?',
                'choices': [
                    {'text': '15', 'is_correct': False},
                    {'text': '21', 'is_correct': False},
                    {'text': '17', 'is_correct': True},
                    {'text': '25', 'is_correct': False}
                ],
                'explanation': '17 is a prime number because it can only be divided by 1 and itself. 15=3×5, 21=3×7, 25=5×5, but 17 has no other factors.'
            },
            {
                'text': 'What is the least common multiple (LCM) of 6 and 8?',
                'choices': [
                    {'text': '24', 'is_correct': True},
                    {'text': '14', 'is_correct': False},
                    {'text': '48', 'is_correct': False},
                    {'text': '12', 'is_correct': False}
                ],
                'explanation': 'Multiples of 6: 6, 12, 18, 24... Multiples of 8: 8, 16, 24... The smallest common multiple is 24.'
            },
            {
                'text': 'What is the greatest common factor (GCF) of 18 and 24?',
                'choices': [
                    {'text': '6', 'is_correct': True},
                    {'text': '3', 'is_correct': False},
                    {'text': '9', 'is_correct': False},
                    {'text': '12', 'is_correct': False}
                ],
                'explanation': 'Factors of 18: 1, 2, 3, 6, 9, 18. Factors of 24: 1, 2, 3, 4, 6, 8, 12, 24. The greatest common factor is 6.'
            },
            {
                'text': 'Express 45 as a product of prime factors.',
                'choices': [
                    {'text': '3² × 5', 'is_correct': True},
                    {'text': '3 × 15', 'is_correct': False},
                    {'text': '5 × 9', 'is_correct': False},
                    {'text': '3 × 5²', 'is_correct': False}
                ],
                'explanation': '45 = 9 × 5 = 3² × 5. Both 3 and 5 are prime numbers, so 45 = 3² × 5.'
            }
        ],

        'Fractions and Decimals': [
            {
                'text': 'What is 3/4 + 1/6?',
                'choices': [
                    {'text': '11/12', 'is_correct': True},
                    {'text': '4/10', 'is_correct': False},
                    {'text': '5/6', 'is_correct': False},
                    {'text': '7/8', 'is_correct': False}
                ],
                'explanation': 'To add fractions, find common denominator: 3/4 = 9/12, 1/6 = 2/12. So 9/12 + 2/12 = 11/12.'
            },
            {
                'text': 'What is 5/6 - 1/4?',
                'choices': [
                    {'text': '7/12', 'is_correct': True},
                    {'text': '4/2', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False}
                ],
                'explanation': 'Common denominator is 12: 5/6 = 10/12, 1/4 = 3/12. So 10/12 - 3/12 = 7/12.'
            },
            {
                'text': 'What is 2/3 × 3/4?',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '5/7', 'is_correct': False},
                    {'text': '6/12', 'is_correct': False},
                    {'text': '2/4', 'is_correct': False}
                ],
                'explanation': 'Multiply numerators and denominators: (2×3)/(3×4) = 6/12 = 1/2.'
            },
            {
                'text': 'Convert 0.75 to a fraction in simplest form.',
                'choices': [
                    {'text': '3/4', 'is_correct': True},
                    {'text': '75/100', 'is_correct': False},
                    {'text': '7/10', 'is_correct': False},
                    {'text': '15/20', 'is_correct': False}
                ],
                'explanation': '0.75 = 75/100. Simplify by dividing both by 25: 75÷25 = 3, 100÷25 = 4. So 0.75 = 3/4.'
            },
            {
                'text': 'What is 2.45 + 3.7?',
                'choices': [
                    {'text': '6.15', 'is_correct': True},
                    {'text': '5.15', 'is_correct': False},
                    {'text': '6.12', 'is_correct': False},
                    {'text': '5.12', 'is_correct': False}
                ],
                'explanation': 'Line up decimal points: 2.45 + 3.70 = 6.15.'
            },
            {
                'text': 'What is 8.4 ÷ 2.1?',
                'choices': [
                    {'text': '4', 'is_correct': True},
                    {'text': '3.5', 'is_correct': False},
                    {'text': '4.2', 'is_correct': False},
                    {'text': '3.8', 'is_correct': False}
                ],
                'explanation': '8.4 ÷ 2.1 = 84 ÷ 21 = 4. You can multiply both numbers by 10 to remove decimals.'
            },
            {
                'text': 'Which decimal is equivalent to 7/8?',
                'choices': [
                    {'text': '0.875', 'is_correct': True},
                    {'text': '0.78', 'is_correct': False},
                    {'text': '0.87', 'is_correct': False},
                    {'text': '0.8', 'is_correct': False}
                ],
                'explanation': '7 ÷ 8 = 0.875. You can verify: 0.875 × 8 = 7.'
            }
        ],

        'Geometry and Shapes': [
            {
                'text': 'How many sides does a hexagon have?',
                'choices': [
                    {'text': '5', 'is_correct': False},
                    {'text': '6', 'is_correct': True},
                    {'text': '7', 'is_correct': False},
                    {'text': '8', 'is_correct': False}
                ],
                'explanation': 'A hexagon has 6 sides. The prefix "hex" means six.'
            },
            {
                'text': 'What is the area of a rectangle with length 8 cm and width 5 cm?',
                'choices': [
                    {'text': '40 cm²', 'is_correct': True},
                    {'text': '26 cm²', 'is_correct': False},
                    {'text': '13 cm²', 'is_correct': False},
                    {'text': '35 cm²', 'is_correct': False}
                ],
                'explanation': 'Area of rectangle = length × width = 8 × 5 = 40 cm².'
            },
            {
                'text': 'What is the perimeter of a square with side length 7 cm?',
                'choices': [
                    {'text': '28 cm', 'is_correct': True},
                    {'text': '49 cm', 'is_correct': False},
                    {'text': '14 cm', 'is_correct': False},
                    {'text': '21 cm', 'is_correct': False}
                ],
                'explanation': 'Perimeter of square = 4 × side length = 4 × 7 = 28 cm.'
            },
            {
                'text': 'What type of angle measures exactly 90 degrees?',
                'choices': [
                    {'text': 'Acute angle', 'is_correct': False},
                    {'text': 'Right angle', 'is_correct': True},
                    {'text': 'Obtuse angle', 'is_correct': False},
                    {'text': 'Straight angle', 'is_correct': False}
                ],
                'explanation': 'A right angle measures exactly 90 degrees. It forms a perfect corner like the corner of a square.'
            },
            {
                'text': 'How many lines of symmetry does a circle have?',
                'choices': [
                    {'text': '1', 'is_correct': False},
                    {'text': '4', 'is_correct': False},
                    {'text': 'Infinite', 'is_correct': True},
                    {'text': '8', 'is_correct': False}
                ],
                'explanation': 'A circle has infinite lines of symmetry. Any line passing through the center divides the circle into two identical halves.'
            },
            {
                'text': 'What is the area of a triangle with base 6 cm and height 4 cm?',
                'choices': [
                    {'text': '12 cm²', 'is_correct': True},
                    {'text': '24 cm²', 'is_correct': False},
                    {'text': '10 cm²', 'is_correct': False},
                    {'text': '20 cm²', 'is_correct': False}
                ],
                'explanation': 'Area of triangle = (1/2) × base × height = (1/2) × 6 × 4 = 12 cm².'
            },
            {
                'text': 'What is the sum of interior angles in a triangle?',
                'choices': [
                    {'text': '180°', 'is_correct': True},
                    {'text': '360°', 'is_correct': False},
                    {'text': '90°', 'is_correct': False},
                    {'text': '270°', 'is_correct': False}
                ],
                'explanation': 'The sum of all interior angles in any triangle is always 180 degrees.'
            }
        ],

        'Measurement': [
            {
                'text': 'How many centimeters are in 2.5 meters?',
                'choices': [
                    {'text': '250 cm', 'is_correct': True},
                    {'text': '25 cm', 'is_correct': False},
                    {'text': '2500 cm', 'is_correct': False},
                    {'text': '2.5 cm', 'is_correct': False}
                ],
                'explanation': '1 meter = 100 centimeters, so 2.5 meters = 2.5 × 100 = 250 centimeters.'
            },
            {
                'text': 'How many minutes are in 3.5 hours?',
                'choices': [
                    {'text': '210 minutes', 'is_correct': True},
                    {'text': '180 minutes', 'is_correct': False},
                    {'text': '350 minutes', 'is_correct': False},
                    {'text': '35 minutes', 'is_correct': False}
                ],
                'explanation': '1 hour = 60 minutes, so 3.5 hours = 3.5 × 60 = 210 minutes.'
            },
            {
                'text': 'What is the volume of a cube with side length 4 cm?',
                'choices': [
                    {'text': '64 cm³', 'is_correct': True},
                    {'text': '16 cm³', 'is_correct': False},
                    {'text': '48 cm³', 'is_correct': False},
                    {'text': '12 cm³', 'is_correct': False}
                ],
                'explanation': 'Volume of cube = side³ = 4³ = 4 × 4 × 4 = 64 cm³.'
            },
            {
                'text': 'How many grams are in 2.3 kilograms?',
                'choices': [
                    {'text': '2,300 g', 'is_correct': True},
                    {'text': '230 g', 'is_correct': False},
                    {'text': '23 g', 'is_correct': False},
                    {'text': '23,000 g', 'is_correct': False}
                ],
                'explanation': '1 kilogram = 1,000 grams, so 2.3 kg = 2.3 × 1,000 = 2,300 grams.'
            },
            {
                'text': 'What is the capacity of a rectangular tank with length 5m, width 3m, and height 2m?',
                'choices': [
                    {'text': '30 m³', 'is_correct': True},
                    {'text': '10 m³', 'is_correct': False},
                    {'text': '20 m³', 'is_correct': False},
                    {'text': '15 m³', 'is_correct': False}
                ],
                'explanation': 'Volume = length × width × height = 5 × 3 × 2 = 30 cubic meters.'
            },
            {
                'text': 'How many milliliters are in 1.5 liters?',
                'choices': [
                    {'text': '1,500 ml', 'is_correct': True},
                    {'text': '150 ml', 'is_correct': False},
                    {'text': '15 ml', 'is_correct': False},
                    {'text': '15,000 ml', 'is_correct': False}
                ],
                'explanation': '1 liter = 1,000 milliliters, so 1.5 liters = 1.5 × 1,000 = 1,500 ml.'
            }
        ],

        'Data Handling and Statistics': [
            {
                'text': 'What is the mean of these numbers: 8, 12, 6, 14, 10?',
                'choices': [
                    {'text': '10', 'is_correct': True},
                    {'text': '12', 'is_correct': False},
                    {'text': '8', 'is_correct': False},
                    {'text': '9', 'is_correct': False}
                ],
                'explanation': 'Mean = (8 + 12 + 6 + 14 + 10) ÷ 5 = 50 ÷ 5 = 10.'
            },
            {
                'text': 'What is the median of these numbers: 3, 7, 5, 9, 6?',
                'choices': [
                    {'text': '6', 'is_correct': True},
                    {'text': '5', 'is_correct': False},
                    {'text': '7', 'is_correct': False},
                    {'text': '6.5', 'is_correct': False}
                ],
                'explanation': 'First arrange in order: 3, 5, 6, 7, 9. The median is the middle number: 6.'
            },
            {
                'text': 'What is the mode of these numbers: 4, 7, 4, 9, 4, 6, 7?',
                'choices': [
                    {'text': '4', 'is_correct': True},
                    {'text': '7', 'is_correct': False},
                    {'text': '6', 'is_correct': False},
                    {'text': '9', 'is_correct': False}
                ],
                'explanation': 'The mode is the number that appears most frequently. 4 appears 3 times, more than any other number.'
            },
            {
                'text': 'What is the range of these numbers: 15, 8, 23, 12, 19?',
                'choices': [
                    {'text': '15', 'is_correct': True},
                    {'text': '23', 'is_correct': False},
                    {'text': '8', 'is_correct': False},
                    {'text': '11', 'is_correct': False}
                ],
                'explanation': 'Range = highest value - lowest value = 23 - 8 = 15.'
            },
            {
                'text': 'In a bar chart, what does the height of each bar represent?',
                'choices': [
                    {'text': 'The frequency or value of that category', 'is_correct': True},
                    {'text': 'The width of the category', 'is_correct': False},
                    {'text': 'The color of the category', 'is_correct': False},
                    {'text': 'The position of the category', 'is_correct': False}
                ],
                'explanation': 'In a bar chart, the height (or length) of each bar represents the frequency or value of that category.'
            }
        ],

        'Patterns and Algebra': [
            {
                'text': 'What is the next number in this pattern: 2, 6, 18, 54, ?',
                'choices': [
                    {'text': '162', 'is_correct': True},
                    {'text': '108', 'is_correct': False},
                    {'text': '72', 'is_correct': False},
                    {'text': '216', 'is_correct': False}
                ],
                'explanation': 'Each number is multiplied by 3: 2×3=6, 6×3=18, 18×3=54, 54×3=162.'
            },
            {
                'text': 'If x + 7 = 15, what is the value of x?',
                'choices': [
                    {'text': '8', 'is_correct': True},
                    {'text': '22', 'is_correct': False},
                    {'text': '7', 'is_correct': False},
                    {'text': '15', 'is_correct': False}
                ],
                'explanation': 'To solve x + 7 = 15, subtract 7 from both sides: x = 15 - 7 = 8.'
            },
            {
                'text': 'What is the rule for this pattern: 5, 10, 15, 20, 25?',
                'choices': [
                    {'text': 'Add 5', 'is_correct': True},
                    {'text': 'Multiply by 2', 'is_correct': False},
                    {'text': 'Add 10', 'is_correct': False},
                    {'text': 'Subtract 5', 'is_correct': False}
                ],
                'explanation': 'Each number increases by 5: 5+5=10, 10+5=15, 15+5=20, 20+5=25.'
            },
            {
                'text': 'If 3y = 21, what is y?',
                'choices': [
                    {'text': '7', 'is_correct': True},
                    {'text': '18', 'is_correct': False},
                    {'text': '24', 'is_correct': False},
                    {'text': '63', 'is_correct': False}
                ],
                'explanation': 'To solve 3y = 21, divide both sides by 3: y = 21 ÷ 3 = 7.'
            }
        ],

        'Money and Financial Literacy': [
            {
                'text': 'How much change will you get from GH₵20 if you buy items costing GH₵7.50 and GH₵8.25?',
                'choices': [
                    {'text': 'GH₵4.25', 'is_correct': True},
                    {'text': 'GH₵4.75', 'is_correct': False},
                    {'text': 'GH₵3.25', 'is_correct': False},
                    {'text': 'GH₵5.25', 'is_correct': False}
                ],
                'explanation': 'Total cost = GH₵7.50 + GH₵8.25 = GH₵15.75. Change = GH₵20.00 - GH₵15.75 = GH₵4.25.'
            },
            {
                'text': 'If you save GH₵5 every week, how much will you have after 8 weeks?',
                'choices': [
                    {'text': 'GH₵40', 'is_correct': True},
                    {'text': 'GH₵35', 'is_correct': False},
                    {'text': 'GH₵45', 'is_correct': False},
                    {'text': 'GH₵13', 'is_correct': False}
                ],
                'explanation': 'Total savings = GH₵5 × 8 weeks = GH₵40.'
            },
            {
                'text': 'What is 15% of GH₵80?',
                'choices': [
                    {'text': 'GH₵12', 'is_correct': True},
                    {'text': 'GH₵15', 'is_correct': False},
                    {'text': 'GH₵10', 'is_correct': False},
                    {'text': 'GH₵20', 'is_correct': False}
                ],
                'explanation': '15% of GH₵80 = 15/100 × 80 = 0.15 × 80 = GH₵12.'
            },
            {
                'text': 'If a shirt costs GH₵25 and is on sale for 20% off, what is the sale price?',
                'choices': [
                    {'text': 'GH₵20', 'is_correct': True},
                    {'text': 'GH₵22', 'is_correct': False},
                    {'text': 'GH₵30', 'is_correct': False},
                    {'text': 'GH₵5', 'is_correct': False}
                ],
                'explanation': '20% off means you pay 80%. 80% of GH₵25 = 0.8 × 25 = GH₵20.'
            }
        ],

        'Problem Solving and Reasoning': [
            {
                'text': 'A bus can carry 45 passengers. How many buses are needed to transport 180 students?',
                'choices': [
                    {'text': '4 buses', 'is_correct': True},
                    {'text': '3 buses', 'is_correct': False},
                    {'text': '5 buses', 'is_correct': False},
                    {'text': '225 buses', 'is_correct': False}
                ],
                'explanation': '180 ÷ 45 = 4. So 4 buses are needed to transport all 180 students.'
            },
            {
                'text': 'Mary has 3 times as many stickers as John. If John has 12 stickers, how many do they have together?',
                'choices': [
                    {'text': '48 stickers', 'is_correct': True},
                    {'text': '36 stickers', 'is_correct': False},
                    {'text': '15 stickers', 'is_correct': False},
                    {'text': '24 stickers', 'is_correct': False}
                ],
                'explanation': 'Mary has 3 × 12 = 36 stickers. Together: 36 + 12 = 48 stickers.'
            },
            {
                'text': 'A rectangular garden is 12m long and 8m wide. What is the cost to fence it if fencing costs GH₵15 per meter?',
                'choices': [
                    {'text': 'GH₵600', 'is_correct': True},
                    {'text': 'GH₵300', 'is_correct': False},
                    {'text': 'GH₵1,440', 'is_correct': False},
                    {'text': 'GH₵180', 'is_correct': False}
                ],
                'explanation': 'Perimeter = 2(12 + 8) = 40m. Cost = 40 × GH₵15 = GH₵600.'
            },
            {
                'text': 'If it takes 6 workers 8 days to complete a job, how long will it take 4 workers?',
                'choices': [
                    {'text': '12 days', 'is_correct': True},
                    {'text': '10 days', 'is_correct': False},
                    {'text': '6 days', 'is_correct': False},
                    {'text': '8 days', 'is_correct': False}
                ],
                'explanation': 'Total work = 6 × 8 = 48 worker-days. With 4 workers: 48 ÷ 4 = 12 days.'
            }
        ]
    }


def create_comprehensive_math_questions():
    """Create comprehensive Mathematics questions for both Primary 5 and Primary 6."""
    try:
        # Get the Ghana curriculum and class levels
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary5 = ClassLevel.objects.get(name='Primary 5', curriculum=ghana_curriculum)
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)

        # Get Mathematics subjects for both classes
        math_subject_p5 = Subject.objects.get(name='Mathematics', class_level=primary5)
        math_subject_p6 = Subject.objects.get(name='Mathematics', class_level=primary6)

        print(f"Adding comprehensive Mathematics questions based on GES curriculum...")
        print(f"- {math_subject_p5.name} - {math_subject_p5.class_level.name}")
        print(f"- {math_subject_p6.name} - {math_subject_p6.class_level.name}")

        questions_data = get_comprehensive_math_questions_data()
        total_questions_created = 0

        # Create questions for both Primary 5 and Primary 6
        for class_level, math_subject in [(primary5, math_subject_p5), (primary6, math_subject_p6)]:
            print(f"\nProcessing {class_level.name}...")

            class_questions_created = 0

            for topic_name, topic_questions in questions_data.items():
                # Create or get the topic
                topic, created = Topic.objects.get_or_create(
                    name=topic_name,
                    subject=math_subject,
                    defaults={
                        'description': f'{topic_name} concepts based on GES Mathematics curriculum for {class_level.name}'
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
                        difficulty='medium',  # Primary level mathematics
                        explanation=question_data['explanation'],
                        curriculum=ghana_curriculum,
                        class_level=class_level,
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

                    topic_questions_created += 1

                print(f"    Added {topic_questions_created} questions to {topic.name}")
                class_questions_created += topic_questions_created

            print(f"  Total new Mathematics questions created for {class_level.name}: {class_questions_created}")
            total_questions_created += class_questions_created

            # Update the existing Mathematics quiz with new question count
            try:
                quiz = Quiz.objects.get(
                    title=f"Mathematics Quiz - {class_level.name}",
                    curriculum=ghana_curriculum,
                    class_level=class_level,
                    subject=math_subject
                )

                # Count all Mathematics questions for this class
                total_math_questions = Question.objects.filter(subject=math_subject).count()
                quiz.question_count = total_math_questions
                quiz.description = f'Comprehensive Mathematics test covering numbers, fractions, geometry, measurement, data handling, algebra, and problem solving for {class_level.name} level'
                quiz.per_question_time = 90  # More time for math problems
                quiz.save()

                print(f"  Updated quiz: {quiz.title} (Total questions: {total_math_questions})")

            except Quiz.DoesNotExist:
                print(f"  Warning: Mathematics Quiz for {class_level.name} not found")

        print(f"\nTotal new Mathematics questions created: {total_questions_created}")

        # Show final Mathematics topic structure
        print(f"\nFinal Mathematics curriculum structure:")
        for class_level in [primary5, primary6]:
            math_subject = Subject.objects.get(name='Mathematics', class_level=class_level)
            topics = Topic.objects.filter(subject=math_subject).order_by('name')
            total_questions = Question.objects.filter(subject=math_subject).count()

            print(f"\n{class_level.name} Mathematics ({total_questions} total questions):")
            for topic in topics:
                question_count = Question.objects.filter(topic=topic).count()
                print(f"  - {topic.name}: {question_count} questions")

        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("🧮 Adding comprehensive Mathematics questions based on GES curriculum...")
    print("📚 Topics: Numbers, Fractions, Geometry, Measurement, Data, Algebra, Problem Solving")

    success = create_comprehensive_math_questions()

    if success:
        print("\n🎉 Comprehensive Mathematics questions added successfully!")
        print("🌍 Your Mathematics curriculum now covers all essential topics!")
        print("🏆 Students will have excellent mathematical foundation!")
    else:
        print("\n❌ Failed to add comprehensive Mathematics questions.")
