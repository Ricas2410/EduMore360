"""
Script to populate SHS2 and Primary 6 with 40 sample quiz questions for each subject:
ICT, English, Science, Mathematics, and Social Studies.
Following the Ghana Education Service (GES) curriculum.
"""

import os
import sys
import django
import random
from django.utils.text import slugify

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from quiz.models import Question, QuestionChoice, Quiz

# Define the subjects and class levels we want to populate
SUBJECTS = ['ICT', 'English', 'Science', 'Mathematics', 'Social Studies']
CLASS_LEVELS = ['SHS 2', 'Primary 6']

# Define topics for each subject based on GES curriculum
TOPICS = {
    'ICT': {
        'SHS 2': [
            'Database Management Systems',
            'Programming Concepts',
            'Networking and Internet',
            'Information Security',
            'Web Development'
        ],
        'Primary 6': [
            'Introduction to Computers',
            'Word Processing',
            'Internet Basics',
            'Computer Ethics',
            'Multimedia'
        ]
    },
    'English': {
        'SHS 2': [
            'Reading Comprehension',
            'Grammar and Structure',
            'Literature',
            'Writing Skills',
            'Oral Communication'
        ],
        'Primary 6': [
            'Reading and Comprehension',
            'Grammar',
            'Composition Writing',
            'Listening and Speaking',
            'Vocabulary Development'
        ]
    },
    'Science': {
        'SHS 2': [
            'Biology - Cells and Genetics',
            'Chemistry - Chemical Reactions',
            'Physics - Forces and Motion',
            'Environmental Science',
            'Scientific Method'
        ],
        'Primary 6': [
            'Living Things',
            'Materials',
            'Energy and Forces',
            'Earth and Space',
            'Human Body'
        ]
    },
    'Mathematics': {
        'SHS 2': [
            'Algebra',
            'Trigonometry',
            'Statistics and Probability',
            'Geometry',
            'Calculus Basics'
        ],
        'Primary 6': [
            'Numbers and Operations',
            'Fractions and Decimals',
            'Measurement',
            'Geometry and Shapes',
            'Data Handling'
        ]
    },
    'Social Studies': {
        'SHS 2': [
            'Governance and Politics',
            'Economic Development',
            'Cultural Practices',
            'Environmental Issues',
            'Global Connections'
        ],
        'Primary 6': [
            'Our Nation Ghana',
            'Map Reading',
            'Environment and Resources',
            'Governance',
            'Cultural Identity'
        ]
    }
}

# Sample questions for each topic
def get_sample_questions(subject, class_level, topic):
    """Generate sample questions for a specific topic."""
    questions = []

    if subject == 'ICT':
        if class_level == 'SHS 2':
            if 'Database' in topic:
                questions.extend([
                    {
                        'text': 'Which of the following is NOT a type of database?',
                        'choices': [
                            {'text': 'Relational Database', 'is_correct': False},
                            {'text': 'NoSQL Database', 'is_correct': False},
                            {'text': 'Graphical Database', 'is_correct': True},
                            {'text': 'Object-Oriented Database', 'is_correct': False}
                        ],
                        'explanation': 'Graphical Database is not a standard type of database. The common types include Relational, NoSQL, Object-Oriented, and Hierarchical databases.'
                    },
                    {
                        'text': 'What does SQL stand for?',
                        'choices': [
                            {'text': 'Structured Query Language', 'is_correct': True},
                            {'text': 'Simple Query Language', 'is_correct': False},
                            {'text': 'Standard Query Logic', 'is_correct': False},
                            {'text': 'System Query Language', 'is_correct': False}
                        ],
                        'explanation': 'SQL stands for Structured Query Language, which is used for managing and manipulating relational databases.'
                    },
                    # Add more questions as needed
                ])
            elif 'Programming' in topic:
                questions.extend([
                    {
                        'text': 'Which of the following is not a programming paradigm?',
                        'choices': [
                            {'text': 'Object-Oriented Programming', 'is_correct': False},
                            {'text': 'Functional Programming', 'is_correct': False},
                            {'text': 'Procedural Programming', 'is_correct': False},
                            {'text': 'Alphabetical Programming', 'is_correct': True}
                        ],
                        'explanation': 'Alphabetical Programming is not a recognized programming paradigm. The common paradigms include Object-Oriented, Functional, and Procedural Programming.'
                    },
                    {
                        'text': 'What is the purpose of a loop in programming?',
                        'choices': [
                            {'text': 'To repeat a block of code multiple times', 'is_correct': True},
                            {'text': 'To create a new variable', 'is_correct': False},
                            {'text': 'To connect to a database', 'is_correct': False},
                            {'text': 'To terminate a program', 'is_correct': False}
                        ],
                        'explanation': 'Loops are used to repeat a block of code multiple times, which helps in automating repetitive tasks.'
                    },
                    # Add more questions as needed
                ])
        elif class_level == 'Primary 6':
            if 'Introduction to Computers' in topic:
                questions.extend([
                    {
                        'text': 'Which of these is an input device?',
                        'choices': [
                            {'text': 'Monitor', 'is_correct': False},
                            {'text': 'Printer', 'is_correct': False},
                            {'text': 'Keyboard', 'is_correct': True},
                            {'text': 'Speaker', 'is_correct': False}
                        ],
                        'explanation': 'A keyboard is an input device used to enter data into a computer.'
                    },
                    {
                        'text': 'What is the brain of the computer called?',
                        'choices': [
                            {'text': 'RAM', 'is_correct': False},
                            {'text': 'CPU', 'is_correct': True},
                            {'text': 'Hard Drive', 'is_correct': False},
                            {'text': 'Monitor', 'is_correct': False}
                        ],
                        'explanation': 'The CPU (Central Processing Unit) is considered the brain of the computer as it processes all instructions.'
                    },
                    # Add more questions as needed
                ])

    # Add more subject-specific questions
    if subject == 'English':
        if class_level == 'SHS 2':
            if 'Grammar' in topic:
                questions.extend([
                    {
                        'text': 'Which of the following is a correct example of the past perfect tense?',
                        'choices': [
                            {'text': 'I am walking to school', 'is_correct': False},
                            {'text': 'I had walked to school', 'is_correct': True},
                            {'text': 'I will walk to school', 'is_correct': False},
                            {'text': 'I walk to school', 'is_correct': False}
                        ],
                        'explanation': 'The past perfect tense is formed with "had" + past participle. "I had walked to school" is the correct example.'
                    },
                    {
                        'text': 'Which sentence contains a dangling modifier?',
                        'choices': [
                            {'text': 'The teacher explained the lesson clearly', 'is_correct': False},
                            {'text': 'Walking to school, my bag was heavy', 'is_correct': True},
                            {'text': 'She read the book that I recommended', 'is_correct': False},
                            {'text': 'They completed their homework on time', 'is_correct': False}
                        ],
                        'explanation': 'In "Walking to school, my bag was heavy," the modifier "walking to school" is dangling because it incorrectly modifies "my bag" instead of the person who was walking.'
                    }
                ])
            elif 'Literature' in topic:
                questions.extend([
                    {
                        'text': 'Which literary device involves comparing two unlike things without using "like" or "as"?',
                        'choices': [
                            {'text': 'Simile', 'is_correct': False},
                            {'text': 'Metaphor', 'is_correct': True},
                            {'text': 'Alliteration', 'is_correct': False},
                            {'text': 'Onomatopoeia', 'is_correct': False}
                        ],
                        'explanation': 'A metaphor directly compares two unlike things without using "like" or "as". For example, "Time is money."'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Grammar' in topic:
                questions.extend([
                    {
                        'text': 'Which of the following is a proper noun?',
                        'choices': [
                            {'text': 'boy', 'is_correct': False},
                            {'text': 'happiness', 'is_correct': False},
                            {'text': 'Accra', 'is_correct': True},
                            {'text': 'book', 'is_correct': False}
                        ],
                        'explanation': 'Proper nouns name specific people, places, or things and are always capitalized. "Accra" is a proper noun because it names a specific city.'
                    }
                ])

    elif subject == 'Mathematics':
        if class_level == 'SHS 2':
            if 'Algebra' in topic:
                questions.extend([
                    {
                        'text': 'Solve for x: 2x + 5 = 15',
                        'choices': [
                            {'text': 'x = 5', 'is_correct': True},
                            {'text': 'x = 10', 'is_correct': False},
                            {'text': 'x = 7.5', 'is_correct': False},
                            {'text': 'x = 20', 'is_correct': False}
                        ],
                        'explanation': 'To solve for x, subtract 5 from both sides: 2x = 10. Then divide both sides by 2: x = 5.'
                    }
                ])
            elif 'Trigonometry' in topic:
                questions.extend([
                    {
                        'text': 'What is the value of sin(30°)?',
                        'choices': [
                            {'text': '0', 'is_correct': False},
                            {'text': '0.5', 'is_correct': True},
                            {'text': '1', 'is_correct': False},
                            {'text': '√3/2', 'is_correct': False}
                        ],
                        'explanation': 'The value of sin(30°) is 0.5 or 1/2.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Fractions' in topic:
                questions.extend([
                    {
                        'text': 'What is 1/4 + 1/2?',
                        'choices': [
                            {'text': '1/6', 'is_correct': False},
                            {'text': '2/6', 'is_correct': False},
                            {'text': '3/4', 'is_correct': True},
                            {'text': '1', 'is_correct': False}
                        ],
                        'explanation': 'To add fractions with different denominators, find a common denominator. 1/4 = 2/8 and 1/2 = 4/8. So 1/4 + 1/2 = 2/8 + 4/8 = 6/8 = 3/4.'
                    }
                ])

    elif subject == 'Science':
        if class_level == 'SHS 2':
            if 'Biology' in topic:
                questions.extend([
                    {
                        'text': 'Which organelle is known as the "powerhouse of the cell"?',
                        'choices': [
                            {'text': 'Nucleus', 'is_correct': False},
                            {'text': 'Mitochondria', 'is_correct': True},
                            {'text': 'Ribosome', 'is_correct': False},
                            {'text': 'Golgi apparatus', 'is_correct': False}
                        ],
                        'explanation': 'Mitochondria are known as the "powerhouse of the cell" because they generate most of the cell\'s supply of ATP, which is used as a source of chemical energy.'
                    }
                ])
            elif 'Chemistry' in topic:
                questions.extend([
                    {
                        'text': 'What is the chemical formula for water?',
                        'choices': [
                            {'text': 'H2O', 'is_correct': True},
                            {'text': 'CO2', 'is_correct': False},
                            {'text': 'O2', 'is_correct': False},
                            {'text': 'NaCl', 'is_correct': False}
                        ],
                        'explanation': 'The chemical formula for water is H2O, which means it consists of two hydrogen atoms and one oxygen atom.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Living Things' in topic:
                questions.extend([
                    {
                        'text': 'Which of these is NOT a characteristic of living things?',
                        'choices': [
                            {'text': 'Growth', 'is_correct': False},
                            {'text': 'Respiration', 'is_correct': False},
                            {'text': 'Magnetism', 'is_correct': True},
                            {'text': 'Reproduction', 'is_correct': False}
                        ],
                        'explanation': 'Magnetism is a physical property of certain materials, not a characteristic of living things. Living things exhibit growth, respiration, reproduction, etc.'
                    }
                ])

    elif subject == 'Social Studies':
        if class_level == 'SHS 2':
            if 'Governance' in topic:
                questions.extend([
                    {
                        'text': 'What is the name of Ghana\'s parliament?',
                        'choices': [
                            {'text': 'House of Commons', 'is_correct': False},
                            {'text': 'National Assembly', 'is_correct': False},
                            {'text': 'Parliament of Ghana', 'is_correct': True},
                            {'text': 'Congress', 'is_correct': False}
                        ],
                        'explanation': 'Ghana\'s legislative body is officially called the Parliament of Ghana.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Our Nation Ghana' in topic:
                questions.extend([
                    {
                        'text': 'Who was the first president of Ghana?',
                        'choices': [
                            {'text': 'Jerry John Rawlings', 'is_correct': False},
                            {'text': 'Kwame Nkrumah', 'is_correct': True},
                            {'text': 'John Agyekum Kufuor', 'is_correct': False},
                            {'text': 'John Dramani Mahama', 'is_correct': False}
                        ],
                        'explanation': 'Dr. Kwame Nkrumah was the first president of Ghana after independence in 1957.'
                    }
                ])

    # Generate generic questions if specific ones aren't defined
    while len(questions) < 8:  # Generate 8 questions per topic (5 topics x 8 questions = 40 per subject)
        question_num = len(questions) + 1
        questions.append({
            'text': f'Sample question {question_num} for {topic} in {subject} ({class_level})',
            'choices': [
                {'text': f'Correct answer for question {question_num}', 'is_correct': True},
                {'text': f'Wrong answer 1 for question {question_num}', 'is_correct': False},
                {'text': f'Wrong answer 2 for question {question_num}', 'is_correct': False},
                {'text': f'Wrong answer 3 for question {question_num}', 'is_correct': False}
            ],
            'explanation': f'This is an explanation for sample question {question_num}.'
        })

    return questions

def create_or_get_topic(subject_obj, topic_name):
    """Create a topic if it doesn't exist, or get it if it does."""
    topic, created = Topic.objects.get_or_create(
        subject=subject_obj,
        name=topic_name,
        defaults={
            'slug': slugify(topic_name),
            'description': f'Topic for {topic_name} in {subject_obj.name}',
            'is_active': True
        }
    )

    if created:
        print(f"  + Created topic: {topic.name}")
    else:
        print(f"  - Topic already exists: {topic.name}")

    return topic

def create_quiz_questions(curriculum, class_level_obj, subject_obj, topic_obj, questions_data):
    """Create quiz questions for a specific topic."""
    questions_created = 0

    for question_data in questions_data:
        # Create the question
        question = Question.objects.create(
            text=question_data['text'],
            question_type='multiple_choice',
            difficulty='medium',
            explanation=question_data['explanation'],
            curriculum=curriculum,
            class_level=class_level_obj,
            subject=subject_obj,
            topic=topic_obj,
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

    return questions_created

def create_quiz(curriculum, class_level_obj, subject_obj):
    """Create a quiz for a subject."""
    quiz, created = Quiz.objects.get_or_create(
        title=f"{subject_obj.name} Quiz - {class_level_obj.name}",
        curriculum=curriculum,
        class_level=class_level_obj,
        subject=subject_obj,
        defaults={
            'description': f"Test your knowledge of {subject_obj.name} for {class_level_obj.name}",
            'quiz_type': 'general',
            'question_count': 40,
            'per_question_time': 30,
            'randomize_questions': True,
            'randomize_choices': True,
            'show_immediate_feedback': True,
            'passing_score': 70,
            'is_active': True,
            'is_featured': True
        }
    )

    if created:
        print(f"  + Created quiz: {quiz.title}")
    else:
        print(f"  - Quiz already exists: {quiz.title}")

    return quiz

def main():
    """Main function to populate quiz questions."""
    try:
        # Get the Ghana curriculum
        ghana_curriculum = Curriculum.objects.get(code='GH')
        print(f"Found Ghana Curriculum: {ghana_curriculum.name}")

        total_questions_created = 0

        # Process each class level
        for class_level_name in CLASS_LEVELS:
            class_level = ClassLevel.objects.get(name=class_level_name, curriculum=ghana_curriculum)
            print(f"\nProcessing class level: {class_level.name}")

            # Process each subject
            for subject_name in SUBJECTS:
                try:
                    subject = Subject.objects.get(name=subject_name, class_level=class_level)
                    print(f"\n  Processing subject: {subject.name}")

                    # Create a quiz for this subject
                    quiz = create_quiz(ghana_curriculum, class_level, subject)

                    # Process each topic for this subject
                    subject_questions_created = 0
                    for topic_name in TOPICS[subject_name][class_level_name]:
                        topic = create_or_get_topic(subject, topic_name)

                        # Generate and create questions for this topic
                        questions_data = get_sample_questions(subject_name, class_level_name, topic_name)
                        questions_created = create_quiz_questions(ghana_curriculum, class_level, subject, topic, questions_data)

                        print(f"    + Added {questions_created} questions for topic: {topic.name}")
                        subject_questions_created += questions_created

                    print(f"  Total questions created for {subject.name}: {subject_questions_created}")
                    total_questions_created += subject_questions_created

                except Subject.DoesNotExist:
                    print(f"  ! Subject {subject_name} not found for {class_level.name}")

        print(f"\nTotal questions created: {total_questions_created}")
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting to populate quiz questions...")
    success = main()

    if success:
        print("Successfully populated quiz questions!")
    else:
        print("Failed to populate quiz questions.")
