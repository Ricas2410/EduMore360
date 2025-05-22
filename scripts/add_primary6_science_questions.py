#!/usr/bin/env python
"""
Script to add comprehensive Science questions for Primary 6 Ghana Curriculum.
Based on the Ghana Education Service (GES) Science curriculum for Primary 6.
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


def get_science_questions_data():
    """Return comprehensive Science questions for Primary 6 based on GES curriculum."""
    return {
        'Living Things': [
            {
                'text': 'Which of these is NOT a characteristic of living things?',
                'choices': [
                    {'text': 'Growth', 'is_correct': False},
                    {'text': 'Respiration', 'is_correct': False},
                    {'text': 'Magnetism', 'is_correct': True},
                    {'text': 'Reproduction', 'is_correct': False}
                ],
                'explanation': 'Magnetism is a physical property of certain materials, not a characteristic of living things. Living things exhibit growth, respiration, reproduction, movement, sensitivity, nutrition, and excretion.'
            },
            {
                'text': 'What do plants need to make their own food?',
                'choices': [
                    {'text': 'Sunlight, water, and carbon dioxide', 'is_correct': True},
                    {'text': 'Only water', 'is_correct': False},
                    {'text': 'Only sunlight', 'is_correct': False},
                    {'text': 'Soil and rocks', 'is_correct': False}
                ],
                'explanation': 'Plants make their own food through photosynthesis, which requires sunlight, water, and carbon dioxide. They use chlorophyll in their leaves to capture sunlight and convert these materials into food.'
            },
            {
                'text': 'Which part of a plant absorbs water and nutrients from the soil?',
                'choices': [
                    {'text': 'Leaves', 'is_correct': False},
                    {'text': 'Stem', 'is_correct': False},
                    {'text': 'Roots', 'is_correct': True},
                    {'text': 'Flowers', 'is_correct': False}
                ],
                'explanation': 'Roots absorb water and nutrients from the soil. They also anchor the plant in the ground and store food for the plant.'
            },
            {
                'text': 'What is the life cycle order of a butterfly?',
                'choices': [
                    {'text': 'Egg → Larva → Pupa → Adult', 'is_correct': True},
                    {'text': 'Egg → Pupa → Larva → Adult', 'is_correct': False},
                    {'text': 'Larva → Egg → Pupa → Adult', 'is_correct': False},
                    {'text': 'Adult → Larva → Egg → Pupa', 'is_correct': False}
                ],
                'explanation': 'The butterfly life cycle is: Egg → Larva (caterpillar) → Pupa (chrysalis) → Adult butterfly. This process is called complete metamorphosis.'
            },
            {
                'text': 'Which animals are herbivores?',
                'choices': [
                    {'text': 'Lions and tigers', 'is_correct': False},
                    {'text': 'Cows and goats', 'is_correct': True},
                    {'text': 'Eagles and hawks', 'is_correct': False},
                    {'text': 'Sharks and crocodiles', 'is_correct': False}
                ],
                'explanation': 'Herbivores are animals that eat only plants. Cows and goats are herbivores. Lions, tigers, eagles, hawks, sharks, and crocodiles are carnivores (meat-eaters).'
            }
        ],

        'Human Body': [
            {
                'text': 'Which organ pumps blood around the body?',
                'choices': [
                    {'text': 'Lungs', 'is_correct': False},
                    {'text': 'Heart', 'is_correct': True},
                    {'text': 'Stomach', 'is_correct': False},
                    {'text': 'Brain', 'is_correct': False}
                ],
                'explanation': 'The heart is a muscular organ that pumps blood around the body through blood vessels. It beats about 70-100 times per minute to keep blood flowing.'
            },
            {
                'text': 'What is the main function of the lungs?',
                'choices': [
                    {'text': 'To digest food', 'is_correct': False},
                    {'text': 'To pump blood', 'is_correct': False},
                    {'text': 'To help us breathe and exchange gases', 'is_correct': True},
                    {'text': 'To think and control the body', 'is_correct': False}
                ],
                'explanation': 'The lungs help us breathe by taking in oxygen from the air and removing carbon dioxide from our blood. This process is called gas exchange.'
            },
            {
                'text': 'How many bones are there approximately in an adult human body?',
                'choices': [
                    {'text': '106', 'is_correct': False},
                    {'text': '206', 'is_correct': True},
                    {'text': '306', 'is_correct': False},
                    {'text': '406', 'is_correct': False}
                ],
                'explanation': 'An adult human body has approximately 206 bones. Babies are born with about 270 bones, but many of these fuse together as they grow.'
            },
            {
                'text': 'Which part of the body controls all other body functions?',
                'choices': [
                    {'text': 'Heart', 'is_correct': False},
                    {'text': 'Brain', 'is_correct': True},
                    {'text': 'Lungs', 'is_correct': False},
                    {'text': 'Stomach', 'is_correct': False}
                ],
                'explanation': 'The brain controls all body functions including thinking, movement, breathing, and heartbeat. It receives information from our senses and sends signals to different parts of the body.'
            },
            {
                'text': 'What should you do to keep your teeth healthy?',
                'choices': [
                    {'text': 'Eat lots of sweets', 'is_correct': False},
                    {'text': 'Brush twice daily and avoid too much sugar', 'is_correct': True},
                    {'text': 'Never brush your teeth', 'is_correct': False},
                    {'text': 'Only drink soft drinks', 'is_correct': False}
                ],
                'explanation': 'To keep teeth healthy, brush them at least twice daily, floss regularly, avoid too much sugar and acidic foods, and visit the dentist regularly for check-ups.'
            }
        ],

        'Materials': [
            {
                'text': 'Which of these materials can conduct electricity?',
                'choices': [
                    {'text': 'Plastic', 'is_correct': False},
                    {'text': 'Wood', 'is_correct': False},
                    {'text': 'Copper', 'is_correct': True},
                    {'text': 'Rubber', 'is_correct': False}
                ],
                'explanation': 'Copper is a metal that can conduct electricity very well. That\'s why it\'s used in electrical wires. Plastic, wood, and rubber are insulators that do not conduct electricity.'
            },
            {
                'text': 'What happens when you heat ice?',
                'choices': [
                    {'text': 'It becomes harder', 'is_correct': False},
                    {'text': 'It melts and becomes water', 'is_correct': True},
                    {'text': 'It stays the same', 'is_correct': False},
                    {'text': 'It becomes gas immediately', 'is_correct': False}
                ],
                'explanation': 'When ice is heated, it melts and changes from solid to liquid (water). This happens at 0°C (32°F). This is called a change of state.'
            },
            {
                'text': 'Which material is transparent?',
                'choices': [
                    {'text': 'Wood', 'is_correct': False},
                    {'text': 'Metal', 'is_correct': False},
                    {'text': 'Glass', 'is_correct': True},
                    {'text': 'Clay', 'is_correct': False}
                ],
                'explanation': 'Glass is transparent, which means you can see through it clearly. Wood, metal, and clay are opaque materials that you cannot see through.'
            },
            {
                'text': 'What is the difference between solids, liquids, and gases?',
                'choices': [
                    {'text': 'They have different colors', 'is_correct': False},
                    {'text': 'They have different shapes and how particles move', 'is_correct': True},
                    {'text': 'They have different weights only', 'is_correct': False},
                    {'text': 'There is no difference', 'is_correct': False}
                ],
                'explanation': 'Solids have fixed shape and volume with particles close together. Liquids have fixed volume but take the shape of their container. Gases have no fixed shape or volume and particles move freely.'
            },
            {
                'text': 'Which process can separate salt from salt water?',
                'choices': [
                    {'text': 'Freezing', 'is_correct': False},
                    {'text': 'Evaporation', 'is_correct': True},
                    {'text': 'Mixing', 'is_correct': False},
                    {'text': 'Cooling', 'is_correct': False}
                ],
                'explanation': 'Evaporation can separate salt from salt water. When the water evaporates (turns to gas), the salt is left behind as a solid because salt doesn\'t evaporate at normal temperatures.'
            }
        ],

        'Energy and Forces': [
            {
                'text': 'What type of energy do we get from food?',
                'choices': [
                    {'text': 'Light energy', 'is_correct': False},
                    {'text': 'Chemical energy', 'is_correct': True},
                    {'text': 'Sound energy', 'is_correct': False},
                    {'text': 'Electrical energy', 'is_correct': False}
                ],
                'explanation': 'Food contains chemical energy that our bodies convert into other forms of energy we need for movement, growth, and staying warm.'
            },
            {
                'text': 'What happens when you rub your hands together quickly?',
                'choices': [
                    {'text': 'They become cold', 'is_correct': False},
                    {'text': 'They become warm due to friction', 'is_correct': True},
                    {'text': 'Nothing happens', 'is_correct': False},
                    {'text': 'They become wet', 'is_correct': False}
                ],
                'explanation': 'When you rub your hands together, friction between them converts movement energy into heat energy, making your hands warm.'
            },
            {
                'text': 'Which force pulls objects toward the Earth?',
                'choices': [
                    {'text': 'Magnetism', 'is_correct': False},
                    {'text': 'Gravity', 'is_correct': True},
                    {'text': 'Friction', 'is_correct': False},
                    {'text': 'Electricity', 'is_correct': False}
                ],
                'explanation': 'Gravity is the force that pulls all objects toward the Earth. This is why things fall down when you drop them and why we stay on the ground.'
            },
            {
                'text': 'What do we call energy from the sun?',
                'choices': [
                    {'text': 'Wind energy', 'is_correct': False},
                    {'text': 'Solar energy', 'is_correct': True},
                    {'text': 'Water energy', 'is_correct': False},
                    {'text': 'Nuclear energy', 'is_correct': False}
                ],
                'explanation': 'Energy from the sun is called solar energy. The sun provides light and heat energy that powers many processes on Earth, including photosynthesis in plants.'
            }
        ],

        'Earth and Space': [
            {
                'text': 'How long does it take for the Earth to orbit around the Sun?',
                'choices': [
                    {'text': 'One day', 'is_correct': False},
                    {'text': 'One month', 'is_correct': False},
                    {'text': 'One year', 'is_correct': True},
                    {'text': 'One week', 'is_correct': False}
                ],
                'explanation': 'It takes the Earth one year (365.25 days) to complete one orbit around the Sun. This is why we have seasons and why a year is 365 days long.'
            },
            {
                'text': 'What causes day and night?',
                'choices': [
                    {'text': 'The Earth moving around the Sun', 'is_correct': False},
                    {'text': 'The Earth spinning on its axis', 'is_correct': True},
                    {'text': 'The Moon moving around Earth', 'is_correct': False},
                    {'text': 'Clouds covering the Sun', 'is_correct': False}
                ],
                'explanation': 'Day and night are caused by the Earth spinning (rotating) on its axis. When your part of Earth faces the Sun, it\'s day. When it faces away from the Sun, it\'s night.'
            },
            {
                'text': 'Which is the closest star to Earth?',
                'choices': [
                    {'text': 'The Moon', 'is_correct': False},
                    {'text': 'The Sun', 'is_correct': True},
                    {'text': 'Mars', 'is_correct': False},
                    {'text': 'Venus', 'is_correct': False}
                ],
                'explanation': 'The Sun is the closest star to Earth. The Moon is not a star (it\'s a satellite), and Mars and Venus are planets, not stars.'
            },
            {
                'text': 'What are the three main layers of the Earth?',
                'choices': [
                    {'text': 'Crust, mantle, and core', 'is_correct': True},
                    {'text': 'Land, water, and air', 'is_correct': False},
                    {'text': 'Top, middle, and bottom', 'is_correct': False},
                    {'text': 'Hot, warm, and cold', 'is_correct': False}
                ],
                'explanation': 'The Earth has three main layers: the crust (outer layer where we live), the mantle (hot rock layer), and the core (very hot center made mostly of iron).'
            }
        ]
    }


def create_science_questions():
    """Create Science questions for Primary 6."""
    try:
        # Get the Ghana curriculum and Primary 6 class level
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        science_subject = Subject.objects.get(name='Science', class_level=primary6)

        print(f"Found Science subject: {science_subject.name} - {science_subject.class_level.name}")

        questions_data = get_science_questions_data()
        total_questions_created = 0

        for topic_name, topic_questions in questions_data.items():
            try:
                topic = Topic.objects.get(name=topic_name, subject=science_subject)
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
                        subject=science_subject,
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

        print(f"\nTotal Science questions created: {total_questions_created}")

        # Create or update the Science quiz
        quiz, created = Quiz.objects.get_or_create(
            title="Science Quiz - Primary 6",
            curriculum=ghana_curriculum,
            class_level=primary6,
            subject=science_subject,
            defaults={
                'description': 'Test your knowledge of Science concepts for Primary 6 level',
                'quiz_type': 'general',
                'question_count': total_questions_created,
                'per_question_time': 50,  # 50 seconds per question for Primary 6 science
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
    print("Adding comprehensive Science questions for Primary 6...")
    success = create_science_questions()

    if success:
        print("\nScience questions added successfully!")
    else:
        print("\nFailed to add Science questions.")
