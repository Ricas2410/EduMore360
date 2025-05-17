"""
Script to add a final set of quiz questions to SHS2 and Primary 6 for the subjects:
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

# Define final set of questions for each topic
def get_final_questions(subject, class_level, topic):
    """Generate a final set of questions for a specific topic."""
    questions = []
    
    # ICT Questions
    if subject == 'ICT':
        if class_level == 'SHS 2':
            if 'Database' in topic:
                questions.extend([
                    {
                        'text': 'Which SQL statement is used to extract data from a database?',
                        'choices': [
                            {'text': 'SELECT', 'is_correct': True},
                            {'text': 'EXTRACT', 'is_correct': False},
                            {'text': 'CAPTURE', 'is_correct': False},
                            {'text': 'OBTAIN', 'is_correct': False}
                        ],
                        'explanation': 'The SELECT statement is used to select data from a database. The data returned is stored in a result table, called the result-set.'
                    },
                    {
                        'text': 'What is a foreign key in a relational database?',
                        'choices': [
                            {'text': 'A key used to encrypt data', 'is_correct': False},
                            {'text': 'A field that uniquely identifies each record in a table', 'is_correct': False},
                            {'text': 'A field that links to the primary key of another table', 'is_correct': True},
                            {'text': 'A key imported from another database system', 'is_correct': False}
                        ],
                        'explanation': 'A foreign key is a field (or collection of fields) in one table that refers to the primary key in another table. It is used to establish and enforce a link between the data in two tables.'
                    }
                ])
            elif 'Programming' in topic:
                questions.extend([
                    {
                        'text': 'What is the purpose of a function in programming?',
                        'choices': [
                            {'text': 'To format the code to look better', 'is_correct': False},
                            {'text': 'To organize code into reusable blocks', 'is_correct': True},
                            {'text': 'To make the program run faster', 'is_correct': False},
                            {'text': 'To connect to external devices', 'is_correct': False}
                        ],
                        'explanation': 'Functions are blocks of code that perform a specific task and can be reused throughout a program. They help in organizing code, reducing repetition, and making programs more modular and maintainable.'
                    },
                    {
                        'text': 'What is an algorithm in computer programming?',
                        'choices': [
                            {'text': 'A programming language', 'is_correct': False},
                            {'text': 'A step-by-step procedure for solving a problem', 'is_correct': True},
                            {'text': 'A type of computer hardware', 'is_correct': False},
                            {'text': 'A method to encrypt data', 'is_correct': False}
                        ],
                        'explanation': 'An algorithm is a step-by-step procedure or a set of rules for solving a specific problem or accomplishing a defined task in a finite number of steps.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Introduction to Computers' in topic:
                questions.extend([
                    {
                        'text': 'What is the main function of a computer\'s memory (RAM)?',
                        'choices': [
                            {'text': 'To permanently store files', 'is_correct': False},
                            {'text': 'To temporarily store data that the CPU is using', 'is_correct': True},
                            {'text': 'To connect to the internet', 'is_correct': False},
                            {'text': 'To display images on the screen', 'is_correct': False}
                        ],
                        'explanation': 'RAM (Random Access Memory) temporarily stores data that the CPU is actively using. It allows for quick access to this data but loses its contents when the computer is turned off.'
                    },
                    {
                        'text': 'Which of these is NOT a type of computer?',
                        'choices': [
                            {'text': 'Desktop', 'is_correct': False},
                            {'text': 'Laptop', 'is_correct': False},
                            {'text': 'Tablet', 'is_correct': False},
                            {'text': 'Microphone', 'is_correct': True}
                        ],
                        'explanation': 'A microphone is an input device used to capture sound, not a type of computer. Desktops, laptops, and tablets are all types of computers.'
                    }
                ])
    
    # English Questions
    elif subject == 'English':
        if class_level == 'SHS 2':
            if 'Literature' in topic:
                questions.extend([
                    {
                        'text': 'What is the term for a play on words that exploits multiple meanings?',
                        'choices': [
                            {'text': 'Metaphor', 'is_correct': False},
                            {'text': 'Pun', 'is_correct': True},
                            {'text': 'Simile', 'is_correct': False},
                            {'text': 'Alliteration', 'is_correct': False}
                        ],
                        'explanation': 'A pun is a play on words that exploits multiple meanings of a term, or replaces it with a similar-sounding word for humorous or rhetorical effect.'
                    },
                    {
                        'text': 'Which of these is an example of personification?',
                        'choices': [
                            {'text': 'He runs as fast as a cheetah', 'is_correct': False},
                            {'text': 'The stars are like diamonds in the sky', 'is_correct': False},
                            {'text': 'The wind whispered through the trees', 'is_correct': True},
                            {'text': 'The room was very quiet', 'is_correct': False}
                        ],
                        'explanation': 'Personification is giving human qualities to non-human things. In "The wind whispered through the trees," whispering is a human action attributed to the wind.'
                    }
                ])
            elif 'Writing Skills' in topic:
                questions.extend([
                    {
                        'text': 'What is the purpose of a thesis statement in an essay?',
                        'choices': [
                            {'text': 'To summarize the entire essay', 'is_correct': False},
                            {'text': 'To state the main idea or argument of the essay', 'is_correct': True},
                            {'text': 'To introduce the topic of the essay', 'is_correct': False},
                            {'text': 'To conclude the essay', 'is_correct': False}
                        ],
                        'explanation': 'A thesis statement clearly states the main idea or argument of an essay. It tells the reader what to expect and is usually placed at the end of the introduction.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Reading and Comprehension' in topic:
                questions.extend([
                    {
                        'text': 'What is the main purpose of reading comprehension?',
                        'choices': [
                            {'text': 'To read as quickly as possible', 'is_correct': False},
                            {'text': 'To memorize the text word for word', 'is_correct': False},
                            {'text': 'To understand and interpret what is being read', 'is_correct': True},
                            {'text': 'To read aloud with proper pronunciation', 'is_correct': False}
                        ],
                        'explanation': 'Reading comprehension is the ability to understand, interpret, and analyze what you read. It involves making meaning from text rather than just recognizing words.'
                    }
                ])
    
    # Mathematics Questions
    elif subject == 'Mathematics':
        if class_level == 'SHS 2':
            if 'Algebra' in topic:
                questions.extend([
                    {
                        'text': 'Solve the equation: 3(x - 2) = 15',
                        'choices': [
                            {'text': 'x = 5', 'is_correct': False},
                            {'text': 'x = 7', 'is_correct': True},
                            {'text': 'x = 9', 'is_correct': False},
                            {'text': 'x = 11', 'is_correct': False}
                        ],
                        'explanation': 'To solve 3(x - 2) = 15, first distribute: 3x - 6 = 15. Then add 6 to both sides: 3x = 21. Finally, divide both sides by 3: x = 7.'
                    },
                    {
                        'text': 'What is the value of x in the equation 2x² - 8 = 0?',
                        'choices': [
                            {'text': 'x = 2', 'is_correct': True},
                            {'text': 'x = 4', 'is_correct': False},
                            {'text': 'x = -2', 'is_correct': True},
                            {'text': 'x = 8', 'is_correct': False}
                        ],
                        'explanation': 'To solve 2x² - 8 = 0, first divide by 2: x² - 4 = 0. Then add 4 to both sides: x² = 4. Taking the square root of both sides: x = ±2. So x = 2 or x = -2.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Numbers and Operations' in topic:
                questions.extend([
                    {
                        'text': 'What is the value of 24 ÷ 6 × 2?',
                        'choices': [
                            {'text': '4', 'is_correct': False},
                            {'text': '8', 'is_correct': True},
                            {'text': '12', 'is_correct': False},
                            {'text': '16', 'is_correct': False}
                        ],
                        'explanation': 'Following the order of operations (division and multiplication from left to right), first calculate 24 ÷ 6 = 4, then 4 × 2 = 8.'
                    }
                ])
    
    # Science Questions
    elif subject == 'Science':
        if class_level == 'SHS 2':
            if 'Physics' in topic:
                questions.extend([
                    {
                        'text': 'What is Newton\'s First Law of Motion?',
                        'choices': [
                            {'text': 'Force equals mass times acceleration', 'is_correct': False},
                            {'text': 'For every action, there is an equal and opposite reaction', 'is_correct': False},
                            {'text': 'An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force', 'is_correct': True},
                            {'text': 'Energy cannot be created or destroyed, only transformed', 'is_correct': False}
                        ],
                        'explanation': 'Newton\'s First Law of Motion, also known as the Law of Inertia, states that an object at rest stays at rest, and an object in motion stays in motion with the same speed and direction unless acted upon by an external force.'
                    }
                ])
            elif 'Chemistry' in topic:
                questions.extend([
                    {
                        'text': 'What is the pH of a neutral solution?',
                        'choices': [
                            {'text': '0', 'is_correct': False},
                            {'text': '7', 'is_correct': True},
                            {'text': '10', 'is_correct': False},
                            {'text': '14', 'is_correct': False}
                        ],
                        'explanation': 'The pH scale ranges from 0 to 14. A neutral solution (neither acidic nor basic) has a pH of 7. Values below 7 indicate acidity, while values above 7 indicate alkalinity.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Human Body' in topic:
                questions.extend([
                    {
                        'text': 'Which organ is responsible for pumping blood throughout the body?',
                        'choices': [
                            {'text': 'Lungs', 'is_correct': False},
                            {'text': 'Brain', 'is_correct': False},
                            {'text': 'Heart', 'is_correct': True},
                            {'text': 'Liver', 'is_correct': False}
                        ],
                        'explanation': 'The heart is a muscular organ that pumps blood throughout the body via the circulatory system, supplying oxygen and nutrients to tissues and removing carbon dioxide and other wastes.'
                    }
                ])
    
    # Social Studies Questions
    elif subject == 'Social Studies':
        if class_level == 'SHS 2':
            if 'Cultural Practices' in topic:
                questions.extend([
                    {
                        'text': 'Which of these is a traditional Ghanaian festival?',
                        'choices': [
                            {'text': 'Diwali', 'is_correct': False},
                            {'text': 'Homowo', 'is_correct': True},
                            {'text': 'Carnival', 'is_correct': False},
                            {'text': 'Thanksgiving', 'is_correct': False}
                        ],
                        'explanation': 'Homowo is a traditional harvest festival celebrated by the Ga people of Ghana. It is celebrated to remember a famine that once happened in their history.'
                    }
                ])
        elif class_level == 'Primary 6':
            if 'Map Reading' in topic:
                questions.extend([
                    {
                        'text': 'What does a compass rose on a map show?',
                        'choices': [
                            {'text': 'The scale of the map', 'is_correct': False},
                            {'text': 'The elevation of the land', 'is_correct': False},
                            {'text': 'The cardinal directions (North, South, East, West)', 'is_correct': True},
                            {'text': 'The population density', 'is_correct': False}
                        ],
                        'explanation': 'A compass rose is a figure on a map that shows the cardinal directions (North, South, East, and West) and helps readers orient themselves.'
                    }
                ])
    
    # Generate generic questions if we don't have enough specific ones
    while len(questions) < 5:  # Generate 5 questions per topic
        question_num = len(questions) + 1
        questions.append({
            'text': f'Final question {question_num} for {topic} in {subject} ({class_level})',
            'choices': [
                {'text': f'Correct answer for final question {question_num}', 'is_correct': True},
                {'text': f'Wrong answer 1 for final question {question_num}', 'is_correct': False},
                {'text': f'Wrong answer 2 for final question {question_num}', 'is_correct': False},
                {'text': f'Wrong answer 3 for final question {question_num}', 'is_correct': False}
            ],
            'explanation': f'This is an explanation for final question {question_num}.'
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
    """Main function to add final set of quiz questions."""
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
                            questions_data = get_final_questions(subject_name, class_level_name, topic.name)
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
    print("Starting to add final set of quiz questions...")
    success = main()
    
    if success:
        print("Successfully added final set of quiz questions!")
    else:
        print("Failed to add final set of quiz questions.")
