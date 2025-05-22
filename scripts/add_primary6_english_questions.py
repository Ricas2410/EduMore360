#!/usr/bin/env python
"""
Script to add comprehensive English questions for Primary 6 Ghana Curriculum.
Based on the Ghana Education Service (GES) English curriculum for Primary 6.
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


def get_english_questions_data():
    """Return comprehensive English questions for Primary 6 based on GES curriculum."""
    return {
        'Grammar': [
            {
                'text': 'Which of the following is a proper noun?',
                'choices': [
                    {'text': 'boy', 'is_correct': False},
                    {'text': 'happiness', 'is_correct': False},
                    {'text': 'Accra', 'is_correct': True},
                    {'text': 'book', 'is_correct': False}
                ],
                'explanation': 'Proper nouns name specific people, places, or things and are always capitalized. "Accra" is a proper noun because it names a specific city in Ghana.'
            },
            {
                'text': 'What type of noun is "children"?',
                'choices': [
                    {'text': 'Singular noun', 'is_correct': False},
                    {'text': 'Plural noun', 'is_correct': True},
                    {'text': 'Proper noun', 'is_correct': False},
                    {'text': 'Abstract noun', 'is_correct': False}
                ],
                'explanation': 'Children is a plural noun because it refers to more than one child. The singular form is "child" and the plural form is "children".'
            },
            {
                'text': 'Choose the correct verb form: "She _____ to school every day."',
                'choices': [
                    {'text': 'go', 'is_correct': False},
                    {'text': 'goes', 'is_correct': True},
                    {'text': 'going', 'is_correct': False},
                    {'text': 'gone', 'is_correct': False}
                ],
                'explanation': 'With singular subjects like "she", we use "goes" in the present tense. The verb must agree with the subject in number and person.'
            },
            {
                'text': 'What is the past tense of "write"?',
                'choices': [
                    {'text': 'writed', 'is_correct': False},
                    {'text': 'wrote', 'is_correct': True},
                    {'text': 'writing', 'is_correct': False},
                    {'text': 'writes', 'is_correct': False}
                ],
                'explanation': 'The past tense of "write" is "wrote". This is an irregular verb, so it doesn\'t follow the regular pattern of adding "-ed".'
            },
            {
                'text': 'Which sentence uses the correct punctuation?',
                'choices': [
                    {'text': 'What is your name', 'is_correct': False},
                    {'text': 'What is your name?', 'is_correct': True},
                    {'text': 'What is your name.', 'is_correct': False},
                    {'text': 'What is your name!', 'is_correct': False}
                ],
                'explanation': 'Questions should end with a question mark (?). "What is your name?" is asking for information, so it needs a question mark.'
            },
            {
                'text': 'Choose the correct adjective: "The elephant is _____ than the mouse."',
                'choices': [
                    {'text': 'big', 'is_correct': False},
                    {'text': 'bigger', 'is_correct': True},
                    {'text': 'biggest', 'is_correct': False},
                    {'text': 'more big', 'is_correct': False}
                ],
                'explanation': 'When comparing two things, we use the comparative form. "Bigger" is the comparative form of "big" used to compare the elephant and the mouse.'
            },
            {
                'text': 'What is the plural of "child"?',
                'choices': [
                    {'text': 'childs', 'is_correct': False},
                    {'text': 'childes', 'is_correct': False},
                    {'text': 'children', 'is_correct': True},
                    {'text': 'child', 'is_correct': False}
                ],
                'explanation': 'The plural of "child" is "children". This is an irregular plural that doesn\'t follow the usual pattern of adding "-s" or "-es".'
            },
            {
                'text': 'Which word is an adverb in this sentence: "She runs quickly"?',
                'choices': [
                    {'text': 'She', 'is_correct': False},
                    {'text': 'runs', 'is_correct': False},
                    {'text': 'quickly', 'is_correct': True},
                    {'text': 'None of the above', 'is_correct': False}
                ],
                'explanation': 'Quickly is an adverb because it describes how she runs. Adverbs often end in "-ly" and describe verbs, adjectives, or other adverbs.'
            }
        ],

        'Reading and Comprehension': [
            {
                'text': 'What is the main purpose of reading comprehension?',
                'choices': [
                    {'text': 'To read as fast as possible', 'is_correct': False},
                    {'text': 'To understand what you read', 'is_correct': True},
                    {'text': 'To memorize every word', 'is_correct': False},
                    {'text': 'To read aloud', 'is_correct': False}
                ],
                'explanation': 'Reading comprehension means understanding what you read. It\'s not just about reading words, but understanding the meaning, ideas, and information in the text.'
            },
            {
                'text': 'When you don\'t understand a word while reading, what should you do first?',
                'choices': [
                    {'text': 'Skip it and continue reading', 'is_correct': False},
                    {'text': 'Try to guess its meaning from the context', 'is_correct': True},
                    {'text': 'Stop reading immediately', 'is_correct': False},
                    {'text': 'Ask someone else', 'is_correct': False}
                ],
                'explanation': 'When you encounter an unknown word, first try to guess its meaning from the context (the words and sentences around it). This helps you understand without stopping your reading flow.'
            },
            {
                'text': 'What is a story\'s main idea?',
                'choices': [
                    {'text': 'The first sentence of the story', 'is_correct': False},
                    {'text': 'The most important point or message of the story', 'is_correct': True},
                    {'text': 'The longest paragraph', 'is_correct': False},
                    {'text': 'The last sentence', 'is_correct': False}
                ],
                'explanation': 'The main idea is the most important point or central message that the author wants to communicate. It\'s what the whole story is really about.'
            },
            {
                'text': 'What are supporting details in a story?',
                'choices': [
                    {'text': 'Information that helps explain the main idea', 'is_correct': True},
                    {'text': 'The title of the story', 'is_correct': False},
                    {'text': 'The author\'s name', 'is_correct': False},
                    {'text': 'The page numbers', 'is_correct': False}
                ],
                'explanation': 'Supporting details are facts, examples, or information that help explain, prove, or give more information about the main idea of the story.'
            },
            {
                'text': 'What should you do before reading a new story?',
                'choices': [
                    {'text': 'Read the last page first', 'is_correct': False},
                    {'text': 'Look at the title and pictures to predict what it\'s about', 'is_correct': True},
                    {'text': 'Count the number of pages', 'is_correct': False},
                    {'text': 'Read it as fast as possible', 'is_correct': False}
                ],
                'explanation': 'Before reading, look at the title, pictures, and headings to predict what the story might be about. This helps prepare your mind and makes reading easier to understand.'
            },
            {
                'text': 'What is the setting of a story?',
                'choices': [
                    {'text': 'The main character', 'is_correct': False},
                    {'text': 'Where and when the story takes place', 'is_correct': True},
                    {'text': 'The problem in the story', 'is_correct': False},
                    {'text': 'The ending of the story', 'is_correct': False}
                ],
                'explanation': 'The setting is where and when the story takes place. It includes the location (like a school, forest, or city) and the time (like morning, long ago, or in the future).'
            }
        ],

        'Vocabulary Development': [
            {
                'text': 'What does the word "enormous" mean?',
                'choices': [
                    {'text': 'Very small', 'is_correct': False},
                    {'text': 'Very large', 'is_correct': True},
                    {'text': 'Very fast', 'is_correct': False},
                    {'text': 'Very slow', 'is_correct': False}
                ],
                'explanation': 'Enormous means very large or huge. For example, "The elephant is enormous" means the elephant is very big.'
            },
            {
                'text': 'Which word means the opposite of "happy"?',
                'choices': [
                    {'text': 'Joyful', 'is_correct': False},
                    {'text': 'Excited', 'is_correct': False},
                    {'text': 'Sad', 'is_correct': True},
                    {'text': 'Cheerful', 'is_correct': False}
                ],
                'explanation': 'Sad is the opposite (antonym) of happy. When someone is not happy, they are sad. Joyful, excited, and cheerful are similar to happy.'
            },
            {
                'text': 'What does "cautious" mean?',
                'choices': [
                    {'text': 'Being very careful', 'is_correct': True},
                    {'text': 'Being very fast', 'is_correct': False},
                    {'text': 'Being very loud', 'is_correct': False},
                    {'text': 'Being very tall', 'is_correct': False}
                ],
                'explanation': 'Cautious means being very careful and thinking before you act. A cautious person looks both ways before crossing the street.'
            },
            {
                'text': 'Which word is a synonym for "intelligent"?',
                'choices': [
                    {'text': 'Stupid', 'is_correct': False},
                    {'text': 'Smart', 'is_correct': True},
                    {'text': 'Lazy', 'is_correct': False},
                    {'text': 'Slow', 'is_correct': False}
                ],
                'explanation': 'Smart is a synonym (word with similar meaning) for intelligent. Both words mean having good thinking ability and being clever.'
            },
            {
                'text': 'What does "ancient" mean?',
                'choices': [
                    {'text': 'Very new', 'is_correct': False},
                    {'text': 'Very old', 'is_correct': True},
                    {'text': 'Very small', 'is_correct': False},
                    {'text': 'Very colorful', 'is_correct': False}
                ],
                'explanation': 'Ancient means very old, from a long time ago. Ancient buildings, like pyramids, were built thousands of years ago.'
            }
        ],

        'Composition Writing': [
            {
                'text': 'What should you do before you start writing a composition?',
                'choices': [
                    {'text': 'Start writing immediately', 'is_correct': False},
                    {'text': 'Plan what you want to write about', 'is_correct': True},
                    {'text': 'Count the pages', 'is_correct': False},
                    {'text': 'Write the conclusion first', 'is_correct': False}
                ],
                'explanation': 'Before writing, you should plan what you want to write about. Think about your main idea, what points you want to make, and how you will organize your thoughts.'
            },
            {
                'text': 'What is the purpose of the introduction in a composition?',
                'choices': [
                    {'text': 'To end the composition', 'is_correct': False},
                    {'text': 'To introduce the topic and grab the reader\'s attention', 'is_correct': True},
                    {'text': 'To list all the details', 'is_correct': False},
                    {'text': 'To repeat the conclusion', 'is_correct': False}
                ],
                'explanation': 'The introduction should introduce your topic and grab the reader\'s attention. It tells the reader what your composition will be about and makes them want to keep reading.'
            },
            {
                'text': 'What makes a good paragraph?',
                'choices': [
                    {'text': 'Having only one sentence', 'is_correct': False},
                    {'text': 'Having one main idea with supporting details', 'is_correct': True},
                    {'text': 'Having many different topics', 'is_correct': False},
                    {'text': 'Having no punctuation', 'is_correct': False}
                ],
                'explanation': 'A good paragraph has one main idea and several sentences that give supporting details about that main idea. All sentences in the paragraph should relate to the main idea.'
            },
            {
                'text': 'What should you include in a conclusion?',
                'choices': [
                    {'text': 'New information not mentioned before', 'is_correct': False},
                    {'text': 'A summary of your main points', 'is_correct': True},
                    {'text': 'Questions for the reader', 'is_correct': False},
                    {'text': 'Your personal address', 'is_correct': False}
                ],
                'explanation': 'A conclusion should summarize your main points and bring your composition to a satisfying end. It reminds the reader of what you have written about.'
            },
            {
                'text': 'When writing a story, what should you include?',
                'choices': [
                    {'text': 'Only dialogue', 'is_correct': False},
                    {'text': 'Characters, setting, and a plot', 'is_correct': True},
                    {'text': 'Only descriptions', 'is_correct': False},
                    {'text': 'Only action', 'is_correct': False}
                ],
                'explanation': 'A good story should have characters (people in the story), setting (where and when it happens), and a plot (what happens in the story).'
            }
        ],

        'Listening and Speaking': [
            {
                'text': 'What is good listening?',
                'choices': [
                    {'text': 'Talking while others speak', 'is_correct': False},
                    {'text': 'Paying attention and understanding what is said', 'is_correct': True},
                    {'text': 'Looking away from the speaker', 'is_correct': False},
                    {'text': 'Thinking about other things', 'is_correct': False}
                ],
                'explanation': 'Good listening means paying attention to the speaker, trying to understand what they are saying, and showing that you are listening through your body language and responses.'
            },
            {
                'text': 'When speaking to others, you should:',
                'choices': [
                    {'text': 'Speak very quietly so no one can hear', 'is_correct': False},
                    {'text': 'Speak clearly and at an appropriate volume', 'is_correct': True},
                    {'text': 'Speak very fast', 'is_correct': False},
                    {'text': 'Look at the ground while speaking', 'is_correct': False}
                ],
                'explanation': 'When speaking, you should speak clearly so people can understand you, at a volume that is appropriate for the situation, and look at your audience to connect with them.'
            },
            {
                'text': 'What should you do when you don\'t understand something someone said?',
                'choices': [
                    {'text': 'Pretend you understand', 'is_correct': False},
                    {'text': 'Ask politely for clarification', 'is_correct': True},
                    {'text': 'Walk away', 'is_correct': False},
                    {'text': 'Change the topic', 'is_correct': False}
                ],
                'explanation': 'If you don\'t understand something, it\'s perfectly okay to ask politely for clarification. You can say "Could you please explain that again?" or "I don\'t understand, could you help me?"'
            },
            {
                'text': 'What is the purpose of asking questions during a conversation?',
                'choices': [
                    {'text': 'To confuse the speaker', 'is_correct': False},
                    {'text': 'To show interest and get more information', 'is_correct': True},
                    {'text': 'To interrupt the speaker', 'is_correct': False},
                    {'text': 'To change the topic', 'is_correct': False}
                ],
                'explanation': 'Asking questions shows that you are interested in what the speaker is saying and helps you get more information or clarification about the topic.'
            },
            {
                'text': 'When giving a presentation, what should you do?',
                'choices': [
                    {'text': 'Read directly from your notes without looking up', 'is_correct': False},
                    {'text': 'Make eye contact with your audience and speak confidently', 'is_correct': True},
                    {'text': 'Speak as fast as possible to finish quickly', 'is_correct': False},
                    {'text': 'Turn your back to the audience', 'is_correct': False}
                ],
                'explanation': 'When presenting, make eye contact with your audience, speak confidently and clearly, and engage with your listeners. This helps them understand and stay interested in your presentation.'
            }
        ]
    }


def create_english_questions():
    """Create English questions for Primary 6."""
    try:
        # Get the Ghana curriculum and Primary 6 class level
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        english_subject = Subject.objects.get(name='English', class_level=primary6)

        print(f"Found English subject: {english_subject.name} - {english_subject.class_level.name}")

        questions_data = get_english_questions_data()
        total_questions_created = 0

        for topic_name, topic_questions in questions_data.items():
            try:
                topic = Topic.objects.get(name=topic_name, subject=english_subject)
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
                        subject=english_subject,
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

        print(f"\nTotal English questions created: {total_questions_created}")

        # Create or update the English quiz
        quiz, created = Quiz.objects.get_or_create(
            title="English Quiz - Primary 6",
            curriculum=ghana_curriculum,
            class_level=primary6,
            subject=english_subject,
            defaults={
                'description': 'Test your knowledge of English language skills for Primary 6 level',
                'quiz_type': 'general',
                'question_count': total_questions_created,
                'per_question_time': 45,  # 45 seconds per question for Primary 6
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
    print("Adding comprehensive English questions for Primary 6...")
    success = create_english_questions()

    if success:
        print("\nEnglish questions added successfully!")
    else:
        print("\nFailed to add English questions.")
