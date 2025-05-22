#!/usr/bin/env python
"""
Script to add comprehensive ICT questions for Primary 6 Ghana Curriculum.
Based on the Ghana Education Service (GES) ICT curriculum for Primary 6.
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


def get_ict_questions_data():
    """Return comprehensive ICT questions for Primary 6."""
    return {
        'Introduction to Computers': [
            {
                'text': 'What is a computer?',
                'choices': [
                    {'text': 'A machine that can store, process and retrieve information', 'is_correct': True},
                    {'text': 'A television set', 'is_correct': False},
                    {'text': 'A radio', 'is_correct': False},
                    {'text': 'A calculator only', 'is_correct': False}
                ],
                'explanation': 'A computer is an electronic machine that can store, process, and retrieve information. It can perform calculations, store data, and help us with many tasks.'
            },
            {
                'text': 'Which of these is an input device?',
                'choices': [
                    {'text': 'Monitor', 'is_correct': False},
                    {'text': 'Printer', 'is_correct': False},
                    {'text': 'Keyboard', 'is_correct': True},
                    {'text': 'Speaker', 'is_correct': False}
                ],
                'explanation': 'A keyboard is an input device because it allows us to enter data and commands into the computer. Input devices help us communicate with the computer.'
            },
            {
                'text': 'What is the brain of the computer called?',
                'choices': [
                    {'text': 'RAM', 'is_correct': False},
                    {'text': 'CPU', 'is_correct': True},
                    {'text': 'Hard Drive', 'is_correct': False},
                    {'text': 'Monitor', 'is_correct': False}
                ],
                'explanation': 'The CPU (Central Processing Unit) is called the brain of the computer because it processes all instructions and performs calculations, just like our brain controls our body.'
            },
            {
                'text': 'Which of these is an output device?',
                'choices': [
                    {'text': 'Mouse', 'is_correct': False},
                    {'text': 'Keyboard', 'is_correct': False},
                    {'text': 'Monitor', 'is_correct': True},
                    {'text': 'Microphone', 'is_correct': False}
                ],
                'explanation': 'A monitor is an output device because it displays information from the computer to us. Output devices show us the results of what the computer has processed.'
            },
            {
                'text': 'What does RAM stand for?',
                'choices': [
                    {'text': 'Random Access Memory', 'is_correct': True},
                    {'text': 'Read And Modify', 'is_correct': False},
                    {'text': 'Rapid Access Mode', 'is_correct': False},
                    {'text': 'Really Amazing Machine', 'is_correct': False}
                ],
                'explanation': 'RAM stands for Random Access Memory. It is the computer\'s temporary memory where it stores information that it is currently working with.'
            },
            {
                'text': 'Which part of the computer stores information permanently?',
                'choices': [
                    {'text': 'RAM', 'is_correct': False},
                    {'text': 'CPU', 'is_correct': False},
                    {'text': 'Hard Drive', 'is_correct': True},
                    {'text': 'Monitor', 'is_correct': False}
                ],
                'explanation': 'The hard drive (or hard disk) stores information permanently. Even when the computer is turned off, the information on the hard drive remains saved.'
            },
            {
                'text': 'What is software?',
                'choices': [
                    {'text': 'The physical parts of a computer', 'is_correct': False},
                    {'text': 'Programs and applications that run on a computer', 'is_correct': True},
                    {'text': 'The computer screen', 'is_correct': False},
                    {'text': 'The computer keyboard', 'is_correct': False}
                ],
                'explanation': 'Software refers to programs and applications that run on a computer. Examples include games, word processors, and web browsers. Software tells the computer what to do.'
            },
            {
                'text': 'What is hardware?',
                'choices': [
                    {'text': 'Computer programs', 'is_correct': False},
                    {'text': 'The physical parts of a computer you can touch', 'is_correct': True},
                    {'text': 'Internet websites', 'is_correct': False},
                    {'text': 'Computer games', 'is_correct': False}
                ],
                'explanation': 'Hardware refers to the physical parts of a computer that you can touch, such as the monitor, keyboard, mouse, CPU, and hard drive.'
            }
        ],

        'Word Processing': [
            {
                'text': 'What is word processing?',
                'choices': [
                    {'text': 'Playing computer games', 'is_correct': False},
                    {'text': 'Creating and editing text documents', 'is_correct': True},
                    {'text': 'Drawing pictures', 'is_correct': False},
                    {'text': 'Listening to music', 'is_correct': False}
                ],
                'explanation': 'Word processing is the activity of creating, editing, and formatting text documents using a computer. It helps us write letters, reports, and other documents.'
            },
            {
                'text': 'Which of these is a word processing software?',
                'choices': [
                    {'text': 'Microsoft Word', 'is_correct': True},
                    {'text': 'Calculator', 'is_correct': False},
                    {'text': 'Paint', 'is_correct': False},
                    {'text': 'Media Player', 'is_correct': False}
                ],
                'explanation': 'Microsoft Word is a popular word processing software that allows us to create, edit, and format text documents with features like fonts, colors, and images.'
            },
            {
                'text': 'What does "Save" mean in word processing?',
                'choices': [
                    {'text': 'Delete the document', 'is_correct': False},
                    {'text': 'Store the document on the computer', 'is_correct': True},
                    {'text': 'Print the document', 'is_correct': False},
                    {'text': 'Close the program', 'is_correct': False}
                ],
                'explanation': 'Save means to store your document on the computer so you can open it again later. It\'s important to save your work regularly to avoid losing it.'
            },
            {
                'text': 'What is the purpose of spell check in word processing?',
                'choices': [
                    {'text': 'To change font colors', 'is_correct': False},
                    {'text': 'To find and correct spelling mistakes', 'is_correct': True},
                    {'text': 'To add pictures', 'is_correct': False},
                    {'text': 'To print documents', 'is_correct': False}
                ],
                'explanation': 'Spell check is a feature that helps find and correct spelling mistakes in your document. It usually underlines misspelled words in red.'
            },
            {
                'text': 'What does "Copy and Paste" allow you to do?',
                'choices': [
                    {'text': 'Delete text', 'is_correct': False},
                    {'text': 'Duplicate text from one place to another', 'is_correct': True},
                    {'text': 'Change font size', 'is_correct': False},
                    {'text': 'Save the document', 'is_correct': False}
                ],
                'explanation': 'Copy and Paste allows you to duplicate text or other content from one place and put it in another place. This saves time when you need to repeat information.'
            },
            {
                'text': 'What is formatting in word processing?',
                'choices': [
                    {'text': 'Deleting the document', 'is_correct': False},
                    {'text': 'Changing the appearance of text (font, size, color)', 'is_correct': True},
                    {'text': 'Saving the document', 'is_correct': False},
                    {'text': 'Printing the document', 'is_correct': False}
                ],
                'explanation': 'Formatting means changing how text looks - such as making it bold, changing the font, size, or color. This makes documents more attractive and easier to read.'
            }
        ],

        'Computer Ethics': [
            {
                'text': 'What does computer ethics mean?',
                'choices': [
                    {'text': 'Rules about how to use computers properly and safely', 'is_correct': True},
                    {'text': 'How to repair computers', 'is_correct': False},
                    {'text': 'How to buy computers', 'is_correct': False},
                    {'text': 'How to build computers', 'is_correct': False}
                ],
                'explanation': 'Computer ethics refers to the rules and guidelines about how to use computers properly, safely, and responsibly. It helps us make good choices when using technology.'
            },
            {
                'text': 'Why should you not share your password with others?',
                'choices': [
                    {'text': 'It\'s not important', 'is_correct': False},
                    {'text': 'To keep your personal information safe', 'is_correct': True},
                    {'text': 'Passwords are meant to be shared', 'is_correct': False},
                    {'text': 'It makes the computer slower', 'is_correct': False}
                ],
                'explanation': 'You should not share your password because it protects your personal information. When others know your password, they can access your private files and accounts.'
            },
            {
                'text': 'What should you do if you see something inappropriate on the Internet?',
                'choices': [
                    {'text': 'Share it with friends', 'is_correct': False},
                    {'text': 'Tell a trusted adult immediately', 'is_correct': True},
                    {'text': 'Ignore it and continue browsing', 'is_correct': False},
                    {'text': 'Download it', 'is_correct': False}
                ],
                'explanation': 'If you see something inappropriate on the Internet, you should tell a trusted adult like a parent or teacher immediately. They can help you handle the situation properly.'
            },
            {
                'text': 'Is it okay to use someone else\'s work without permission?',
                'choices': [
                    {'text': 'Yes, everything on the Internet is free to use', 'is_correct': False},
                    {'text': 'No, you should always ask permission or give credit', 'is_correct': True},
                    {'text': 'Only if no one finds out', 'is_correct': False},
                    {'text': 'Yes, if it\'s for school work', 'is_correct': False}
                ],
                'explanation': 'No, you should not use someone else\'s work without permission. This is called plagiarism. Always ask permission or give credit to the original creator.'
            },
            {
                'text': 'What is cyberbullying?',
                'choices': [
                    {'text': 'Playing computer games', 'is_correct': False},
                    {'text': 'Using technology to hurt or embarrass others', 'is_correct': True},
                    {'text': 'Learning about computers', 'is_correct': False},
                    {'text': 'Fixing computer problems', 'is_correct': False}
                ],
                'explanation': 'Cyberbullying is using technology like computers, phones, or the Internet to hurt, embarrass, or be mean to other people. It is wrong and should be reported to adults.'
            }
        ],

        'Internet Basics': [
            {
                'text': 'What is the Internet?',
                'choices': [
                    {'text': 'A single computer', 'is_correct': False},
                    {'text': 'A global network of connected computers', 'is_correct': True},
                    {'text': 'A type of software', 'is_correct': False},
                    {'text': 'A computer game', 'is_correct': False}
                ],
                'explanation': 'The Internet is a global network that connects millions of computers around the world, allowing them to share information and communicate with each other.'
            },
            {
                'text': 'What is a web browser?',
                'choices': [
                    {'text': 'A type of computer', 'is_correct': False},
                    {'text': 'Software used to access websites on the Internet', 'is_correct': True},
                    {'text': 'A printer', 'is_correct': False},
                    {'text': 'A keyboard', 'is_correct': False}
                ],
                'explanation': 'A web browser is software that allows you to access and view websites on the Internet. Examples include Chrome, Firefox, Safari, and Edge.'
            },
            {
                'text': 'What does WWW stand for?',
                'choices': [
                    {'text': 'World Wide Web', 'is_correct': True},
                    {'text': 'World Wide Window', 'is_correct': False},
                    {'text': 'World Wide Work', 'is_correct': False},
                    {'text': 'World Wide Wire', 'is_correct': False}
                ],
                'explanation': 'WWW stands for World Wide Web. It is a system of websites and web pages that can be accessed through the Internet using web browsers.'
            },
            {
                'text': 'What is a website?',
                'choices': [
                    {'text': 'A physical location', 'is_correct': False},
                    {'text': 'A collection of web pages on the Internet', 'is_correct': True},
                    {'text': 'A type of computer', 'is_correct': False},
                    {'text': 'A software program', 'is_correct': False}
                ],
                'explanation': 'A website is a collection of related web pages that can be accessed on the Internet. Websites contain information, images, videos, and other content.'
            },
            {
                'text': 'What is email?',
                'choices': [
                    {'text': 'Electronic mail sent over the Internet', 'is_correct': True},
                    {'text': 'A type of computer', 'is_correct': False},
                    {'text': 'A web browser', 'is_correct': False},
                    {'text': 'A printer', 'is_correct': False}
                ],
                'explanation': 'Email (electronic mail) is a way to send messages and files to other people over the Internet. It\'s like sending a letter, but much faster.'
            },
            {
                'text': 'What is a search engine?',
                'choices': [
                    {'text': 'A type of car engine', 'is_correct': False},
                    {'text': 'A tool that helps you find information on the Internet', 'is_correct': True},
                    {'text': 'A computer game', 'is_correct': False},
                    {'text': 'A word processor', 'is_correct': False}
                ],
                'explanation': 'A search engine is a tool that helps you find information on the Internet by searching through millions of web pages. Google is the most popular search engine.'
            }
        ],

        'Multimedia': [
            {
                'text': 'What is multimedia?',
                'choices': [
                    {'text': 'Only text documents', 'is_correct': False},
                    {'text': 'Content that combines text, images, audio, and video', 'is_correct': True},
                    {'text': 'Only pictures', 'is_correct': False},
                    {'text': 'Only sound files', 'is_correct': False}
                ],
                'explanation': 'Multimedia is content that combines different types of media like text, images, audio (sound), and video all together to create rich, interactive experiences.'
            },
            {
                'text': 'Which of these is an example of multimedia?',
                'choices': [
                    {'text': 'A plain text document', 'is_correct': False},
                    {'text': 'A video with sound and text', 'is_correct': True},
                    {'text': 'A blank page', 'is_correct': False},
                    {'text': 'A calculator', 'is_correct': False}
                ],
                'explanation': 'A video with sound and text is multimedia because it combines different types of media - moving images (video), audio (sound), and text all in one.'
            },
            {
                'text': 'What is an image file?',
                'choices': [
                    {'text': 'A file that contains pictures or graphics', 'is_correct': True},
                    {'text': 'A file that contains only text', 'is_correct': False},
                    {'text': 'A file that contains only sound', 'is_correct': False},
                    {'text': 'A file that contains only numbers', 'is_correct': False}
                ],
                'explanation': 'An image file is a computer file that contains pictures, photos, or graphics. Common image file types include JPEG, PNG, and GIF.'
            },
            {
                'text': 'What is an audio file?',
                'choices': [
                    {'text': 'A file that contains pictures', 'is_correct': False},
                    {'text': 'A file that contains sound or music', 'is_correct': True},
                    {'text': 'A file that contains text', 'is_correct': False},
                    {'text': 'A file that contains videos', 'is_correct': False}
                ],
                'explanation': 'An audio file is a computer file that contains sound, music, or voice recordings. Common audio file types include MP3, WAV, and AAC.'
            },
            {
                'text': 'What can you do with multimedia on a computer?',
                'choices': [
                    {'text': 'Only read text', 'is_correct': False},
                    {'text': 'Watch videos, listen to music, view pictures, and read text', 'is_correct': True},
                    {'text': 'Only calculate numbers', 'is_correct': False},
                    {'text': 'Only print documents', 'is_correct': False}
                ],
                'explanation': 'With multimedia on a computer, you can enjoy many different types of content - watch videos, listen to music, view pictures, read text, and even create your own multimedia content.'
            },
            {
                'text': 'Why is multimedia useful in learning?',
                'choices': [
                    {'text': 'It makes learning boring', 'is_correct': False},
                    {'text': 'It makes learning more interesting and easier to understand', 'is_correct': True},
                    {'text': 'It makes learning harder', 'is_correct': False},
                    {'text': 'It has no effect on learning', 'is_correct': False}
                ],
                'explanation': 'Multimedia makes learning more interesting and easier to understand because it appeals to different senses - we can see, hear, and interact with the content, which helps us learn better.'
            }
        ]
    }


def create_ict_questions():
    """Create ICT questions for Primary 6."""
    try:
        # Get the Ghana curriculum and Primary 6 class level
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)
        ict_subject = Subject.objects.get(name='ICT', class_level=primary6)

        print(f"Found ICT subject: {ict_subject.name} - {ict_subject.class_level.name}")

        questions_data = get_ict_questions_data()
        total_questions_created = 0

        for topic_name, topic_questions in questions_data.items():
            try:
                topic = Topic.objects.get(name=topic_name, subject=ict_subject)
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

                    questions_created += 1

                print(f"  Created {questions_created} questions for {topic.name}")
                total_questions_created += questions_created

            except Topic.DoesNotExist:
                print(f"  Topic '{topic_name}' not found, skipping...")

        print(f"\nTotal ICT questions created: {total_questions_created}")

        # Create or update the ICT quiz
        quiz, created = Quiz.objects.get_or_create(
            title="ICT Quiz - Primary 6",
            curriculum=ghana_curriculum,
            class_level=primary6,
            subject=ict_subject,
            defaults={
                'description': 'Test your knowledge of ICT concepts for Primary 6 level',
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
    print("Adding comprehensive ICT questions for Primary 6...")
    success = create_ict_questions()

    if success:
        print("\nICT questions added successfully!")
    else:
        print("\nFailed to add ICT questions.")
