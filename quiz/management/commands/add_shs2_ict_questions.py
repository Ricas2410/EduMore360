import random
from django.core.management.base import BaseCommand
from django.db import transaction
from curriculum.models import Curriculum, ClassLevel, Subject, Topic
from quiz.models import Question, QuestionChoice, ShortAnswer, Quiz


class Command(BaseCommand):
    help = 'Add sample quiz questions for Ghana SHS 2 ICT'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding SHS 2 ICT questions...'))
        
        # Add topics if they don't exist
        self.add_topics()
        
        # Add questions
        self.add_shs2_ict_questions()
        
        # Create quiz
        self.create_quiz()
        
        self.stdout.write(self.style.SUCCESS('Successfully added SHS 2 ICT questions!'))
    
    def add_topics(self):
        """Add topics if they don't exist"""
        gh_curriculum = Curriculum.objects.get(code='GH')
        shs2 = ClassLevel.objects.get(curriculum=gh_curriculum, name='SHS 2')
        ict_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=shs2, name='ICT')
        
        # Add Database topic
        Topic.objects.get_or_create(
            name='Database',
            subject=ict_subject,
            defaults={
                'description': 'Database concepts and management',
                'order': 1,
                'is_active': True
            }
        )
        
        # Add Programming topic
        Topic.objects.get_or_create(
            name='Programming',
            subject=ict_subject,
            defaults={
                'description': 'Programming concepts and languages',
                'order': 2,
                'is_active': True
            }
        )
        
        # Add Networking topic
        Topic.objects.get_or_create(
            name='Networking',
            subject=ict_subject,
            defaults={
                'description': 'Computer networking concepts',
                'order': 3,
                'is_active': True
            }
        )
    
    def add_shs2_ict_questions(self):
        """Add questions for Ghana Curriculum - SHS 2 - ICT"""
        gh_curriculum = Curriculum.objects.get(code='GH')
        shs2 = ClassLevel.objects.get(curriculum=gh_curriculum, name='SHS 2')
        ict_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=shs2, name='ICT')
        
        # Get topics
        database_topic = Topic.objects.get(subject=ict_subject, name='Database')
        programming_topic = Topic.objects.get(subject=ict_subject, name='Programming')
        networking_topic = Topic.objects.get(subject=ict_subject, name='Networking')
        
        # Database questions
        database_mc_questions = [
            {
                'text': 'Which of the following is NOT a type of database?',
                'choices': [
                    {'text': 'Algorithmic Database', 'is_correct': True},
                    {'text': 'Relational Database', 'is_correct': False},
                    {'text': 'NoSQL Database', 'is_correct': False},
                    {'text': 'Object-Oriented Database', 'is_correct': False},
                ],
                'explanation': 'Algorithmic Database is not a standard type of database. The common types include Relational, NoSQL, Object-Oriented, Hierarchical, and Network databases.'
            },
            {
                'text': 'What does SQL stand for?',
                'choices': [
                    {'text': 'Structured Query Language', 'is_correct': True},
                    {'text': 'Simple Query Language', 'is_correct': False},
                    {'text': 'Standard Query Language', 'is_correct': False},
                    {'text': 'System Query Language', 'is_correct': False},
                ],
                'explanation': 'SQL stands for Structured Query Language, which is a standard language for managing and manipulating relational databases.'
            },
            {
                'text': 'Which of the following is a primary key constraint?',
                'choices': [
                    {'text': 'A field that uniquely identifies each record in a table', 'is_correct': True},
                    {'text': 'A field that can contain duplicate values', 'is_correct': False},
                    {'text': 'A field that can be null', 'is_correct': False},
                    {'text': 'A field that references another table', 'is_correct': False},
                ],
                'explanation': 'A primary key is a field or combination of fields that uniquely identifies each record in a table. It cannot contain duplicate values or be null.'
            },
            {
                'text': 'What is normalization in database design?',
                'choices': [
                    {'text': 'The process of organizing data to reduce redundancy', 'is_correct': True},
                    {'text': 'The process of adding more tables to a database', 'is_correct': False},
                    {'text': 'The process of increasing data redundancy', 'is_correct': False},
                    {'text': 'The process of converting a database to SQL', 'is_correct': False},
                ],
                'explanation': 'Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity by dividing large tables into smaller, related tables.'
            },
            {
                'text': 'Which SQL statement is used to retrieve data from a database?',
                'choices': [
                    {'text': 'SELECT', 'is_correct': True},
                    {'text': 'INSERT', 'is_correct': False},
                    {'text': 'UPDATE', 'is_correct': False},
                    {'text': 'DELETE', 'is_correct': False},
                ],
                'explanation': 'The SELECT statement is used to retrieve data from a database. INSERT is used to add new records, UPDATE is used to modify existing records, and DELETE is used to remove records.'
            },
            {
                'text': 'What is a foreign key in a relational database?',
                'choices': [
                    {'text': 'A field that links to the primary key of another table', 'is_correct': True},
                    {'text': 'A field that uniquely identifies each record in a table', 'is_correct': False},
                    {'text': 'A field that cannot be null', 'is_correct': False},
                    {'text': 'A field that contains encrypted data', 'is_correct': False},
                ],
                'explanation': 'A foreign key is a field in one table that refers to the primary key in another table, establishing a relationship between the two tables.'
            },
            {
                'text': 'Which of the following is NOT a valid SQL data type?',
                'choices': [
                    {'text': 'ARRAY', 'is_correct': True},
                    {'text': 'VARCHAR', 'is_correct': False},
                    {'text': 'INTEGER', 'is_correct': False},
                    {'text': 'DATE', 'is_correct': False},
                ],
                'explanation': 'ARRAY is not a standard SQL data type in most relational database systems. VARCHAR, INTEGER, and DATE are common SQL data types.'
            },
            {
                'text': 'What is a database transaction?',
                'choices': [
                    {'text': 'A sequence of operations performed as a single logical unit of work', 'is_correct': True},
                    {'text': 'A payment made for using a database', 'is_correct': False},
                    {'text': 'The process of backing up a database', 'is_correct': False},
                    {'text': 'The process of creating a new database', 'is_correct': False},
                ],
                'explanation': 'A database transaction is a sequence of operations performed as a single logical unit of work. It either completes entirely or fails completely, ensuring data integrity.'
            },
            {
                'text': 'What does DBMS stand for?',
                'choices': [
                    {'text': 'Database Management System', 'is_correct': True},
                    {'text': 'Data Backup Management System', 'is_correct': False},
                    {'text': 'Database Manipulation System', 'is_correct': False},
                    {'text': 'Data Business Management System', 'is_correct': False},
                ],
                'explanation': 'DBMS stands for Database Management System, which is software that enables users to create, maintain, and access a database.'
            },
            {
                'text': 'Which of the following is an example of a NoSQL database?',
                'choices': [
                    {'text': 'MongoDB', 'is_correct': True},
                    {'text': 'MySQL', 'is_correct': False},
                    {'text': 'Oracle', 'is_correct': False},
                    {'text': 'SQL Server', 'is_correct': False},
                ],
                'explanation': 'MongoDB is an example of a NoSQL database. MySQL, Oracle, and SQL Server are examples of relational database management systems.'
            },
        ]
        
        database_sa_questions = [
            {
                'text': 'What SQL command is used to create a new table?',
                'answers': ['CREATE TABLE', 'CREATE TABLE'],
                'explanation': 'The CREATE TABLE command is used to create a new table in a database.'
            },
            {
                'text': 'What is the term for a database design technique that divides tables into smaller tables to reduce redundancy?',
                'answers': ['normalization', 'Normalization'],
                'explanation': 'Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity.'
            },
            {
                'text': 'What SQL clause is used to filter records in a query?',
                'answers': ['WHERE', 'where'],
                'explanation': 'The WHERE clause is used to filter records in a SQL query based on specified conditions.'
            },
        ]
        
        # Programming questions
        programming_mc_questions = [
            {
                'text': 'Which of the following is not a programming paradigm?',
                'choices': [
                    {'text': 'Logical Programming', 'is_correct': False},
                    {'text': 'Object-Oriented Programming', 'is_correct': False},
                    {'text': 'Functional Programming', 'is_correct': False},
                    {'text': 'Database Programming', 'is_correct': True},
                ],
                'explanation': 'Database Programming is not a standard programming paradigm. Common paradigms include Procedural, Object-Oriented, Functional, and Logical Programming.'
            },
            {
                'text': 'What is an algorithm?',
                'choices': [
                    {'text': 'A step-by-step procedure for solving a problem', 'is_correct': True},
                    {'text': 'A programming language', 'is_correct': False},
                    {'text': 'A type of computer hardware', 'is_correct': False},
                    {'text': 'A database management system', 'is_correct': False},
                ],
                'explanation': 'An algorithm is a step-by-step procedure or set of rules for solving a problem or accomplishing a task.'
            },
            {
                'text': 'Which of the following is not a high-level programming language?',
                'choices': [
                    {'text': 'Assembly', 'is_correct': True},
                    {'text': 'Python', 'is_correct': False},
                    {'text': 'Java', 'is_correct': False},
                    {'text': 'C++', 'is_correct': False},
                ],
                'explanation': 'Assembly is a low-level programming language that is closely related to machine code. Python, Java, and C++ are high-level programming languages.'
            },
            {
                'text': 'What is a variable in programming?',
                'choices': [
                    {'text': 'A named storage location for data', 'is_correct': True},
                    {'text': 'A fixed value that cannot change', 'is_correct': False},
                    {'text': 'A programming error', 'is_correct': False},
                    {'text': 'A type of loop', 'is_correct': False},
                ],
                'explanation': 'A variable is a named storage location for data that can be modified during program execution.'
            },
            {
                'text': 'What is a loop in programming?',
                'choices': [
                    {'text': 'A control structure that repeats a sequence of instructions', 'is_correct': True},
                    {'text': 'A type of error', 'is_correct': False},
                    {'text': 'A data type', 'is_correct': False},
                    {'text': 'A function that returns a value', 'is_correct': False},
                ],
                'explanation': 'A loop is a control structure that repeats a sequence of instructions until a specific condition is met.'
            },
            {
                'text': 'What is an array in programming?',
                'choices': [
                    {'text': 'A data structure that stores a collection of elements', 'is_correct': True},
                    {'text': 'A type of loop', 'is_correct': False},
                    {'text': 'A programming language', 'is_correct': False},
                    {'text': 'A function that performs calculations', 'is_correct': False},
                ],
                'explanation': 'An array is a data structure that stores a collection of elements, typically of the same data type, in a contiguous memory location.'
            },
            {
                'text': 'What is a function in programming?',
                'choices': [
                    {'text': 'A reusable block of code that performs a specific task', 'is_correct': True},
                    {'text': 'A type of variable', 'is_correct': False},
                    {'text': 'A programming error', 'is_correct': False},
                    {'text': 'A data type', 'is_correct': False},
                ],
                'explanation': 'A function is a reusable block of code that performs a specific task and can be called from other parts of the program.'
            },
            {
                'text': 'What is debugging in programming?',
                'choices': [
                    {'text': 'The process of finding and fixing errors in a program', 'is_correct': True},
                    {'text': 'The process of writing code', 'is_correct': False},
                    {'text': 'The process of compiling a program', 'is_correct': False},
                    {'text': 'The process of documenting a program', 'is_correct': False},
                ],
                'explanation': 'Debugging is the process of finding and fixing errors, bugs, or defects in a computer program.'
            },
            {
                'text': 'What is object-oriented programming?',
                'choices': [
                    {'text': 'A programming paradigm based on objects and classes', 'is_correct': True},
                    {'text': 'A programming language', 'is_correct': False},
                    {'text': 'A type of database', 'is_correct': False},
                    {'text': 'A method of sorting data', 'is_correct': False},
                ],
                'explanation': 'Object-oriented programming is a programming paradigm based on the concept of objects and classes, which can contain data and code to manipulate that data.'
            },
            {
                'text': 'What is a compiler in programming?',
                'choices': [
                    {'text': 'A program that translates source code into machine code', 'is_correct': True},
                    {'text': 'A program that runs other programs', 'is_correct': False},
                    {'text': 'A program that detects errors in code', 'is_correct': False},
                    {'text': 'A program that writes code automatically', 'is_correct': False},
                ],
                'explanation': 'A compiler is a program that translates source code written in a high-level programming language into machine code that can be executed by a computer.'
            },
        ]
        
        programming_sa_questions = [
            {
                'text': 'What programming construct is used to make decisions based on conditions?',
                'answers': ['if statement', 'if-else', 'conditional statement', 'if'],
                'explanation': 'Conditional statements like if, if-else, or switch statements are used to make decisions in a program based on specified conditions.'
            },
            {
                'text': 'What is the term for a programming error that occurs during program execution?',
                'answers': ['runtime error', 'Runtime error'],
                'explanation': 'A runtime error is an error that occurs during the execution of a program, as opposed to a syntax error which is detected during compilation.'
            },
            {
                'text': 'What is the name of the loop that executes a block of code at least once before checking the condition?',
                'answers': ['do-while loop', 'do while', 'do-while'],
                'explanation': 'A do-while loop executes a block of code at least once before checking the condition for further iterations.'
            },
        ]
        
        # Networking questions
        networking_mc_questions = [
            {
                'text': 'What does LAN stand for?',
                'choices': [
                    {'text': 'Local Area Network', 'is_correct': True},
                    {'text': 'Large Area Network', 'is_correct': False},
                    {'text': 'Long Access Network', 'is_correct': False},
                    {'text': 'Logical Area Network', 'is_correct': False},
                ],
                'explanation': 'LAN stands for Local Area Network, which is a network that connects computers and devices in a limited area such as a home, school, or office building.'
            },
            {
                'text': 'What does IP stand for in networking?',
                'choices': [
                    {'text': 'Internet Protocol', 'is_correct': True},
                    {'text': 'Internet Provider', 'is_correct': False},
                    {'text': 'Internet Port', 'is_correct': False},
                    {'text': 'Internet Process', 'is_correct': False},
                ],
                'explanation': 'IP stands for Internet Protocol, which is a set of rules governing the format of data sent over the internet or local network.'
            },
            {
                'text': 'Which of the following is not a network topology?',
                'choices': [
                    {'text': 'Circular', 'is_correct': True},
                    {'text': 'Star', 'is_correct': False},
                    {'text': 'Bus', 'is_correct': False},
                    {'text': 'Ring', 'is_correct': False},
                ],
                'explanation': 'Circular is not a standard network topology. Common network topologies include Star, Bus, Ring, Mesh, and Tree.'
            },
            {
                'text': 'What is a router in networking?',
                'choices': [
                    {'text': 'A device that forwards data packets between computer networks', 'is_correct': True},
                    {'text': 'A device that connects a computer to a network', 'is_correct': False},
                    {'text': 'A device that stores network data', 'is_correct': False},
                    {'text': 'A device that encrypts network traffic', 'is_correct': False},
                ],
                'explanation': 'A router is a networking device that forwards data packets between computer networks, determining the best path for data transmission.'
            },
            {
                'text': 'What is the purpose of a firewall in networking?',
                'choices': [
                    {'text': 'To monitor and control incoming and outgoing network traffic', 'is_correct': True},
                    {'text': 'To increase network speed', 'is_correct': False},
                    {'text': 'To store network data', 'is_correct': False},
                    {'text': 'To connect multiple networks', 'is_correct': False},
                ],
                'explanation': 'A firewall is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.'
            },
            {
                'text': 'What does HTTP stand for?',
                'choices': [
                    {'text': 'Hypertext Transfer Protocol', 'is_correct': True},
                    {'text': 'Hypertext Transfer Process', 'is_correct': False},
                    {'text': 'Hypertext Transit Protocol', 'is_correct': False},
                    {'text': 'Hypertext Transport Protocol', 'is_correct': False},
                ],
                'explanation': 'HTTP stands for Hypertext Transfer Protocol, which is the foundation of data communication on the World Wide Web.'
            },
            {
                'text': 'What is the function of DNS in networking?',
                'choices': [
                    {'text': 'To translate domain names to IP addresses', 'is_correct': True},
                    {'text': 'To encrypt network traffic', 'is_correct': False},
                    {'text': 'To connect to the internet', 'is_correct': False},
                    {'text': 'To filter network traffic', 'is_correct': False},
                ],
                'explanation': 'DNS (Domain Name System) translates human-readable domain names (like www.example.com) to machine-readable IP addresses (like 192.0.2.1).'
            },
            {
                'text': 'What is a MAC address?',
                'choices': [
                    {'text': 'A unique identifier assigned to a network interface controller', 'is_correct': True},
                    {'text': 'A type of computer made by Apple', 'is_correct': False},
                    {'text': 'A network security protocol', 'is_correct': False},
                    {'text': 'A type of network cable', 'is_correct': False},
                ],
                'explanation': 'A MAC (Media Access Control) address is a unique identifier assigned to a network interface controller for use as a network address in communications within a network segment.'
            },
            {
                'text': 'What is the OSI model in networking?',
                'choices': [
                    {'text': 'A conceptual framework used to understand network interactions', 'is_correct': True},
                    {'text': 'A type of network topology', 'is_correct': False},
                    {'text': 'A network security protocol', 'is_correct': False},
                    {'text': 'A type of network cable', 'is_correct': False},
                ],
                'explanation': 'The OSI (Open Systems Interconnection) model is a conceptual framework used to understand and standardize the functions of a telecommunication or computing system without regard to its underlying internal structure and technology.'
            },
            {
                'text': 'What is a VPN in networking?',
                'choices': [
                    {'text': 'A service that provides a secure connection over a public network', 'is_correct': True},
                    {'text': 'A type of network cable', 'is_correct': False},
                    {'text': 'A network topology', 'is_correct': False},
                    {'text': 'A network protocol', 'is_correct': False},
                ],
                'explanation': 'A VPN (Virtual Private Network) is a service that provides a secure, encrypted connection over a less secure network, such as the public internet.'
            },
        ]
        
        networking_sa_questions = [
            {
                'text': 'What does WAN stand for in networking?',
                'answers': ['Wide Area Network', 'wide area network'],
                'explanation': 'WAN stands for Wide Area Network, which is a network that spans a large geographical area, often connecting multiple LANs.'
            },
            {
                'text': 'What is the protocol used for sending email over the internet?',
                'answers': ['SMTP', 'Simple Mail Transfer Protocol'],
                'explanation': 'SMTP (Simple Mail Transfer Protocol) is the standard protocol for sending email messages between servers over the internet.'
            },
            {
                'text': 'What is the default port number for HTTP?',
                'answers': ['80', '80'],
                'explanation': 'The default port number for HTTP (Hypertext Transfer Protocol) is 80.'
            },
            {
                'text': 'What is the name of the addressing system used on the internet?',
                'answers': ['IP addressing', 'IP address system', 'IP'],
                'explanation': 'IP (Internet Protocol) addressing is the system used to identify devices on a network by assigning a unique address to each device.'
            },
        ]
        
        # Add Database questions
        self.add_questions(database_mc_questions, database_sa_questions, gh_curriculum, shs2, ict_subject, database_topic)
        
        # Add Programming questions
        self.add_questions(programming_mc_questions, programming_sa_questions, gh_curriculum, shs2, ict_subject, programming_topic)
        
        # Add Networking questions
        self.add_questions(networking_mc_questions, networking_sa_questions, gh_curriculum, shs2, ict_subject, networking_topic)
    
    def add_questions(self, mc_questions, sa_questions, curriculum, class_level, subject, topic):
        """Add multiple choice and short answer questions for a topic"""
        # Add multiple choice questions
        for q_data in mc_questions:
            with transaction.atomic():
                question = Question.objects.create(
                    text=q_data['text'],
                    question_type='multiple_choice',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=curriculum,
                    class_level=class_level,
                    subject=subject,
                    topic=topic,
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
        for q_data in sa_questions:
            with transaction.atomic():
                question = Question.objects.create(
                    text=q_data['text'],
                    question_type='short_answer',
                    difficulty='medium',
                    explanation=q_data['explanation'],
                    curriculum=curriculum,
                    class_level=class_level,
                    subject=subject,
                    topic=topic,
                    is_active=True,
                    is_premium=False
                )
                
                for answer in q_data['answers']:
                    ShortAnswer.objects.create(
                        question=question,
                        text=answer
                    )
    
    def create_quiz(self):
        """Create quiz for ICT"""
        gh_curriculum = Curriculum.objects.get(code='GH')
        shs2 = ClassLevel.objects.get(curriculum=gh_curriculum, name='SHS 2')
        ict_subject = Subject.objects.get(curriculum=gh_curriculum, class_level=shs2, name='ICT')
        
        # Create general ICT quiz
        Quiz.objects.get_or_create(
            title='SHS 2 ICT Quiz',
            quiz_type='general',
            curriculum=gh_curriculum,
            class_level=shs2,
            subject=ict_subject,
            defaults={
                'description': 'Test your knowledge of ICT concepts including databases, programming, and networking',
                'question_count': 40,
                'per_question_time': 60,
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 70,
                'is_active': True,
            }
        )
        
        # Create topic quizzes
        database_topic = Topic.objects.get(subject=ict_subject, name='Database')
        Quiz.objects.get_or_create(
            title='Database Quiz',
            quiz_type='topic',
            curriculum=gh_curriculum,
            class_level=shs2,
            subject=ict_subject,
            topic=database_topic,
            defaults={
                'description': 'Test your knowledge of database concepts',
                'question_count': 15,
                'per_question_time': 60,
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 70,
                'is_active': True,
            }
        )
        
        programming_topic = Topic.objects.get(subject=ict_subject, name='Programming')
        Quiz.objects.get_or_create(
            title='Programming Quiz',
            quiz_type='topic',
            curriculum=gh_curriculum,
            class_level=shs2,
            subject=ict_subject,
            topic=programming_topic,
            defaults={
                'description': 'Test your knowledge of programming concepts',
                'question_count': 15,
                'per_question_time': 60,
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 70,
                'is_active': True,
            }
        )
        
        networking_topic = Topic.objects.get(subject=ict_subject, name='Networking')
        Quiz.objects.get_or_create(
            title='Networking Quiz',
            quiz_type='topic',
            curriculum=gh_curriculum,
            class_level=shs2,
            subject=ict_subject,
            topic=networking_topic,
            defaults={
                'description': 'Test your knowledge of networking concepts',
                'question_count': 15,
                'per_question_time': 60,
                'randomize_questions': True,
                'randomize_choices': True,
                'show_immediate_feedback': True,
                'passing_score': 70,
                'is_active': True,
            }
        )
