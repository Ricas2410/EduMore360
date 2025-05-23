#!/usr/bin/env python
"""
Script to add comprehensive ICT questions based on GES ICT curriculum.
Covers Hardware, Software, Programming Basics, Networks, and other essential ICT topics.
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


def get_comprehensive_ict_questions_data():
    """Return comprehensive ICT questions based on GES curriculum."""
    return {
        'Computer Hardware': [
            {
                'text': 'What is computer hardware?',
                'choices': [
                    {'text': 'The physical parts of a computer you can touch', 'is_correct': True},
                    {'text': 'Computer programs and applications', 'is_correct': False},
                    {'text': 'Internet websites', 'is_correct': False},
                    {'text': 'Computer games', 'is_correct': False}
                ],
                'explanation': 'Computer hardware refers to the physical components of a computer that you can touch, such as the monitor, keyboard, mouse, CPU, and hard drive.'
            },
            {
                'text': 'Which of these is an input device?',
                'choices': [
                    {'text': 'Monitor', 'is_correct': False},
                    {'text': 'Printer', 'is_correct': False},
                    {'text': 'Mouse', 'is_correct': True},
                    {'text': 'Speaker', 'is_correct': False}
                ],
                'explanation': 'A mouse is an input device because it allows you to input commands and data into the computer. Input devices help you communicate with the computer.'
            },
            {
                'text': 'Which of these is an output device?',
                'choices': [
                    {'text': 'Keyboard', 'is_correct': False},
                    {'text': 'Printer', 'is_correct': True},
                    {'text': 'Mouse', 'is_correct': False},
                    {'text': 'Microphone', 'is_correct': False}
                ],
                'explanation': 'A printer is an output device because it produces output from the computer in the form of printed documents or images.'
            },
            {
                'text': 'What does CPU stand for?',
                'choices': [
                    {'text': 'Computer Processing Unit', 'is_correct': False},
                    {'text': 'Central Processing Unit', 'is_correct': True},
                    {'text': 'Computer Program Unit', 'is_correct': False},
                    {'text': 'Central Program Unit', 'is_correct': False}
                ],
                'explanation': 'CPU stands for Central Processing Unit. It is the brain of the computer that processes all instructions and performs calculations.'
            },
            {
                'text': 'What is the main function of RAM?',
                'choices': [
                    {'text': 'To store data permanently', 'is_correct': False},
                    {'text': 'To provide temporary storage for data being used', 'is_correct': True},
                    {'text': 'To display images on screen', 'is_correct': False},
                    {'text': 'To connect to the internet', 'is_correct': False}
                ],
                'explanation': 'RAM (Random Access Memory) provides temporary storage for data and programs that are currently being used by the computer. When you turn off the computer, data in RAM is lost.'
            },
            {
                'text': 'Which storage device can store the most data?',
                'choices': [
                    {'text': 'Floppy disk', 'is_correct': False},
                    {'text': 'CD-ROM', 'is_correct': False},
                    {'text': 'Hard drive', 'is_correct': True},
                    {'text': 'USB flash drive', 'is_correct': False}
                ],
                'explanation': 'A hard drive can typically store the most data among these options. Modern hard drives can store terabytes of data, much more than CDs, floppy disks, or most USB drives.'
            },
            {
                'text': 'What is the difference between hardware and software?',
                'choices': [
                    {'text': 'There is no difference', 'is_correct': False},
                    {'text': 'Hardware is physical, software is programs and instructions', 'is_correct': True},
                    {'text': 'Hardware is newer than software', 'is_correct': False},
                    {'text': 'Software is more expensive than hardware', 'is_correct': False}
                ],
                'explanation': 'Hardware consists of physical components you can touch (like keyboard, monitor), while software consists of programs, applications, and instructions that tell the hardware what to do.'
            },
            {
                'text': 'What is a motherboard?',
                'choices': [
                    {'text': 'A type of keyboard', 'is_correct': False},
                    {'text': 'The main circuit board that connects all computer components', 'is_correct': True},
                    {'text': 'A computer screen', 'is_correct': False},
                    {'text': 'A storage device', 'is_correct': False}
                ],
                'explanation': 'The motherboard is the main circuit board inside a computer that connects and allows communication between all the different components like CPU, RAM, and storage devices.'
            }
        ],

        'Computer Software': [
            {
                'text': 'What is computer software?',
                'choices': [
                    {'text': 'The physical parts of a computer', 'is_correct': False},
                    {'text': 'Programs and instructions that tell the computer what to do', 'is_correct': True},
                    {'text': 'The computer screen', 'is_correct': False},
                    {'text': 'Computer cables and wires', 'is_correct': False}
                ],
                'explanation': 'Computer software consists of programs, applications, and instructions that tell the computer hardware what to do. Examples include operating systems, games, and word processors.'
            },
            {
                'text': 'What is an operating system?',
                'choices': [
                    {'text': 'A computer game', 'is_correct': False},
                    {'text': 'Software that manages the computer and runs other programs', 'is_correct': True},
                    {'text': 'A type of hardware', 'is_correct': False},
                    {'text': 'An internet browser', 'is_correct': False}
                ],
                'explanation': 'An operating system (like Windows, macOS, or Linux) is software that manages the computer\'s hardware and provides a platform for other programs to run.'
            },
            {
                'text': 'Which of these is an example of application software?',
                'choices': [
                    {'text': 'Windows', 'is_correct': False},
                    {'text': 'Microsoft Word', 'is_correct': True},
                    {'text': 'Device drivers', 'is_correct': False},
                    {'text': 'BIOS', 'is_correct': False}
                ],
                'explanation': 'Microsoft Word is application software - a program designed to help users accomplish specific tasks, in this case, word processing and document creation.'
            },
            {
                'text': 'What is the difference between system software and application software?',
                'choices': [
                    {'text': 'There is no difference', 'is_correct': False},
                    {'text': 'System software manages the computer; application software helps users do tasks', 'is_correct': True},
                    {'text': 'Application software is always free', 'is_correct': False},
                    {'text': 'System software is newer', 'is_correct': False}
                ],
                'explanation': 'System software (like operating systems) manages the computer and its resources. Application software (like games, word processors) helps users accomplish specific tasks.'
            },
            {
                'text': 'What is a computer virus?',
                'choices': [
                    {'text': 'A helpful program', 'is_correct': False},
                    {'text': 'Harmful software that can damage your computer', 'is_correct': True},
                    {'text': 'A type of hardware', 'is_correct': False},
                    {'text': 'A computer game', 'is_correct': False}
                ],
                'explanation': 'A computer virus is harmful software (malware) that can damage your computer, steal information, or disrupt normal operations. It\'s important to use antivirus software for protection.'
            },
            {
                'text': 'What is antivirus software?',
                'choices': [
                    {'text': 'Software that creates viruses', 'is_correct': False},
                    {'text': 'Software that protects your computer from harmful programs', 'is_correct': True},
                    {'text': 'A type of game', 'is_correct': False},
                    {'text': 'Software for creating documents', 'is_correct': False}
                ],
                'explanation': 'Antivirus software protects your computer by detecting, preventing, and removing harmful software like viruses, malware, and other threats.'
            },
            {
                'text': 'What does it mean to "install" software?',
                'choices': [
                    {'text': 'To delete software from the computer', 'is_correct': False},
                    {'text': 'To put software on the computer so it can be used', 'is_correct': True},
                    {'text': 'To repair broken software', 'is_correct': False},
                    {'text': 'To update software', 'is_correct': False}
                ],
                'explanation': 'Installing software means putting a program on your computer and setting it up so that it can be used. This usually involves copying files and configuring settings.'
            }
        ],

        'Programming and Algorithms': [
            {
                'text': 'What is an algorithm?',
                'choices': [
                    {'text': 'A type of computer', 'is_correct': False},
                    {'text': 'A step-by-step set of instructions to solve a problem', 'is_correct': True},
                    {'text': 'A computer game', 'is_correct': False},
                    {'text': 'A type of software', 'is_correct': False}
                ],
                'explanation': 'An algorithm is a step-by-step set of instructions or rules designed to solve a problem or complete a task. It\'s like a recipe that tells you exactly what to do.'
            },
            {
                'text': 'What is programming?',
                'choices': [
                    {'text': 'Playing computer games', 'is_correct': False},
                    {'text': 'Writing instructions for computers to follow', 'is_correct': True},
                    {'text': 'Fixing broken computers', 'is_correct': False},
                    {'text': 'Using the internet', 'is_correct': False}
                ],
                'explanation': 'Programming is the process of writing step-by-step instructions (called code) that tell a computer what to do. Programmers use special languages to communicate with computers.'
            },
            {
                'text': 'What is a programming language?',
                'choices': [
                    {'text': 'A language spoken by computers', 'is_correct': False},
                    {'text': 'A special language used to write computer programs', 'is_correct': True},
                    {'text': 'A foreign language', 'is_correct': False},
                    {'text': 'A type of hardware', 'is_correct': False}
                ],
                'explanation': 'A programming language is a special language with specific rules and syntax that programmers use to write instructions for computers. Examples include Python, Java, and Scratch.'
            },
            {
                'text': 'Which of these is a beginner-friendly programming language for children?',
                'choices': [
                    {'text': 'Assembly', 'is_correct': False},
                    {'text': 'Scratch', 'is_correct': True},
                    {'text': 'Machine Code', 'is_correct': False},
                    {'text': 'Binary', 'is_correct': False}
                ],
                'explanation': 'Scratch is a visual programming language designed for children. It uses colorful blocks that snap together to create programs, making it easy and fun to learn programming concepts.'
            },
            {
                'text': 'What is debugging in programming?',
                'choices': [
                    {'text': 'Adding more features to a program', 'is_correct': False},
                    {'text': 'Finding and fixing errors in a program', 'is_correct': True},
                    {'text': 'Deleting a program', 'is_correct': False},
                    {'text': 'Installing a program', 'is_correct': False}
                ],
                'explanation': 'Debugging is the process of finding and fixing errors (called bugs) in a computer program. It\'s an important skill for programmers to ensure their programs work correctly.'
            },
            {
                'text': 'What is a loop in programming?',
                'choices': [
                    {'text': 'A circle drawn on screen', 'is_correct': False},
                    {'text': 'Instructions that repeat multiple times', 'is_correct': True},
                    {'text': 'A type of computer', 'is_correct': False},
                    {'text': 'An error in the program', 'is_correct': False}
                ],
                'explanation': 'A loop is a programming concept that allows instructions to be repeated multiple times. For example, you might use a loop to count from 1 to 10 or to repeat an animation.'
            }
        ],

        'Computer Networks and Communication': [
            {
                'text': 'What is a computer network?',
                'choices': [
                    {'text': 'A single computer', 'is_correct': False},
                    {'text': 'Two or more computers connected together to share information', 'is_correct': True},
                    {'text': 'A computer game', 'is_correct': False},
                    {'text': 'A type of software', 'is_correct': False}
                ],
                'explanation': 'A computer network is a group of two or more computers connected together so they can share information, resources, and communicate with each other.'
            },
            {
                'text': 'What does LAN stand for?',
                'choices': [
                    {'text': 'Large Area Network', 'is_correct': False},
                    {'text': 'Local Area Network', 'is_correct': True},
                    {'text': 'Long Area Network', 'is_correct': False},
                    {'text': 'Limited Area Network', 'is_correct': False}
                ],
                'explanation': 'LAN stands for Local Area Network. It\'s a network that connects computers in a small area like a school, office, or home.'
            },
            {
                'text': 'What does WAN stand for?',
                'choices': [
                    {'text': 'Wide Area Network', 'is_correct': True},
                    {'text': 'Wireless Area Network', 'is_correct': False},
                    {'text': 'World Area Network', 'is_correct': False},
                    {'text': 'Web Area Network', 'is_correct': False}
                ],
                'explanation': 'WAN stands for Wide Area Network. It connects computers over large geographical areas, like connecting networks in different cities or countries. The Internet is the largest WAN.'
            },
            {
                'text': 'What is Wi-Fi?',
                'choices': [
                    {'text': 'A type of computer', 'is_correct': False},
                    {'text': 'A wireless way to connect to the internet', 'is_correct': True},
                    {'text': 'A computer game', 'is_correct': False},
                    {'text': 'A type of software', 'is_correct': False}
                ],
                'explanation': 'Wi-Fi is a wireless technology that allows devices like computers, phones, and tablets to connect to the internet without using cables.'
            },
            {
                'text': 'What is the purpose of a router?',
                'choices': [
                    {'text': 'To store files', 'is_correct': False},
                    {'text': 'To connect different networks and direct data traffic', 'is_correct': True},
                    {'text': 'To display images', 'is_correct': False},
                    {'text': 'To print documents', 'is_correct': False}
                ],
                'explanation': 'A router is a device that connects different networks together and directs data traffic between them. It helps devices in your home connect to the internet.'
            },
            {
                'text': 'What is bandwidth in networking?',
                'choices': [
                    {'text': 'The width of a computer screen', 'is_correct': False},
                    {'text': 'The amount of data that can be transmitted over a network', 'is_correct': True},
                    {'text': 'The size of a computer file', 'is_correct': False},
                    {'text': 'The number of computers in a network', 'is_correct': False}
                ],
                'explanation': 'Bandwidth refers to the amount of data that can be transmitted over a network connection in a given amount of time. Higher bandwidth means faster internet speeds.'
            }
        ],

        'Digital Citizenship and Safety': [
            {
                'text': 'What is digital citizenship?',
                'choices': [
                    {'text': 'Being a citizen of a digital country', 'is_correct': False},
                    {'text': 'Using technology responsibly and safely', 'is_correct': True},
                    {'text': 'Only using digital devices', 'is_correct': False},
                    {'text': 'Avoiding all technology', 'is_correct': False}
                ],
                'explanation': 'Digital citizenship means using technology responsibly, safely, and ethically. It includes being respectful online, protecting personal information, and following digital laws and rules.'
            },
            {
                'text': 'What should you do if someone online asks for your personal information?',
                'choices': [
                    {'text': 'Give them all the information they want', 'is_correct': False},
                    {'text': 'Don\'t give personal information and tell a trusted adult', 'is_correct': True},
                    {'text': 'Give them only some information', 'is_correct': False},
                    {'text': 'Ask them for their information first', 'is_correct': False}
                ],
                'explanation': 'Never give personal information (like your real name, address, phone number, or school) to strangers online. Always tell a trusted adult if someone asks for this information.'
            },
            {
                'text': 'What is a strong password?',
                'choices': [
                    {'text': 'Your name', 'is_correct': False},
                    {'text': 'A combination of letters, numbers, and symbols that is hard to guess', 'is_correct': True},
                    {'text': '123456', 'is_correct': False},
                    {'text': 'Your birthday', 'is_correct': False}
                ],
                'explanation': 'A strong password is long and includes a mix of uppercase letters, lowercase letters, numbers, and symbols. It should be something that others cannot easily guess.'
            },
            {
                'text': 'What is cyberbullying?',
                'choices': [
                    {'text': 'A computer game', 'is_correct': False},
                    {'text': 'Using technology to hurt, embarrass, or threaten others', 'is_correct': True},
                    {'text': 'Learning about computers', 'is_correct': False},
                    {'text': 'Fixing computer problems', 'is_correct': False}
                ],
                'explanation': 'Cyberbullying is using technology (like computers, phones, or social media) to hurt, embarrass, threaten, or be mean to other people. It is wrong and should be reported to adults.'
            },
            {
                'text': 'What should you do if you encounter inappropriate content online?',
                'choices': [
                    {'text': 'Share it with friends', 'is_correct': False},
                    {'text': 'Close it immediately and tell a trusted adult', 'is_correct': True},
                    {'text': 'Keep looking at it', 'is_correct': False},
                    {'text': 'Download it', 'is_correct': False}
                ],
                'explanation': 'If you see inappropriate content online, close it immediately and tell a trusted adult like a parent, teacher, or guardian. They can help you handle the situation properly.'
            },
            {
                'text': 'Why is it important to respect others online?',
                'choices': [
                    {'text': 'It\'s not important', 'is_correct': False},
                    {'text': 'Because people online have feelings just like people in real life', 'is_correct': True},
                    {'text': 'Only to avoid getting in trouble', 'is_correct': False},
                    {'text': 'Because it\'s required by law', 'is_correct': False}
                ],
                'explanation': 'It\'s important to respect others online because people on the internet have real feelings just like people you meet in person. Being kind and respectful online helps create a better digital world for everyone.'
            }
        ]
    }


def create_comprehensive_ict_questions():
    """Create comprehensive ICT questions for both Primary 5 and Primary 6."""
    try:
        # Get the Ghana curriculum and class levels
        ghana_curriculum = Curriculum.objects.get(code='GH')
        primary5 = ClassLevel.objects.get(name='Primary 5', curriculum=ghana_curriculum)
        primary6 = ClassLevel.objects.get(name='Primary 6', curriculum=ghana_curriculum)

        # Get ICT subjects for both classes
        ict_subject_p5 = Subject.objects.get(name='ICT', class_level=primary5)
        ict_subject_p6 = Subject.objects.get(name='ICT', class_level=primary6)

        print(f"Adding comprehensive ICT questions based on GES curriculum...")
        print(f"- {ict_subject_p5.name} - {ict_subject_p5.class_level.name}")
        print(f"- {ict_subject_p6.name} - {ict_subject_p6.class_level.name}")

        questions_data = get_comprehensive_ict_questions_data()
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
                        'description': f'{topic_name} concepts based on GES ICT curriculum for {class_level.name}'
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
                        difficulty='easy',  # Primary level
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

            print(f"  Total new ICT questions created for {class_level.name}: {class_questions_created}")
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
                quiz.description = f'Comprehensive ICT knowledge test covering hardware, software, programming, networks, databases, and digital citizenship for {class_level.name} level'
                quiz.save()

                print(f"  Updated quiz: {quiz.title} (Total questions: {total_ict_questions})")

            except Quiz.DoesNotExist:
                print(f"  Warning: ICT Quiz for {class_level.name} not found")

        print(f"\nTotal new ICT questions created: {total_questions_created}")

        # Show final ICT topic structure
        print(f"\nFinal ICT curriculum structure:")
        for class_level in [primary5, primary6]:
            ict_subject = Subject.objects.get(name='ICT', class_level=class_level)
            topics = Topic.objects.filter(subject=ict_subject).order_by('name')
            total_questions = Question.objects.filter(subject=ict_subject).count()

            print(f"\n{class_level.name} ICT ({total_questions} total questions):")
            for topic in topics:
                question_count = Question.objects.filter(topic=topic).count()
                print(f"  - {topic.name}: {question_count} questions")

        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 Adding comprehensive ICT questions based on GES curriculum...")
    print("📚 Topics: Hardware, Software, Programming, Networks, Digital Citizenship")

    success = create_comprehensive_ict_questions()

    if success:
        print("\n🎉 Comprehensive ICT questions added successfully!")
        print("🌍 Your ICT curriculum now covers all essential topics!")
        print("🏆 Students will have world-class ICT education!")
    else:
        print("\n❌ Failed to add comprehensive ICT questions.")
