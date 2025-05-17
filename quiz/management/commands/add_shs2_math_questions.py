import random
from django.core.management.base import BaseCommand
from django.db import transaction
from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from quiz.models import Question, QuestionChoice, ShortAnswer, Quiz


class Command(BaseCommand):
    help = 'Add sample quiz questions for Ghana SHS 2 Mathematics'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding SHS 2 Mathematics questions...'))
        
        # Add topic if it doesn't exist
        self.add_topic()
        
        # Add questions
        self.add_shs2_math_questions()
        
        # Create quiz
        self.create_quiz()
        
        self.stdout.write(self.style.SUCCESS('Successfully added SHS 2 Mathematics questions!'))
    
    def add_topic(self):
        """Add topic if it doesn't exist"""
        gh_curriculum = Curriculum.objects.get(code='GH')
        shs2 = ClassLevel.objects.get(curriculum=gh_curriculum, name='SHS 2')
        math_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=shs2, name='Mathematics')
        
        Topic.objects.get_or_create(
            name='Trigonometry',
            subject=math_subject,
            defaults={
                'description': 'Study of relationships between angles and sides of triangles',
                'order': 1,
                'is_active': True
            }
        )
    
    def add_shs2_math_questions(self):
        """Add questions for Ghana Curriculum - SHS 2 - Mathematics - Trigonometry"""
        gh_curriculum = Curriculum.objects.get(code='GH')
        shs2 = ClassLevel.objects.get(curriculum=gh_curriculum, name='SHS 2')
        math_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=shs2, name='Mathematics')
        trig_topic = Topic.objects.get(subject=math_subject, name='Trigonometry')
        
        # Multiple choice questions
        trig_mc_questions = [
            {
                'text': 'What is the value of sin(30°)?',
                'choices': [
                    {'text': '0.5', 'is_correct': True},
                    {'text': '0.866', 'is_correct': False},
                    {'text': '1', 'is_correct': False},
                    {'text': '0', 'is_correct': False},
                ],
                'explanation': 'sin(30°) = 1/2 = 0.5'
            },
            {
                'text': 'What is the value of cos(60°)?',
                'choices': [
                    {'text': '0.5', 'is_correct': True},
                    {'text': '0.866', 'is_correct': False},
                    {'text': '1', 'is_correct': False},
                    {'text': '0', 'is_correct': False},
                ],
                'explanation': 'cos(60°) = 1/2 = 0.5'
            },
            {
                'text': 'What is the value of tan(45°)?',
                'choices': [
                    {'text': '1', 'is_correct': True},
                    {'text': '0.5', 'is_correct': False},
                    {'text': '0', 'is_correct': False},
                    {'text': '√3', 'is_correct': False},
                ],
                'explanation': 'tan(45°) = 1'
            },
            {
                'text': 'In a right-angled triangle, if one angle is 30°, what is the other non-right angle?',
                'choices': [
                    {'text': '60°', 'is_correct': True},
                    {'text': '45°', 'is_correct': False},
                    {'text': '30°', 'is_correct': False},
                    {'text': '90°', 'is_correct': False},
                ],
                'explanation': 'In a triangle, the sum of all angles is 180°. If one angle is 90° (right angle) and another is 30°, then the third angle is 180° - 90° - 30° = 60°.'
            },
            {
                'text': 'Which of the following is the Pythagorean identity?',
                'choices': [
                    {'text': 'sin²θ + cos²θ = 1', 'is_correct': True},
                    {'text': 'sin²θ - cos²θ = 1', 'is_correct': False},
                    {'text': 'sin²θ + cos²θ = 0', 'is_correct': False},
                    {'text': 'sin²θ - cos²θ = 0', 'is_correct': False},
                ],
                'explanation': 'The Pythagorean identity is sin²θ + cos²θ = 1.'
            },
            {
                'text': 'If sin(θ) = 0.6, what is cos(θ)?',
                'choices': [
                    {'text': '0.8', 'is_correct': True},
                    {'text': '0.6', 'is_correct': False},
                    {'text': '0.36', 'is_correct': False},
                    {'text': '0.64', 'is_correct': False},
                ],
                'explanation': 'Using the Pythagorean identity sin²θ + cos²θ = 1, we get cos²θ = 1 - sin²θ = 1 - 0.6² = 1 - 0.36 = 0.64. Therefore, cos(θ) = √0.64 = 0.8.'
            },
            {
                'text': 'In a right-angled triangle, which side is opposite to the right angle?',
                'choices': [
                    {'text': 'Hypotenuse', 'is_correct': True},
                    {'text': 'Adjacent', 'is_correct': False},
                    {'text': 'Opposite', 'is_correct': False},
                    {'text': 'Base', 'is_correct': False},
                ],
                'explanation': 'The hypotenuse is the side opposite to the right angle in a right-angled triangle.'
            },
            {
                'text': 'What is the formula for the area of a triangle using sine?',
                'choices': [
                    {'text': 'A = (1/2)ab·sin(C)', 'is_correct': True},
                    {'text': 'A = ab·sin(C)', 'is_correct': False},
                    {'text': 'A = (1/2)ab·cos(C)', 'is_correct': False},
                    {'text': 'A = ab·cos(C)', 'is_correct': False},
                ],
                'explanation': 'The formula for the area of a triangle using sine is A = (1/2)ab·sin(C), where a and b are two sides of the triangle and C is the angle between them.'
            },
            {
                'text': 'What is the value of sin(90°)?',
                'choices': [
                    {'text': '1', 'is_correct': True},
                    {'text': '0', 'is_correct': False},
                    {'text': '0.5', 'is_correct': False},
                    {'text': 'undefined', 'is_correct': False},
                ],
                'explanation': 'sin(90°) = 1'
            },
            {
                'text': 'What is the value of cos(90°)?',
                'choices': [
                    {'text': '0', 'is_correct': True},
                    {'text': '1', 'is_correct': False},
                    {'text': '0.5', 'is_correct': False},
                    {'text': 'undefined', 'is_correct': False},
                ],
                'explanation': 'cos(90°) = 0'
            },
            {
                'text': 'What is the value of tan(90°)?',
                'choices': [
                    {'text': 'undefined', 'is_correct': True},
                    {'text': '0', 'is_correct': False},
                    {'text': '1', 'is_correct': False},
                    {'text': 'infinity', 'is_correct': False},
                ],
                'explanation': 'tan(90°) is undefined because tan(θ) = sin(θ)/cos(θ), and cos(90°) = 0. Division by zero is undefined.'
            },
            {
                'text': 'In a right-angled triangle, if the hypotenuse is 10 cm and one of the other sides is 6 cm, what is the length of the third side?',
                'choices': [
                    {'text': '8 cm', 'is_correct': True},
                    {'text': '4 cm', 'is_correct': False},
                    {'text': '6 cm', 'is_correct': False},
                    {'text': '10 cm', 'is_correct': False},
                ],
                'explanation': 'Using the Pythagorean theorem, a² + b² = c², where c is the hypotenuse. We have 10² = 6² + b², so b² = 10² - 6² = 100 - 36 = 64. Therefore, b = 8 cm.'
            },
            {
                'text': 'What is the relationship between sin(θ) and sin(180° - θ)?',
                'choices': [
                    {'text': 'sin(θ) = sin(180° - θ)', 'is_correct': True},
                    {'text': 'sin(θ) = -sin(180° - θ)', 'is_correct': False},
                    {'text': 'sin(θ) = cos(180° - θ)', 'is_correct': False},
                    {'text': 'sin(θ) = -cos(180° - θ)', 'is_correct': False},
                ],
                'explanation': 'sin(θ) = sin(180° - θ) is a trigonometric identity.'
            },
            {
                'text': 'What is the relationship between cos(θ) and cos(180° - θ)?',
                'choices': [
                    {'text': 'cos(θ) = -cos(180° - θ)', 'is_correct': True},
                    {'text': 'cos(θ) = cos(180° - θ)', 'is_correct': False},
                    {'text': 'cos(θ) = sin(180° - θ)', 'is_correct': False},
                    {'text': 'cos(θ) = -sin(180° - θ)', 'is_correct': False},
                ],
                'explanation': 'cos(θ) = -cos(180° - θ) is a trigonometric identity.'
            },
            {
                'text': 'What is the value of sin(-θ)?',
                'choices': [
                    {'text': '-sin(θ)', 'is_correct': True},
                    {'text': 'sin(θ)', 'is_correct': False},
                    {'text': 'cos(θ)', 'is_correct': False},
                    {'text': '-cos(θ)', 'is_correct': False},
                ],
                'explanation': 'sin(-θ) = -sin(θ) is a trigonometric identity.'
            },
            {
                'text': 'What is the value of cos(-θ)?',
                'choices': [
                    {'text': 'cos(θ)', 'is_correct': True},
                    {'text': '-cos(θ)', 'is_correct': False},
                    {'text': 'sin(θ)', 'is_correct': False},
                    {'text': '-sin(θ)', 'is_correct': False},
                ],
                'explanation': 'cos(-θ) = cos(θ) is a trigonometric identity.'
            },
            {
                'text': 'What is the value of sin(θ + 90°)?',
                'choices': [
                    {'text': 'cos(θ)', 'is_correct': True},
                    {'text': '-cos(θ)', 'is_correct': False},
                    {'text': 'sin(θ)', 'is_correct': False},
                    {'text': '-sin(θ)', 'is_correct': False},
                ],
                'explanation': 'sin(θ + 90°) = cos(θ) is a trigonometric identity.'
            },
            {
                'text': 'What is the value of cos(θ + 90°)?',
                'choices': [
                    {'text': '-sin(θ)', 'is_correct': True},
                    {'text': 'sin(θ)', 'is_correct': False},
                    {'text': 'cos(θ)', 'is_correct': False},
                    {'text': '-cos(θ)', 'is_correct': False},
                ],
                'explanation': 'cos(θ + 90°) = -sin(θ) is a trigonometric identity.'
            },
            {
                'text': 'If sin(θ) = 3/5, what is the value of cos(θ)?',
                'choices': [
                    {'text': '4/5', 'is_correct': True},
                    {'text': '3/5', 'is_correct': False},
                    {'text': '5/3', 'is_correct': False},
                    {'text': '5/4', 'is_correct': False},
                ],
                'explanation': 'Using the Pythagorean identity sin²θ + cos²θ = 1, we get cos²θ = 1 - sin²θ = 1 - (3/5)² = 1 - 9/25 = 16/25. Therefore, cos(θ) = 4/5.'
            },
            {
                'text': 'In a right-angled triangle, which trigonometric ratio is equal to the opposite side divided by the hypotenuse?',
                'choices': [
                    {'text': 'sine', 'is_correct': True},
                    {'text': 'cosine', 'is_correct': False},
                    {'text': 'tangent', 'is_correct': False},
                    {'text': 'secant', 'is_correct': False},
                ],
                'explanation': 'The sine of an angle in a right-angled triangle is equal to the opposite side divided by the hypotenuse.'
            },
        ]
        
        # Short answer questions
        trig_sa_questions = [
            {
                'text': 'What is the value of sin(45°) in decimal form?',
                'answers': ['0.7071', '0.707', '0.71', '1/√2', '0.7'],
                'explanation': 'sin(45°) = 1/√2 ≈ 0.7071'
            },
            {
                'text': 'What is the formula for the law of sines?',
                'answers': ['a/sin(A) = b/sin(B) = c/sin(C)', 'sin(A)/a = sin(B)/b = sin(C)/c'],
                'explanation': 'The law of sines states that the ratio of the length of a side of a triangle to the sine of the opposite angle is constant for all three sides and angles of the triangle. It can be written as a/sin(A) = b/sin(B) = c/sin(C) or sin(A)/a = sin(B)/b = sin(C)/c.'
            },
            {
                'text': 'What is the formula for the law of cosines?',
                'answers': ['c² = a² + b² - 2ab·cos(C)', 'a² = b² + c² - 2bc·cos(A)', 'b² = a² + c² - 2ac·cos(B)'],
                'explanation': 'The law of cosines relates the square of the length of a side of a triangle to the squares of the lengths of the other two sides and the cosine of the opposite angle. It can be written as c² = a² + b² - 2ab·cos(C), a² = b² + c² - 2bc·cos(A), or b² = a² + c² - 2ac·cos(B).'
            },
            {
                'text': 'What is the value of cos(45°) in decimal form?',
                'answers': ['0.7071', '0.707', '0.71', '1/√2', '0.7'],
                'explanation': 'cos(45°) = 1/√2 ≈ 0.7071'
            },
            {
                'text': 'What is the value of tan(60°) in decimal form?',
                'answers': ['1.732', '1.73', '√3', '1.7'],
                'explanation': 'tan(60°) = √3 ≈ 1.732'
            },
        ]
        
        # Add multiple choice questions
        for q_data in trig_mc_questions:
            with transaction.atomic():
                question = Question.objects.create(
                    text=q_data['text'],
                    question_type='multiple_choice',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=gh_curriculum,
                    class_level=shs2,
                    subject=math_subject,
                    topic=trig_topic,
                    is_active=True,
                    is_premium=False
                )
                
                for choice_data in q_data['choices']:
                    QuestionChoice.objects.create(
                        question=question,
                        text=choice_data['text'],
                        is_correct=choice_data['is_correct']
                    )
        
        # Add short answer questions
        for q_data in trig_sa_questions:
            with transaction.atomic():
                question = Question.objects.create(
                    text=q_data['text'],
                    question_type='short_answer',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=gh_curriculum,
                    class_level=shs2,
                    subject=math_subject,
                    topic=trig_topic,
                    is_active=True,
                    is_premium=False
                )
                
                for answer in q_data['answers']:
                    ShortAnswer.objects.create(
                        question=question,
                        text=answer
                    )
    
    def create_quiz(self):
        """Create quiz for the topic"""
        gh_curriculum = Curriculum.objects.get(code='GH')
        shs2 = ClassLevel.objects.get(curriculum=gh_curriculum, name='SHS 2')
        math_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=shs2, name='Mathematics')
        trig_topic = Topic.objects.get(subject=math_subject, name='Trigonometry')
        
        Quiz.objects.get_or_create(
            title='Trigonometry Quiz',
            quiz_type='topic',
            curriculum=gh_curriculum,
            class_level=shs2,
            subject=math_subject,
            topic=trig_topic,
            defaults={
                'description': 'Test your knowledge of trigonometry',
                'question_count': 30,
                'per_question_time': 60,
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 70,
                'is_active': True,
            }
        )
