#!/usr/bin/env python
"""
Script to add comprehensive Ghanaian Festivals questions for Primary 5 and Primary 6.
Based on the Ghana Education Service (GES) curriculum and Ghanaian cultural heritage.
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


def get_festival_questions_data():
    """Return comprehensive Ghanaian Festival questions based on GES curriculum."""
    return {
        'Traditional Festivals': [
            {
                'text': 'What is the most famous festival celebrated by the Ashanti people?',
                'choices': [
                    {'text': 'Homowo', 'is_correct': False},
                    {'text': 'Akwasidae', 'is_correct': True},
                    {'text': 'Damba', 'is_correct': False},
                    {'text': 'Bakatue', 'is_correct': False}
                ],
                'explanation': 'Akwasidae is the most famous festival of the Ashanti people. It is celebrated every six weeks to honor the ancestors and the Golden Stool, which is the symbol of Ashanti unity and power.'
            },
            {
                'text': 'Which festival is celebrated by the Ga people to remember their ancestors?',
                'choices': [
                    {'text': 'Homowo', 'is_correct': True},
                    {'text': 'Akwasidae', 'is_correct': False},
                    {'text': 'Yam Festival', 'is_correct': False},
                    {'text': 'Damba', 'is_correct': False}
                ],
                'explanation': 'Homowo is celebrated by the Ga people of Greater Accra. The name means "hooting at hunger" and it commemorates their ancestors\' victory over famine. During the festival, they sprinkle kpokpoi (traditional food) to feed the ancestors.'
            },
            {
                'text': 'What does "Homowo" mean in English?',
                'choices': [
                    {'text': 'Harvest time', 'is_correct': False},
                    {'text': 'Hooting at hunger', 'is_correct': True},
                    {'text': 'New year celebration', 'is_correct': False},
                    {'text': 'Victory dance', 'is_correct': False}
                ],
                'explanation': 'Homowo means "hooting at hunger" in the Ga language. This festival celebrates the end of a great famine that once affected the Ga people, and they now celebrate with abundance of food.'
            },
            {
                'text': 'Which festival is celebrated by the people of the Northern Region to mark the end of Ramadan?',
                'choices': [
                    {'text': 'Damba', 'is_correct': True},
                    {'text': 'Homowo', 'is_correct': False},
                    {'text': 'Akwasidae', 'is_correct': False},
                    {'text': 'Bakatue', 'is_correct': False}
                ],
                'explanation': 'Damba is celebrated by the people of Northern Ghana, particularly the Dagomba, Mamprusi, and Gonja people. It marks the birth of Prophet Mohammed and is celebrated with drumming, dancing, and horse riding.'
            },
            {
                'text': 'What is the Yam Festival also known as?',
                'choices': [
                    {'text': 'Homowo', 'is_correct': False},
                    {'text': 'Odwira', 'is_correct': True},
                    {'text': 'Damba', 'is_correct': False},
                    {'text': 'Bakatue', 'is_correct': False}
                ],
                'explanation': 'The Yam Festival is also known as Odwira in some parts of Ghana. It is celebrated to give thanks for the yam harvest and to purify the community. Yam is considered a sacred crop in many Ghanaian cultures.'
            },
            {
                'text': 'Which festival is celebrated by the people of Elmina to mark the beginning of the fishing season?',
                'choices': [
                    {'text': 'Bakatue', 'is_correct': True},
                    {'text': 'Homowo', 'is_correct': False},
                    {'text': 'Akwasidae', 'is_correct': False},
                    {'text': 'Damba', 'is_correct': False}
                ],
                'explanation': 'Bakatue is celebrated by the people of Elmina in the Central Region. It marks the beginning of the fishing season and is celebrated with colorful canoes, drumming, dancing, and the casting of nets into the sea.'
            },
            {
                'text': 'What is the main purpose of traditional festivals in Ghana?',
                'choices': [
                    {'text': 'To make money from tourists', 'is_correct': False},
                    {'text': 'To honor ancestors, give thanks, and unite the community', 'is_correct': True},
                    {'text': 'To compete with other regions', 'is_correct': False},
                    {'text': 'To show off traditional clothes', 'is_correct': False}
                ],
                'explanation': 'Traditional festivals in Ghana serve important purposes: honoring ancestors, giving thanks to God and nature, uniting the community, preserving culture, and passing traditions to younger generations.'
            },
            {
                'text': 'During which festival do people sprinkle kpokpoi (corn meal) to feed the ancestors?',
                'choices': [
                    {'text': 'Akwasidae', 'is_correct': False},
                    {'text': 'Homowo', 'is_correct': True},
                    {'text': 'Damba', 'is_correct': False},
                    {'text': 'Bakatue', 'is_correct': False}
                ],
                'explanation': 'During Homowo festival, the Ga people sprinkle kpokpoi (a traditional food made from corn meal) around their homes and communities to feed their ancestors and ensure their blessings.'
            }
        ],

        'Festival Activities and Customs': [
            {
                'text': 'What are the main activities during most Ghanaian festivals?',
                'choices': [
                    {'text': 'Only eating and drinking', 'is_correct': False},
                    {'text': 'Drumming, dancing, singing, and traditional ceremonies', 'is_correct': True},
                    {'text': 'Only religious prayers', 'is_correct': False},
                    {'text': 'Only modern entertainment', 'is_correct': False}
                ],
                'explanation': 'Ghanaian festivals typically include drumming, dancing, singing, traditional ceremonies, wearing of traditional clothes, sharing of food, and various cultural performances that bring the community together.'
            },
            {
                'text': 'What type of clothing do people wear during traditional festivals?',
                'choices': [
                    {'text': 'Modern Western clothes only', 'is_correct': False},
                    {'text': 'Traditional Ghanaian clothes like kente and adinkra', 'is_correct': True},
                    {'text': 'Sports uniforms', 'is_correct': False},
                    {'text': 'School uniforms', 'is_correct': False}
                ],
                'explanation': 'During traditional festivals, people wear beautiful traditional Ghanaian clothes such as kente cloth, adinkra cloth, smocks, and other colorful traditional garments that represent their cultural heritage.'
            },
            {
                'text': 'What role do chiefs play during traditional festivals?',
                'choices': [
                    {'text': 'They stay at home', 'is_correct': False},
                    {'text': 'They lead ceremonies and bless the people', 'is_correct': True},
                    {'text': 'They only watch from far away', 'is_correct': False},
                    {'text': 'They do not participate', 'is_correct': False}
                ],
                'explanation': 'Chiefs play a central role in traditional festivals. They lead important ceremonies, offer prayers and blessings, pour libation to ancestors, and serve as the link between the living and the ancestors.'
            },
            {
                'text': 'What is libation in Ghanaian festivals?',
                'choices': [
                    {'text': 'A type of dance', 'is_correct': False},
                    {'text': 'Pouring drinks to honor ancestors and gods', 'is_correct': True},
                    {'text': 'A traditional song', 'is_correct': False},
                    {'text': 'A type of food', 'is_correct': False}
                ],
                'explanation': 'Libation is the pouring of drinks (usually water, palm wine, or schnapps) on the ground while saying prayers to honor ancestors, gods, and seek their blessings and protection.'
            },
            {
                'text': 'Why do people return to their hometowns during festivals?',
                'choices': [
                    {'text': 'To avoid work', 'is_correct': False},
                    {'text': 'To reunite with family and participate in cultural traditions', 'is_correct': True},
                    {'text': 'To escape from the city', 'is_correct': False},
                    {'text': 'To avoid paying bills', 'is_correct': False}
                ],
                'explanation': 'People return to their hometowns during festivals to reunite with family, participate in cultural traditions, honor their ancestors, and strengthen their connection to their roots and community.'
            },
            {
                'text': 'What types of food are commonly shared during festivals?',
                'choices': [
                    {'text': 'Only foreign foods', 'is_correct': False},
                    {'text': 'Traditional Ghanaian foods like fufu, kenkey, and palm nut soup', 'is_correct': True},
                    {'text': 'Only fast food', 'is_correct': False},
                    {'text': 'Only fruits', 'is_correct': False}
                ],
                'explanation': 'During festivals, people share traditional Ghanaian foods such as fufu, kenkey, banku, palm nut soup, groundnut soup, jollof rice, and other local delicacies that represent their cultural heritage.'
            }
        ],

        'Cultural Significance': [
            {
                'text': 'Why are festivals important for preserving Ghanaian culture?',
                'choices': [
                    {'text': 'They are not important', 'is_correct': False},
                    {'text': 'They help pass traditions from old to young generations', 'is_correct': True},
                    {'text': 'They only entertain people', 'is_correct': False},
                    {'text': 'They waste time and money', 'is_correct': False}
                ],
                'explanation': 'Festivals are crucial for preserving Ghanaian culture because they help pass traditions, values, history, and customs from older generations to younger ones, ensuring cultural continuity.'
            },
            {
                'text': 'What can young people learn from participating in traditional festivals?',
                'choices': [
                    {'text': 'Nothing important', 'is_correct': False},
                    {'text': 'Their history, values, and cultural identity', 'is_correct': True},
                    {'text': 'Only how to dance', 'is_correct': False},
                    {'text': 'Only how to eat traditional food', 'is_correct': False}
                ],
                'explanation': 'Young people learn about their history, cultural values, traditional practices, respect for elders and ancestors, community unity, and develop a strong sense of cultural identity through festival participation.'
            },
            {
                'text': 'How do festivals promote unity in Ghanaian communities?',
                'choices': [
                    {'text': 'They divide people', 'is_correct': False},
                    {'text': 'They bring people together regardless of their differences', 'is_correct': True},
                    {'text': 'They only unite rich people', 'is_correct': False},
                    {'text': 'They create conflicts', 'is_correct': False}
                ],
                'explanation': 'Festivals promote unity by bringing people together regardless of their social status, age, or differences. Everyone participates in shared activities, celebrates together, and strengthens community bonds.'
            },
            {
                'text': 'What role do festivals play in tourism in Ghana?',
                'choices': [
                    {'text': 'They discourage tourists', 'is_correct': False},
                    {'text': 'They attract visitors who want to experience Ghanaian culture', 'is_correct': True},
                    {'text': 'They have no effect on tourism', 'is_correct': False},
                    {'text': 'They only attract local people', 'is_correct': False}
                ],
                'explanation': 'Festivals attract tourists from around the world who want to experience authentic Ghanaian culture, contributing to the economy and promoting Ghana\'s rich cultural heritage globally.'
            },
            {
                'text': 'How should we respect traditional festivals as students?',
                'choices': [
                    {'text': 'Ignore them completely', 'is_correct': False},
                    {'text': 'Learn about them, participate respectfully, and appreciate their value', 'is_correct': True},
                    {'text': 'Make fun of the traditions', 'is_correct': False},
                    {'text': 'Only attend for the food', 'is_correct': False}
                ],
                'explanation': 'As students, we should learn about festivals, participate respectfully, appreciate their cultural value, ask questions to understand their meaning, and help preserve these important traditions for future generations.'
            }
        ]
    }


def create_festival_questions():
    """Create Festival questions for both Primary 5 and Primary 6."""
    try:
        # Get the Ghana curriculum and class levels
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary5 = ClassLevel.objects.get(name='Primary 5', curriculum=ghana_curriculum)
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)

        # Get Social Studies subjects for both classes
        social_studies_p5 = Subject.objects.get(name='Social Studies', class_level=primary5)
        social_studies_p6 = Subject.objects.get(name='Social Studies', class_level=primary6)

        print(f"Found Social Studies subjects:")
        print(f"- {social_studies_p5.name} - {social_studies_p5.class_level.name}")
        print(f"- {social_studies_p6.name} - {social_studies_p6.class_level.name}")

        # Create or get the "Cultural Identity" topic for both classes
        cultural_topic_p5, created = Topic.objects.get_or_create(
            name='Cultural Identity',
            subject=social_studies_p5,
            defaults={
                'description': 'Learning about Ghanaian festivals, traditions, and cultural heritage'
            }
        )

        cultural_topic_p6, created = Topic.objects.get_or_create(
            name='Cultural Identity',
            subject=social_studies_p6,
            defaults={
                'description': 'Learning about Ghanaian festivals, traditions, and cultural heritage'
            }
        )

        print(f"\nCultural Identity topics:")
        print(f"- Primary 5: {'Created' if created else 'Found existing'}")
        print(f"- Primary 6: {'Created' if created else 'Found existing'}")

        questions_data = get_festival_questions_data()
        total_questions_created = 0

        # Create questions for both Primary 5 and Primary 6
        for class_level, social_subject, cultural_topic in [
            (primary5, social_studies_p5, cultural_topic_p5),
            (primary6, social_studies_p6, cultural_topic_p6)
        ]:
            print(f"\nProcessing {class_level.name}...")

            # Remove existing festival questions to avoid duplicates
            existing_questions = Question.objects.filter(topic=cultural_topic)
            if existing_questions.exists():
                print(f"  Removing {existing_questions.count()} existing festival questions...")
                existing_questions.delete()

            class_questions_created = 0

            for topic_name, topic_questions in questions_data.items():
                print(f"  Adding {topic_name} questions...")

                for question_data in topic_questions:
                    # Create the question
                    question = Question.objects.create(
                        text=question_data['text'],
                        question_type='multiple_choice',
                        difficulty='easy',  # Primary level
                        explanation=question_data['explanation'],
                        curriculum=ghana_curriculum,
                        class_level=class_level,
                        subject=social_subject,
                        topic=cultural_topic,
                        is_active=True
                    )

                    # Create the choices
                    for choice_data in question_data['choices']:
                        QuestionChoice.objects.create(
                            question=question,
                            text=choice_data['text'],
                            is_correct=choice_data['is_correct']
                        )

                    class_questions_created += 1

            print(f"  Created {class_questions_created} festival questions for {class_level.name}")
            total_questions_created += class_questions_created

            # Create or update the Cultural Heritage quiz
            quiz, created = Quiz.objects.get_or_create(
                title=f"Ghanaian Festivals Quiz - {class_level.name}",
                curriculum=ghana_curriculum,
                class_level=class_level,
                subject=social_subject,
                defaults={
                    'description': f'Test your knowledge of Ghanaian festivals and cultural heritage for {class_level.name} level',
                    'quiz_type': 'general',
                    'question_count': class_questions_created,
                    'per_question_time': 45,  # 45 seconds per question
                    'randomize_questions': True,
                    'randomize_choices': True,
                    'show_immediate_feedback': True,
                    'passing_score': 60,  # 60% passing score
                    'is_active': True,
                    'is_featured': True
                }
            )

            if created:
                print(f"  Created quiz: {quiz.title}")
            else:
                # Update question count
                quiz.question_count = class_questions_created
                quiz.save()
                print(f"  Updated quiz: {quiz.title}")

        print(f"\nTotal festival questions created: {total_questions_created}")
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("Adding comprehensive Ghanaian Festival questions for Primary 5 and Primary 6...")
    success = create_festival_questions()

    if success:
        print("\nGhanaian Festival questions added successfully!")
    else:
        print("\nFailed to add Ghanaian Festival questions.")
