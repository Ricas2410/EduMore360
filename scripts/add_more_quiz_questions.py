"""
Script to add more quiz questions to SHS2 and Primary 6 for the subjects:
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

# Define additional questions for each topic
def get_additional_questions(subject, class_level, topic):
    """Generate additional questions for a specific topic."""
    questions = []
    
    # ICT Questions
    if subject == 'ICT':
        if class_level == 'SHS 2':
            if 'Database' in topic:
                questions.extend([
                    {
                        'text': 'Which of the following is a primary key constraint?',
                        'choices': [
                            {'text': 'It ensures that a column cannot have NULL values', 'is_correct': False},
                            {'text': 'It ensures that a column or set of columns uniquely identifies each record', 'is_correct': True},
                            {'text': 'It ensures that values in a column match values in another table', 'is_correct': False},
                            {'text': 'It ensures that a column can only contain specific values', 'is_correct': False}
                        ],
                        'explanation': 'A primary key constraint ensures that a column or set of columns uniquely identifies each record in a table and cannot contain NULL values.'
                    },
                    {
                        'text': 'What is normalization in database design?',
                        'choices': [
                            {'text': 'The process of organizing data to reduce redundancy', 'is_correct': True},
                            {'text': 'The process of adding more tables to a database', 'is_correct': False},
                            {'text': 'The process of converting data to binary format', 'is_correct': False},
                            {'text': 'The process of securing a database with passwords', 'is_correct': False}
                        ],
                        'explanation': 'Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity by dividing large tables into smaller, related tables.'
                    }
                ])
            elif 'Programming' in topic:
                questions.extend([
                    {
                        'text': 'What is the difference between a while loop and a for loop?',
                        'choices': [
                            {'text': 'A while loop executes once, a for loop executes multiple times', 'is_correct': False},
                            {'text': 'A while loop is used for strings, a for loop is used for numbers', 'is_correct': False},
                            {'text': 'A while loop checks a condition before each iteration, a for loop iterates over a sequence', 'is_correct': True},
                            {'text': 'There is no difference between them', 'is_correct': False}
                        ],
                        'explanation': 'A while loop continues to execute as long as a condition is true, while a for loop is typically used to iterate over a sequence (like a list or range) a specific number of times.'
                    },
                    {
                        'text': 'What is an array in programming?',
                        'choices': [
                            {'text': 'A data structure that stores a collection of elements', 'is_correct': True},
                            {'text': 'A type of loop that repeats code', 'is_correct': False},
                            {'text': 'A function that performs mathematical operations', 'is_correct': False},
                            {'text': 'A method to connect to a database', 'is_correct': False}
                        ],
                        'explanation': 'An array is a data structure that stores a collection of elements (values or variables), typically of the same type, in contiguous memory locations.'
                    }
                ])
            elif 'Networking' in topic:
                questions.extend([
                    {
                        'text': 'What does HTTP stand for?',
                        'choices': [
                            {'text': 'Hypertext Transfer Protocol', 'is_correct': True},
                            {'text': 'High Tech Transfer Protocol', 'is_correct': False},
                            {'text': 'Hypertext Technical Process', 'is_correct': False},
                            {'text': 'Home Transfer Protocol', 'is_correct': False}
                        ],
                        'explanation': 'HTTP (Hypertext Transfer Protocol) is the foundation of data communication on the World Wide Web, used for transferring web pages and other resources.'
                    },
                    {
                        'text': 'Which of the following is NOT a network topology?',
                        'choices': [
                            {'text': 'Star', 'is_correct': False},
                            {'text': 'Ring', 'is_correct': False},
                            {'text': 'Pyramid', 'is_correct': True},
                            {'text': 'Bus', 'is_correct': False}
                        ],
                        'explanation': 'Pyramid is not a standard network topology. Common network topologies include Star, Ring, Bus, and Mesh.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Introduction to Computers' in topic:
                questions.extend([
                    {
                        'text': 'Which of these is an example of an operating system?',
                        'choices': [
                            {'text': 'Microsoft Word', 'is_correct': False},
                            {'text': 'Windows', 'is_correct': True},
                            {'text': 'Google Chrome', 'is_correct': False},
                            {'text': 'Printer', 'is_correct': False}
                        ],
                        'explanation': 'Windows is an operating system developed by Microsoft. Operating systems manage computer hardware and software resources.'
                    },
                    {
                        'text': 'What is the function of a mouse?',
                        'choices': [
                            {'text': 'To display information', 'is_correct': False},
                            {'text': 'To print documents', 'is_correct': False},
                            {'text': 'To point to and select items on the screen', 'is_correct': True},
                            {'text': 'To store data permanently', 'is_correct': False}
                        ],
                        'explanation': 'A mouse is a pointing device that allows users to point to and select items on a computer screen.'
                    }
                ])
    
    # English Questions
    elif subject == 'English':
        if class_level == 'SHS 2':
            if 'Grammar' in topic:
                questions.extend([
                    {
                        'text': 'Which of the following sentences contains a split infinitive?',
                        'choices': [
                            {'text': 'She quickly ran to the store.', 'is_correct': False},
                            {'text': 'He decided to quickly run to the store.', 'is_correct': True},
                            {'text': 'They were running quickly to the store.', 'is_correct': False},
                            {'text': 'We ran to the store quickly.', 'is_correct': False}
                        ],
                        'explanation': 'A split infinitive occurs when a word (usually an adverb) is placed between "to" and the verb. In "to quickly run," the adverb "quickly" splits the infinitive "to run."'
                    },
                    {
                        'text': 'Which sentence uses the subjunctive mood correctly?',
                        'choices': [
                            {'text': 'I wish I was taller.', 'is_correct': False},
                            {'text': 'I wish I were taller.', 'is_correct': True},
                            {'text': 'I wish I am taller.', 'is_correct': False},
                            {'text': 'I wish I will be taller.', 'is_correct': False}
                        ],
                        'explanation': 'The subjunctive mood is used to express wishes, hypothetical situations, or suggestions. "I wish I were taller" correctly uses the subjunctive form "were" instead of "was."'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Grammar' in topic:
                questions.extend([
                    {
                        'text': 'Which of the following is an example of a compound sentence?',
                        'choices': [
                            {'text': 'The boy ran.', 'is_correct': False},
                            {'text': 'The boy ran and the girl walked.', 'is_correct': True},
                            {'text': 'The boy, who was tall, ran.', 'is_correct': False},
                            {'text': 'Running quickly, the boy arrived first.', 'is_correct': False}
                        ],
                        'explanation': 'A compound sentence contains two or more independent clauses joined by a conjunction. "The boy ran and the girl walked" has two independent clauses joined by "and."'
                    }
                ])
    
    # Mathematics Questions
    elif subject == 'Mathematics':
        if class_level == 'SHS 2':
            if 'Trigonometry' in topic:
                questions.extend([
                    {
                        'text': 'What is the value of cos(60°)?',
                        'choices': [
                            {'text': '0', 'is_correct': False},
                            {'text': '0.5', 'is_correct': True},
                            {'text': '1', 'is_correct': False},
                            {'text': '√3/2', 'is_correct': False}
                        ],
                        'explanation': 'The value of cos(60°) is 0.5 or 1/2.'
                    },
                    {
                        'text': 'In a right-angled triangle, if one angle is 30°, what is the other acute angle?',
                        'choices': [
                            {'text': '30°', 'is_correct': False},
                            {'text': '45°', 'is_correct': False},
                            {'text': '60°', 'is_correct': True},
                            {'text': '90°', 'is_correct': False}
                        ],
                        'explanation': 'In a right-angled triangle, the three angles sum to 180°. If one angle is 90° (the right angle) and another is 30°, then the third angle must be 60° (180° - 90° - 30° = 60°).'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Fractions' in topic:
                questions.extend([
                    {
                        'text': 'What is 2/3 of 18?',
                        'choices': [
                            {'text': '6', 'is_correct': False},
                            {'text': '9', 'is_correct': False},
                            {'text': '12', 'is_correct': True},
                            {'text': '15', 'is_correct': False}
                        ],
                        'explanation': 'To find 2/3 of 18, multiply 18 by 2/3: 18 × 2/3 = 36/3 = 12.'
                    }
                ])
    
    # Science Questions
    elif subject == 'Science':
        if class_level == 'SHS 2':
            if 'Biology' in topic:
                questions.extend([
                    {
                        'text': 'What is the process by which plants make their own food called?',
                        'choices': [
                            {'text': 'Respiration', 'is_correct': False},
                            {'text': 'Photosynthesis', 'is_correct': True},
                            {'text': 'Transpiration', 'is_correct': False},
                            {'text': 'Digestion', 'is_correct': False}
                        ],
                        'explanation': 'Photosynthesis is the process by which green plants use sunlight, carbon dioxide, and water to create glucose (food) and oxygen.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Living Things' in topic:
                questions.extend([
                    {
                        'text': 'Which of these is an example of a mammal?',
                        'choices': [
                            {'text': 'Snake', 'is_correct': False},
                            {'text': 'Fish', 'is_correct': False},
                            {'text': 'Elephant', 'is_correct': True},
                            {'text': 'Frog', 'is_correct': False}
                        ],
                        'explanation': 'Elephants are mammals. Mammals are warm-blooded animals that have hair or fur, give birth to live young, and produce milk for their babies.'
                    }
                ])
    
    # Social Studies Questions
    elif subject == 'Social Studies':
        if class_level == 'SHS 2':
            if 'Governance' in topic:
                questions.extend([
                    {
                        'text': 'How many regions are there in Ghana as of 2023?',
                        'choices': [
                            {'text': '10', 'is_correct': False},
                            {'text': '12', 'is_correct': False},
                            {'text': '16', 'is_correct': True},
                            {'text': '20', 'is_correct': False}
                        ],
                        'explanation': 'As of 2023, Ghana has 16 administrative regions following the creation of 6 new regions in 2019.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Our Nation Ghana' in topic:
                questions.extend([
                    {
                        'text': 'What is the capital city of Ghana?',
                        'choices': [
                            {'text': 'Kumasi', 'is_correct': False},
                            {'text': 'Tamale', 'is_correct': False},
                            {'text': 'Accra', 'is_correct': True},
                            {'text': 'Cape Coast', 'is_correct': False}
                        ],
                        'explanation': 'Accra is the capital city of Ghana and its largest city.'
                    }
                ])
    
    # Generate generic questions if we don't have enough specific ones
    while len(questions) < 5:  # Generate 5 questions per topic
        question_num = len(questions) + 1
        questions.append({
            'text': f'Additional question {question_num} for {topic} in {subject} ({class_level})',
            'choices': [
                {'text': f'Correct answer for additional question {question_num}', 'is_correct': True},
                {'text': f'Wrong answer 1 for additional question {question_num}', 'is_correct': False},
                {'text': f'Wrong answer 2 for additional question {question_num}', 'is_correct': False},
                {'text': f'Wrong answer 3 for additional question {question_num}', 'is_correct': False}
            ],
            'explanation': f'This is an explanation for additional question {question_num}.'
        })
    
    return questions

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

def main():
    """Main function to add more quiz questions."""
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
                    
                    # Get existing topics for this subject
                    topics = Topic.objects.filter(subject=subject)
                    
                    if topics.exists():
                        # Process each topic for this subject
                        subject_questions_created = 0
                        for topic in topics:
                            # Generate and create questions for this topic
                            questions_data = get_additional_questions(subject_name, class_level_name, topic.name)
                            questions_created = create_quiz_questions(ghana_curriculum, class_level, subject, topic, questions_data)
                            
                            print(f"    + Added {questions_created} questions for topic: {topic.name}")
                            subject_questions_created += questions_created
                        
                        print(f"  Total questions created for {subject.name}: {subject_questions_created}")
                        total_questions_created += subject_questions_created
                    else:
                        print(f"  ! No topics found for {subject.name}")
                    
                except Subject.DoesNotExist:
                    print(f"  ! Subject {subject_name} not found for {class_level.name}")
        
        print(f"\nTotal questions created: {total_questions_created}")
        return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting to add more quiz questions...")
    success = main()
    
    if success:
        print("Successfully added more quiz questions!")
    else:
        print("Failed to add more quiz questions.")
