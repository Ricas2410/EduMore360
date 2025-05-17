import random
from django.core.management.base import BaseCommand
from django.db import transaction
from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from quiz.models import Question, QuestionChoice, ShortAnswer, Quiz


class Command(BaseCommand):
    help = 'Add sample quiz questions for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding sample quiz questions...'))

        # Add topics if they don't exist
        self.add_topics()

        # Add questions for US Curriculum - Grade 5 - English - Noun
        self.add_us_grade5_english_noun_questions()

        # Add questions for US Curriculum - Grade 3 - Mathematics - Addition and Subtraction
        self.add_us_grade3_math_questions()

        # Add questions for Ghana Curriculum - Primary 4 - Science - Living Things
        self.add_ghana_primary4_science_questions()

        # Create quizzes for each topic
        self.create_topic_quizzes()

        self.stdout.write(self.style.SUCCESS('Successfully added sample quiz questions!'))

    def add_topics(self):
        """Add topics if they don't exist"""
        # US Curriculum - Grade 3 - Mathematics - Addition and Subtraction
        us_curriculum = Curriculum.objects.get(code='US')
        grade3 = ClassLevel.objects.get(curriculum=us_curriculum, name='Grade 3')
        math_subject = Subject.objects.get(curriculum=us_curriculum, class_level=grade3, name='Mathematics')

        Topic.objects.get_or_create(
            name='Addition and Subtraction',
            subject=math_subject,
            defaults={
                'description': 'Addition and subtraction of numbers up to 1000',
                'order': 1,
                'is_active': True
            }
        )

        # Ghana Curriculum - Primary 4 - Science - Living Things
        gh_curriculum = Curriculum.objects.get(code='GH')
        primary4 = ClassLevel.objects.get(curriculum=gh_curriculum, name='Primary 4')
        science_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=primary4, name='Science')

        Topic.objects.get_or_create(
            name='Living Things',
            subject=science_subject,
            defaults={
                'description': 'Study of plants and animals',
                'order': 1,
                'is_active': True
            }
        )

    def add_us_grade5_english_noun_questions(self):
        """Add questions for US Curriculum - Grade 5 - English - Noun"""
        us_curriculum = Curriculum.objects.get(code='US')
        grade5 = ClassLevel.objects.get(curriculum=us_curriculum, name='Grade 5')
        english_subject = Subject.objects.get(curriculum=us_curriculum, class_level=grade5, name='English')
        noun_topic = Topic.objects.get(subject=english_subject, name='Noun')

        # Multiple choice questions
        noun_mc_questions = [
            {
                'text': 'Which of the following is a proper noun?',
                'choices': [
                    {'text': 'New York', 'is_correct': True},
                    {'text': 'city', 'is_correct': False},
                    {'text': 'book', 'is_correct': False},
                    {'text': 'teacher', 'is_correct': False},
                ],
                'explanation': 'Proper nouns are specific names of people, places, or things and are always capitalized.'
            },
            {
                'text': 'Which sentence contains a collective noun?',
                'choices': [
                    {'text': 'The team won the championship.', 'is_correct': True},
                    {'text': 'She bought a new car.', 'is_correct': False},
                    {'text': 'The dog barked loudly.', 'is_correct': False},
                    {'text': 'He wrote a letter.', 'is_correct': False},
                ],
                'explanation': 'Collective nouns refer to groups of people or things, such as "team," "family," "flock," etc.'
            },
            {
                'text': 'Which of the following is an abstract noun?',
                'choices': [
                    {'text': 'Happiness', 'is_correct': True},
                    {'text': 'Table', 'is_correct': False},
                    {'text': 'Dog', 'is_correct': False},
                    {'text': 'Mountain', 'is_correct': False},
                ],
                'explanation': 'Abstract nouns represent ideas, qualities, or states that cannot be seen or touched, such as "happiness," "love," "courage," etc.'
            },
        ]

        # Short answer questions
        noun_sa_questions = [
            {
                'text': 'Write a proper noun for a famous city.',
                'answers': ['New York', 'London', 'Paris', 'Tokyo', 'Beijing', 'Rome', 'Cairo', 'Sydney'],
                'explanation': 'Proper nouns are specific names of people, places, or things and are always capitalized.'
            },
            {
                'text': 'What is a collective noun for a group of lions?',
                'answers': ['pride'],
                'explanation': 'A group of lions is called a "pride."'
            },
        ]

        # Add multiple choice questions
        for q_data in noun_mc_questions:
            with transaction.atomic():
                # Create the question without HTML
                question = Question(
                    text=q_data['text'],
                    question_type='multiple_choice',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=us_curriculum,
                    class_level=grade5,
                    subject=english_subject,
                    topic=noun_topic,
                    is_active=True,
                    is_premium=False
                )
                # Save directly to the database to bypass SummernoteTextField processing
                question.save()

                for choice_data in q_data['choices']:
                    QuestionChoice.objects.create(
                        question=question,
                        text=choice_data['text'],
                        is_correct=choice_data['is_correct']
                    )

        # Add short answer questions
        for q_data in noun_sa_questions:
            with transaction.atomic():
                # Create the question without HTML
                question = Question(
                    text=q_data['text'],
                    question_type='short_answer',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=us_curriculum,
                    class_level=grade5,
                    subject=english_subject,
                    topic=noun_topic,
                    is_active=True,
                    is_premium=False
                )
                # Save directly to the database to bypass SummernoteTextField processing
                question.save()

                for answer in q_data['answers']:
                    ShortAnswer.objects.create(
                        question=question,
                        text=answer
                    )

    def add_us_grade3_math_questions(self):
        """Add questions for US Curriculum - Grade 3 - Mathematics - Addition and Subtraction"""
        us_curriculum = Curriculum.objects.get(code='US')
        grade3 = ClassLevel.objects.get(curriculum=us_curriculum, name='Grade 3')
        math_subject = Subject.objects.get(curriculum=us_curriculum, class_level=grade3, name='Mathematics')
        addition_topic = Topic.objects.get(subject=math_subject, name='Addition and Subtraction')

        # Multiple choice questions
        math_mc_questions = [
            {
                'text': 'What is 245 + 367?',
                'choices': [
                    {'text': '612', 'is_correct': True},
                    {'text': '602', 'is_correct': False},
                    {'text': '712', 'is_correct': False},
                    {'text': '512', 'is_correct': False},
                ],
                'explanation': '245 + 367 = 612. You can solve this by adding the ones place (5 + 7 = 12, carry the 1), then the tens place (4 + 6 + 1 = 11, carry the 1), and finally the hundreds place (2 + 3 + 1 = 6).'
            },
            {
                'text': 'What is 523 - 178?',
                'choices': [
                    {'text': '345', 'is_correct': True},
                    {'text': '355', 'is_correct': False},
                    {'text': '335', 'is_correct': False},
                    {'text': '445', 'is_correct': False},
                ],
                'explanation': '523 - 178 = 345. You can solve this by subtracting the ones place (3 - 8 requires borrowing, so it becomes 13 - 8 = 5), then the tens place (1 - 7 requires borrowing, so it becomes 11 - 7 = 4), and finally the hundreds place (4 - 1 = 3).'
            },
            {
                'text': 'John had 342 marbles. He gave 127 marbles to his friend. How many marbles does John have now?',
                'choices': [
                    {'text': '215', 'is_correct': True},
                    {'text': '225', 'is_correct': False},
                    {'text': '205', 'is_correct': False},
                    {'text': '235', 'is_correct': False},
                ],
                'explanation': 'To find how many marbles John has left, we need to subtract: 342 - 127 = 215 marbles.'
            },
        ]

        # Short answer questions
        math_sa_questions = [
            {
                'text': 'What is 456 + 289?',
                'answers': ['745'],
                'explanation': '456 + 289 = 745. You can solve this by adding the ones place (6 + 9 = 15, carry the 1), then the tens place (5 + 8 + 1 = 14, carry the 1), and finally the hundreds place (4 + 2 + 1 = 7).'
            },
            {
                'text': 'What is 700 - 356?',
                'answers': ['344'],
                'explanation': '700 - 356 = 344. You can solve this by subtracting the ones place (0 - 6 requires borrowing, so it becomes 10 - 6 = 4), then the tens place (9 - 5 = 4), and finally the hundreds place (6 - 3 = 3).'
            },
        ]

        # Add multiple choice questions
        for q_data in math_mc_questions:
            with transaction.atomic():
                # Create the question without HTML
                question = Question(
                    text=q_data['text'],
                    question_type='multiple_choice',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=us_curriculum,
                    class_level=grade3,
                    subject=math_subject,
                    topic=addition_topic,
                    is_active=True,
                    is_premium=False
                )
                # Save directly to the database to bypass SummernoteTextField processing
                question.save()

                for choice_data in q_data['choices']:
                    QuestionChoice.objects.create(
                        question=question,
                        text=choice_data['text'],
                        is_correct=choice_data['is_correct']
                    )

        # Add short answer questions
        for q_data in math_sa_questions:
            with transaction.atomic():
                # Create the question without HTML
                question = Question(
                    text=q_data['text'],
                    question_type='short_answer',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=us_curriculum,
                    class_level=grade3,
                    subject=math_subject,
                    topic=addition_topic,
                    is_active=True,
                    is_premium=False
                )
                # Save directly to the database to bypass SummernoteTextField processing
                question.save()

                for answer in q_data['answers']:
                    ShortAnswer.objects.create(
                        question=question,
                        text=answer
                    )

    def add_ghana_primary4_science_questions(self):
        """Add questions for Ghana Curriculum - Primary 4 - Science - Living Things"""
        gh_curriculum = Curriculum.objects.get(code='GH')
        primary4 = ClassLevel.objects.get(curriculum=gh_curriculum, name='Primary 4')
        science_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=primary4, name='Science')
        living_things_topic = Topic.objects.get(subject=science_subject, name='Living Things')

        # Multiple choice questions
        science_mc_questions = [
            {
                'text': 'Which of the following is NOT a living thing?',
                'choices': [
                    {'text': 'Rock', 'is_correct': True},
                    {'text': 'Tree', 'is_correct': False},
                    {'text': 'Fish', 'is_correct': False},
                    {'text': 'Mushroom', 'is_correct': False},
                ],
                'explanation': 'Living things have certain characteristics such as the ability to grow, reproduce, respond to stimuli, and require energy. Rocks do not have these characteristics and are therefore not living things.'
            },
            {
                'text': 'Which of the following is a characteristic of living things?',
                'choices': [
                    {'text': 'They can reproduce', 'is_correct': True},
                    {'text': 'They are all green in color', 'is_correct': False},
                    {'text': 'They cannot move', 'is_correct': False},
                    {'text': 'They do not need water', 'is_correct': False},
                ],
                'explanation': 'Reproduction is a key characteristic of living things. Not all living things are green, many can move, and all living things need water to survive.'
            },
            {
                'text': 'Plants make their own food through a process called:',
                'choices': [
                    {'text': 'Photosynthesis', 'is_correct': True},
                    {'text': 'Respiration', 'is_correct': False},
                    {'text': 'Digestion', 'is_correct': False},
                    {'text': 'Transpiration', 'is_correct': False},
                ],
                'explanation': 'Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar.'
            },
        ]

        # Short answer questions
        science_sa_questions = [
            {
                'text': 'Name one way plants and animals are different.',
                'answers': ['Plants make their own food', 'Plants cannot move from place to place', 'Animals can move', 'Animals cannot make their own food', 'Plants have cell walls'],
                'explanation': 'Plants and animals differ in several ways: plants make their own food through photosynthesis while animals consume other organisms; plants generally cannot move from place to place while most animals can; plants have cell walls while animal cells do not.'
            },
            {
                'text': 'What gas do plants release during photosynthesis?',
                'answers': ['oxygen', 'o2'],
                'explanation': 'During photosynthesis, plants take in carbon dioxide and release oxygen as a byproduct.'
            },
        ]

        # Add multiple choice questions
        for q_data in science_mc_questions:
            with transaction.atomic():
                # Create the question without HTML
                question = Question(
                    text=q_data['text'],
                    question_type='multiple_choice',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=gh_curriculum,
                    class_level=primary4,
                    subject=science_subject,
                    topic=living_things_topic,
                    is_active=True,
                    is_premium=False
                )
                # Save directly to the database to bypass SummernoteTextField processing
                question.save()

                for choice_data in q_data['choices']:
                    QuestionChoice.objects.create(
                        question=question,
                        text=choice_data['text'],
                        is_correct=choice_data['is_correct']
                    )

        # Add short answer questions
        for q_data in science_sa_questions:
            with transaction.atomic():
                # Create the question without HTML
                question = Question(
                    text=q_data['text'],
                    question_type='short_answer',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=gh_curriculum,
                    class_level=primary4,
                    subject=science_subject,
                    topic=living_things_topic,
                    is_active=True,
                    is_premium=False
                )
                # Save directly to the database to bypass SummernoteTextField processing
                question.save()

                for answer in q_data['answers']:
                    ShortAnswer.objects.create(
                        question=question,
                        text=answer
                    )

    def create_topic_quizzes(self):
        """Create quizzes for each topic"""
        # US Curriculum - Grade 5 - English - Noun
        us_curriculum = Curriculum.objects.get(code='US')
        grade5 = ClassLevel.objects.get(curriculum=us_curriculum, name='Grade 5')
        english_subject = Subject.objects.get(curriculum=us_curriculum, class_level=grade5, name='English')
        noun_topic = Topic.objects.get(subject=english_subject, name='Noun')

        Quiz.objects.get_or_create(
            title='Nouns Quiz',
            quiz_type='topic',
            curriculum=us_curriculum,
            class_level=grade5,
            subject=english_subject,
            topic=noun_topic,
            defaults={
                'description': 'Test your knowledge of nouns',
                'question_count': 5,
                'per_question_time': 30,
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 70,
                'is_active': True,
            }
        )

        # US Curriculum - Grade 3 - Mathematics - Addition and Subtraction
        grade3 = ClassLevel.objects.get(curriculum=us_curriculum, name='Grade 3')
        math_subject = Subject.objects.get(curriculum=us_curriculum, class_level=grade3, name='Mathematics')
        addition_topic = Topic.objects.get(subject=math_subject, name='Addition and Subtraction')

        Quiz.objects.get_or_create(
            title='Addition and Subtraction Quiz',
            quiz_type='topic',
            curriculum=us_curriculum,
            class_level=grade3,
            subject=math_subject,
            topic=addition_topic,
            defaults={
                'description': 'Practice addition and subtraction of numbers up to 1000',
                'question_count': 5,
                'per_question_time': 30,
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 70,
                'is_active': True,
            }
        )

        # Ghana Curriculum - Primary 4 - Science - Living Things
        gh_curriculum = Curriculum.objects.get(code='GH')
        primary4 = ClassLevel.objects.get(curriculum=gh_curriculum, name='Primary 4')
        science_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=primary4, name='Science')
        living_things_topic = Topic.objects.get(subject=science_subject, name='Living Things')

        Quiz.objects.get_or_create(
            title='Living Things Quiz',
            quiz_type='topic',
            curriculum=gh_curriculum,
            class_level=primary4,
            subject=science_subject,
            topic=living_things_topic,
            defaults={
                'description': 'Test your knowledge of living things',
                'question_count': 5,
                'per_question_time': 30,
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 70,
                'is_active': True,
            }
        )
