#!/usr/bin/env python
"""
Script to add comprehensive Social Studies questions for Primary 6 Ghana Curriculum.
Based on the Ghana Education Service (GES) Social Studies curriculum for Primary 6.
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


def get_social_studies_questions_data():
    """Return comprehensive Social Studies questions for Primary 6 based on GES curriculum."""
    return {
        'Our Nation Ghana': [
            {
                'text': 'Who was the first president of Ghana?',
                'choices': [
                    {'text': 'Jerry John Rawlings', 'is_correct': False},
                    {'text': 'Kwame Nkrumah', 'is_correct': True},
                    {'text': 'John Agyekum Kufuor', 'is_correct': False},
                    {'text': 'John Dramani Mahama', 'is_correct': False}
                ],
                'explanation': 'Dr. Kwame Nkrumah was the first president of Ghana after independence in 1957. He led the country to independence from British colonial rule and is known as the founder of modern Ghana.'
            },
            {
                'text': 'When did Ghana gain independence?',
                'choices': [
                    {'text': 'March 6, 1957', 'is_correct': True},
                    {'text': 'March 6, 1960', 'is_correct': False},
                    {'text': 'July 1, 1960', 'is_correct': False},
                    {'text': 'December 31, 1981', 'is_correct': False}
                ],
                'explanation': 'Ghana gained independence from Britain on March 6, 1957. This date is celebrated every year as Independence Day, a national holiday in Ghana.'
            },
            {
                'text': 'What is the capital city of Ghana?',
                'choices': [
                    {'text': 'Kumasi', 'is_correct': False},
                    {'text': 'Accra', 'is_correct': True},
                    {'text': 'Tamale', 'is_correct': False},
                    {'text': 'Cape Coast', 'is_correct': False}
                ],
                'explanation': 'Accra is the capital and largest city of Ghana. It is located on the Atlantic coast and serves as the political, economic, and cultural center of the country.'
            },
            {
                'text': 'Which colors are on the Ghana flag?',
                'choices': [
                    {'text': 'Red, gold, green with a black star', 'is_correct': True},
                    {'text': 'Blue, white, red', 'is_correct': False},
                    {'text': 'Green, white, orange', 'is_correct': False},
                    {'text': 'Yellow, blue, black', 'is_correct': False}
                ],
                'explanation': 'The Ghana flag has three horizontal stripes: red (top), gold/yellow (middle), and green (bottom), with a black five-pointed star in the center. Each color has special meaning for Ghana.'
            },
            {
                'text': 'What is the national language of Ghana?',
                'choices': [
                    {'text': 'Twi', 'is_correct': False},
                    {'text': 'Ga', 'is_correct': False},
                    {'text': 'English', 'is_correct': True},
                    {'text': 'Ewe', 'is_correct': False}
                ],
                'explanation': 'English is the official language of Ghana, used in government, education, and business. However, Ghana has many local languages like Twi, Ga, Ewe, and others that people speak at home.'
            },
            {
                'text': 'How many regions does Ghana have?',
                'choices': [
                    {'text': '10', 'is_correct': False},
                    {'text': '16', 'is_correct': True},
                    {'text': '12', 'is_correct': False},
                    {'text': '8', 'is_correct': False}
                ],
                'explanation': 'Ghana currently has 16 regions. The country was originally divided into 10 regions, but 6 new regions were created in 2018 to bring governance closer to the people.'
            }
        ],

        'Map Reading': [
            {
                'text': 'What does a map legend or key show?',
                'choices': [
                    {'text': 'The size of the map', 'is_correct': False},
                    {'text': 'The meaning of symbols used on the map', 'is_correct': True},
                    {'text': 'The date the map was made', 'is_correct': False},
                    {'text': 'The name of the mapmaker', 'is_correct': False}
                ],
                'explanation': 'A map legend or key explains what the different symbols, colors, and lines on a map represent. For example, it might show that a blue line represents a river or a green area represents a forest.'
            },
            {
                'text': 'Which direction is at the top of most maps?',
                'choices': [
                    {'text': 'South', 'is_correct': False},
                    {'text': 'East', 'is_correct': False},
                    {'text': 'North', 'is_correct': True},
                    {'text': 'West', 'is_correct': False}
                ],
                'explanation': 'North is usually at the top of most maps. Maps often have a compass rose or north arrow to show which direction is north.'
            },
            {
                'text': 'What are the four main directions called?',
                'choices': [
                    {'text': 'Cardinal directions', 'is_correct': True},
                    {'text': 'Map directions', 'is_correct': False},
                    {'text': 'Compass directions', 'is_correct': False},
                    {'text': 'Basic directions', 'is_correct': False}
                ],
                'explanation': 'The four main directions (North, South, East, West) are called cardinal directions. These are the most important directions for navigation and map reading.'
            },
            {
                'text': 'What does scale on a map tell us?',
                'choices': [
                    {'text': 'How old the map is', 'is_correct': False},
                    {'text': 'How big or small things are compared to real life', 'is_correct': True},
                    {'text': 'What colors to use', 'is_correct': False},
                    {'text': 'Who made the map', 'is_correct': False}
                ],
                'explanation': 'Map scale shows the relationship between distances on the map and real distances on the ground. For example, 1 cm on the map might represent 1 km in real life.'
            },
            {
                'text': 'If you are facing north, which direction is to your right?',
                'choices': [
                    {'text': 'South', 'is_correct': False},
                    {'text': 'West', 'is_correct': False},
                    {'text': 'East', 'is_correct': True},
                    {'text': 'North', 'is_correct': False}
                ],
                'explanation': 'If you are facing north, east is to your right, west is to your left, and south is behind you. This is a basic rule for understanding directions.'
            }
        ],

        'Governance': [
            {
                'text': 'What is the name of Ghana\'s parliament?',
                'choices': [
                    {'text': 'House of Commons', 'is_correct': False},
                    {'text': 'National Assembly', 'is_correct': False},
                    {'text': 'Parliament of Ghana', 'is_correct': True},
                    {'text': 'Congress', 'is_correct': False}
                ],
                'explanation': 'Ghana\'s legislative body is officially called the Parliament of Ghana. It is located in Accra and is responsible for making laws for the country.'
            },
            {
                'text': 'How often are presidential elections held in Ghana?',
                'choices': [
                    {'text': 'Every 3 years', 'is_correct': False},
                    {'text': 'Every 4 years', 'is_correct': True},
                    {'text': 'Every 5 years', 'is_correct': False},
                    {'text': 'Every 6 years', 'is_correct': False}
                ],
                'explanation': 'Presidential elections in Ghana are held every 4 years. The president can serve a maximum of two terms, which means 8 years in total.'
            },
            {
                'text': 'What is the role of a Member of Parliament (MP)?',
                'choices': [
                    {'text': 'To represent the people in their constituency', 'is_correct': True},
                    {'text': 'To be the president', 'is_correct': False},
                    {'text': 'To be a judge', 'is_correct': False},
                    {'text': 'To be a teacher', 'is_correct': False}
                ],
                'explanation': 'A Member of Parliament (MP) represents the people in their constituency (area) in parliament. They speak for their people, make laws, and help solve problems in their communities.'
            },
            {
                'text': 'What are the three branches of government?',
                'choices': [
                    {'text': 'Executive, Legislative, and Judicial', 'is_correct': True},
                    {'text': 'President, Parliament, and Police', 'is_correct': False},
                    {'text': 'National, Regional, and Local', 'is_correct': False},
                    {'text': 'Government, Opposition, and Citizens', 'is_correct': False}
                ],
                'explanation': 'The three branches of government are: Executive (led by the President), Legislative (Parliament that makes laws), and Judicial (courts that interpret laws). This separation helps prevent abuse of power.'
            },
            {
                'text': 'What is a citizen\'s responsibility in a democracy?',
                'choices': [
                    {'text': 'To vote and participate in governance', 'is_correct': True},
                    {'text': 'To only pay taxes', 'is_correct': False},
                    {'text': 'To avoid politics completely', 'is_correct': False},
                    {'text': 'To only obey laws', 'is_correct': False}
                ],
                'explanation': 'In a democracy, citizens have the responsibility to vote, participate in governance, obey laws, pay taxes, and hold leaders accountable. Voting is especially important for choosing good leaders.'
            }
        ],

        'Environment and Resources': [
            {
                'text': 'Which of these is a renewable natural resource?',
                'choices': [
                    {'text': 'Coal', 'is_correct': False},
                    {'text': 'Oil', 'is_correct': False},
                    {'text': 'Solar energy', 'is_correct': True},
                    {'text': 'Natural gas', 'is_correct': False}
                ],
                'explanation': 'Solar energy is renewable because the sun will continue to shine for billions of years. Coal, oil, and natural gas are non-renewable because once we use them up, they cannot be replaced quickly.'
            },
            {
                'text': 'What is deforestation?',
                'choices': [
                    {'text': 'Planting more trees', 'is_correct': False},
                    {'text': 'Cutting down forests', 'is_correct': True},
                    {'text': 'Protecting forests', 'is_correct': False},
                    {'text': 'Studying forests', 'is_correct': False}
                ],
                'explanation': 'Deforestation means cutting down or clearing forests. This can be harmful to the environment because trees help clean the air, prevent soil erosion, and provide homes for animals.'
            },
            {
                'text': 'Why is it important to conserve water?',
                'choices': [
                    {'text': 'Water is unlimited', 'is_correct': False},
                    {'text': 'Clean water is limited and precious', 'is_correct': True},
                    {'text': 'Water is not important', 'is_correct': False},
                    {'text': 'Water conservation is not necessary', 'is_correct': False}
                ],
                'explanation': 'Clean, fresh water is limited and precious. Many people around the world don\'t have access to clean water, so we should not waste it. Conserving water helps ensure there\'s enough for everyone.'
            },
            {
                'text': 'What can we do to protect our environment?',
                'choices': [
                    {'text': 'Throw rubbish everywhere', 'is_correct': False},
                    {'text': 'Reduce, reuse, and recycle', 'is_correct': True},
                    {'text': 'Use more plastic bags', 'is_correct': False},
                    {'text': 'Waste more resources', 'is_correct': False}
                ],
                'explanation': 'We can protect our environment by following the 3 Rs: Reduce (use less), Reuse (use things again), and Recycle (turn waste into new products). This helps reduce pollution and saves resources.'
            },
            {
                'text': 'Which of these causes air pollution?',
                'choices': [
                    {'text': 'Planting trees', 'is_correct': False},
                    {'text': 'Car exhaust and factory smoke', 'is_correct': True},
                    {'text': 'Clean water', 'is_correct': False},
                    {'text': 'Solar panels', 'is_correct': False}
                ],
                'explanation': 'Car exhaust and factory smoke release harmful gases into the air, causing air pollution. This can make people sick and harm the environment. Planting trees actually helps clean the air.'
            }
        ]
    }


def create_social_studies_questions():
    """Create Social Studies questions for Primary 6."""
    try:
        # Get the Ghana curriculum and Primary 6 class level
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        social_subject = Subject.objects.get(name='Social Studies', class_level=primary6)

        print(f"Found Social Studies subject: {social_subject.name} - {social_subject.class_level.name}")

        questions_data = get_social_studies_questions_data()
        total_questions_created = 0

        for topic_name, topic_questions in questions_data.items():
            try:
                topic = Topic.objects.get(name=topic_name, subject=social_subject)
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
                        subject=social_subject,
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

        print(f"\nTotal Social Studies questions created: {total_questions_created}")

        # Create or update the Social Studies quiz
        quiz, created = Quiz.objects.get_or_create(
            title="Social Studies Quiz - Primary 6",
            curriculum=ghana_curriculum,
            class_level=primary6,
            subject=social_subject,
            defaults={
                'description': 'Test your knowledge of Social Studies concepts for Primary 6 level',
                'quiz_type': 'general',
                'question_count': total_questions_created,
                'per_question_time': 50,  # 50 seconds per question for Primary 6 social studies
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
    print("Adding comprehensive Social Studies questions for Primary 6...")
    success = create_social_studies_questions()

    if success:
        print("\nSocial Studies questions added successfully!")
    else:
        print("\nFailed to add Social Studies questions.")
