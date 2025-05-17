from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db import transaction
import csv
import io
import logging
from django.utils.text import slugify

from .models import Quiz, Question, QuestionChoice, ShortAnswer
from curriculum.models import Curriculum, ClassLevel, Subject, Topic, SubTopic

# Set up logging
logger = logging.getLogger(__name__)

@staff_member_required
def quiz_management(request):
    """View for managing quizzes."""
    quizzes = Quiz.objects.all().order_by('-created_at')

    context = {
        'quizzes': quizzes,
        'title': 'Quiz Management',
    }
    return render(request, 'admin/quiz/quiz_management.html', context)

@staff_member_required
def create_quiz(request):
    """View for creating a new quiz."""
    curricula = Curriculum.objects.filter(is_active=True)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        curriculum_id = request.POST.get('curriculum')
        class_level_id = request.POST.get('class_level')
        subject_id = request.POST.get('subject')
        topic_id = request.POST.get('topic')
        instructions = request.POST.get('instructions', '')

        # Validate required fields
        if not all([title, curriculum_id, class_level_id, subject_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('admin:create_quiz')

        # Create the quiz
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            quiz_type='topic',
            curriculum_id=curriculum_id,
            class_level_id=class_level_id,
            subject_id=subject_id,
            topic_id=topic_id if topic_id else None,
            question_count=40,  # Default value
            per_question_time=30,  # Default value
            randomize_questions=True,
            randomize_choices=True,
            passing_score=70,
            is_active=True,
            created_by=request.user,
        )

        messages.success(request, f'Quiz "{quiz.title}" created successfully. Now add questions to your quiz.')
        return redirect('my_admin:quiz_admin:add_questions', quiz_id=quiz.id)

    context = {
        'curricula': curricula,
        'title': 'Create New Quiz',
    }
    return render(request, 'my_admin/create_quiz.html', context)

@staff_member_required
def add_questions(request, quiz_id):
    """View for adding questions to a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Get existing questions for this quiz
    existing_questions = Question.objects.filter(
        curriculum=quiz.curriculum,
        class_level=quiz.class_level,
        subject=quiz.subject,
        topic=quiz.topic if quiz.topic else None,
        is_active=True
    )

    context = {
        'quiz': quiz,
        'existing_questions': existing_questions,
        'title': f'Add Questions to {quiz.title}',
    }
    return render(request, 'my_admin/add_questions.html', context)

@staff_member_required
@require_POST
def save_question(request, quiz_id):
    """AJAX view for saving a question."""
    quiz = get_object_or_404(Quiz, id=quiz_id)

    try:
        with transaction.atomic():
            question_type = request.POST.get('question_type')
            question_text = request.POST.get('question_text')
            explanation = request.POST.get('explanation', '')

            # Create the question
            question = Question.objects.create(
                text=question_text,
                question_type=question_type,
                explanation=explanation,
                curriculum=quiz.curriculum,
                class_level=quiz.class_level,
                subject=quiz.subject,
                topic=quiz.topic,
                is_active=True,
                created_by=request.user,
            )

            # Handle multiple choice questions
            if question_type == 'multiple_choice':
                choices = request.POST.getlist('choices[]')
                correct_choice = request.POST.get('correct_choice')

                for i, choice_text in enumerate(choices):
                    if choice_text.strip():
                        QuestionChoice.objects.create(
                            question=question,
                            text=choice_text,
                            is_correct=(str(i) == correct_choice),
                        )

            # Handle short answer questions
            elif question_type == 'short_answer':
                answers = request.POST.getlist('answers[]')

                for answer in answers:
                    if answer.strip():
                        ShortAnswer.objects.create(
                            question=question,
                            text=answer,
                        )

        return JsonResponse({
            'success': True,
            'message': 'Question saved successfully.',
            'question_id': question.id,
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error saving question: {str(e)}',
        })

@staff_member_required
def review_quiz(request, quiz_id):
    """View for reviewing and finalizing a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Get all questions for this quiz
    if quiz.topic:
        # Topic-specific quiz
        questions = Question.objects.filter(
            curriculum=quiz.curriculum,
            class_level=quiz.class_level,
            subject=quiz.subject,
            topic=quiz.topic,
            is_active=True
        )
    else:
        # General quiz for the subject
        questions = Question.objects.filter(
            curriculum=quiz.curriculum,
            class_level=quiz.class_level,
            subject=quiz.subject,
            is_active=True
        )

    # Log the number of questions found
    logger.info(f"Found {questions.count()} questions for quiz {quiz_id}")

    if request.method == 'POST':
        # Update quiz settings
        quiz.question_count = int(request.POST.get('question_count', 40))
        quiz.per_question_time = int(request.POST.get('per_question_time', 30))
        quiz.passing_score = int(request.POST.get('passing_score', 70))
        quiz.randomize_questions = request.POST.get('randomize_questions') == 'on'
        quiz.randomize_choices = request.POST.get('randomize_choices') == 'on'
        quiz.is_active = request.POST.get('is_active') == 'on'
        quiz.save()

        messages.success(request, f'Quiz "{quiz.title}" has been updated and is now ready for use.')
        return redirect('my_admin:quiz_management')

    context = {
        'quiz': quiz,
        'questions': questions,
        'question_count': questions.count(),
        'title': f'Review Quiz: {quiz.title}',
    }
    return render(request, 'my_admin/review_quiz.html', context)

@staff_member_required
@require_POST
def delete_question(request, question_id):
    """AJAX view for deleting a question."""
    question = get_object_or_404(Question, id=question_id)

    try:
        question.delete()
        return JsonResponse({
            'success': True,
            'message': 'Question deleted successfully.',
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error deleting question: {str(e)}',
        })

@staff_member_required
def get_class_levels(request):
    """AJAX view for getting class levels for a curriculum."""
    curriculum_id = request.GET.get('curriculum_id')

    if not curriculum_id:
        return JsonResponse({'class_levels': []})

    class_levels = ClassLevel.objects.filter(
        curriculum_id=curriculum_id,
        is_active=True
    ).values('id', 'name')

    return JsonResponse({'class_levels': list(class_levels)})

@staff_member_required
def get_subjects(request):
    """AJAX view for getting subjects for a class level."""
    class_level_id = request.GET.get('class_level_id')

    if not class_level_id:
        return JsonResponse({'subjects': []})

    subjects = Subject.objects.filter(
        class_level_id=class_level_id,
        is_active=True
    ).values('id', 'name')

    return JsonResponse({'subjects': list(subjects)})

@staff_member_required
def get_topics(request):
    """AJAX view for getting topics for a subject."""
    subject_id = request.GET.get('subject_id')

    if not subject_id:
        return JsonResponse({'topics': []})

    topics = Topic.objects.filter(
        subject_id=subject_id,
        is_active=True
    ).values('id', 'name')

    return JsonResponse({'topics': list(topics)})


@staff_member_required
def edit_question(request, question_id):
    """View for editing a question."""
    question = get_object_or_404(Question, id=question_id)

    context = {
        'question': question,
        'title': f'Edit Question',
    }
    return render(request, 'my_admin/edit_question.html', context)


@staff_member_required
@require_POST
def update_question(request, question_id):
    """AJAX view for updating a question."""
    question = get_object_or_404(Question, id=question_id)

    try:
        with transaction.atomic():
            question_type = request.POST.get('question_type')
            question_text = request.POST.get('question_text')
            explanation = request.POST.get('explanation', '')

            # Update the question
            question.text = question_text
            question.question_type = question_type
            question.explanation = explanation
            question.save()

            # Handle multiple choice questions
            if question_type == 'multiple_choice':
                # Delete existing choices
                question.questionchoice_set.all().delete()

                # Add new choices
                choices = request.POST.getlist('choices[]')
                correct_choice = request.POST.get('correct_choice')

                for i, choice_text in enumerate(choices):
                    if choice_text.strip():
                        QuestionChoice.objects.create(
                            question=question,
                            text=choice_text,
                            is_correct=(str(i) == correct_choice),
                        )

            # Handle short answer questions
            elif question_type == 'short_answer':
                # Delete existing answers
                question.shortanswer_set.all().delete()

                # Add new answers
                answers = request.POST.getlist('answers[]')

                for answer in answers:
                    if answer.strip():
                        ShortAnswer.objects.create(
                            question=question,
                            text=answer,
                        )

        return JsonResponse({
            'success': True,
            'message': 'Question updated successfully.',
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating question: {str(e)}',
        })


@staff_member_required
def import_questions(request):
    """View for importing questions from a CSV file."""
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Check if file is CSV
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('my_admin:quiz_admin:import_questions')

        # Process the CSV file
        try:
            # For Excel-generated CSV files, we'll try multiple approaches

            # First, try to read with common encodings used by Excel
            encodings_to_try = ['utf-8-sig', 'cp1252', 'latin-1', 'iso-8859-1', 'utf-16']
            csv_data = None
            successful_encoding = None

            # For debugging purposes
            import logging
            logger = logging.getLogger(__name__)

            for encoding in encodings_to_try:
                try:
                    # Reset file pointer to the beginning
                    csv_file.seek(0)
                    csv_data = csv_file.read().decode(encoding)
                    successful_encoding = encoding
                    logger.info(f"Successfully decoded CSV with encoding: {encoding}")
                    break  # If successful, break the loop
                except UnicodeDecodeError:
                    continue  # Try the next encoding

            if csv_data is None:
                # If all encodings failed, try a more aggressive approach - replace problematic characters
                try:
                    csv_file.seek(0)
                    # Read as bytes and replace problematic bytes with spaces
                    raw_data = csv_file.read()
                    csv_data = raw_data.decode('utf-8', errors='replace')
                    successful_encoding = 'utf-8 (with character replacement)'
                    logger.info("Used character replacement to decode CSV")
                except Exception:
                    # If that still fails, raise a more helpful error
                    raise ValueError("Could not read your CSV file. It may contain special characters or formatting that can't be processed. Please try saving your Excel file as 'CSV (Comma delimited)' and remove any special formatting.")

            io_string = io.StringIO(csv_data)

            # Try to parse the CSV
            try:
                reader = csv.DictReader(io_string)
                # Validate that the CSV has the required columns
                required_columns = ['curriculum_code', 'class_level_name', 'subject_name', 'topic_name', 'question_type', 'question_text']

                # Get the fieldnames from the reader
                fieldnames = reader.fieldnames

                if not fieldnames:
                    raise ValueError("CSV file appears to be empty or improperly formatted. Please check the file format.")

                # Check for missing required columns
                missing_columns = [col for col in required_columns if col not in fieldnames]
                if missing_columns:
                    raise ValueError(f"CSV file is missing required columns: {', '.join(missing_columns)}. Please use the template provided.")

                # Reset the reader to the beginning
                io_string.seek(0)
                reader = csv.DictReader(io_string)
            except Exception as e:
                raise ValueError(f"Error parsing CSV file: {str(e)}. Please ensure the file is a valid CSV format.")

            # Counters for success and error messages
            questions_created = 0
            questions_skipped = 0
            skipped_count = 0  # For duplicate questions
            errors = []
            new_question_ids = []  # Track IDs of newly created questions

            # Process each row
            for row_num, row in enumerate(reader, start=2):  # Start from 2 to account for header row
                try:
                    with transaction.atomic():
                        # Get or create curriculum
                        curriculum_code = row.get('curriculum_code', '').strip()
                        if not curriculum_code:
                            errors.append(f"Row {row_num}: Missing curriculum code")
                            questions_skipped += 1
                            continue

                        try:
                            curriculum = Curriculum.objects.get(code=curriculum_code)
                        except Curriculum.DoesNotExist:
                            errors.append(f"Row {row_num}: Curriculum with code '{curriculum_code}' does not exist")
                            questions_skipped += 1
                            continue

                        # Get or create class level
                        class_level_name = row.get('class_level_name', '').strip()
                        if not class_level_name:
                            errors.append(f"Row {row_num}: Missing class level name")
                            questions_skipped += 1
                            continue

                        try:
                            class_level = ClassLevel.objects.get(curriculum=curriculum, name=class_level_name)
                        except ClassLevel.DoesNotExist:
                            errors.append(f"Row {row_num}: Class level '{class_level_name}' does not exist for curriculum '{curriculum.name}'")
                            questions_skipped += 1
                            continue

                        # Get or create subject
                        subject_name = row.get('subject_name', '').strip()
                        if not subject_name:
                            errors.append(f"Row {row_num}: Missing subject name")
                            questions_skipped += 1
                            continue

                        try:
                            subject = Subject.objects.get(curriculum=curriculum, class_level=class_level, name=subject_name)
                        except Subject.DoesNotExist:
                            errors.append(f"Row {row_num}: Subject '{subject_name}' does not exist for {curriculum.name} - {class_level.name}")
                            questions_skipped += 1
                            continue

                        # Get or create topic
                        topic_name = row.get('topic_name', '').strip()
                        if not topic_name:
                            errors.append(f"Row {row_num}: Missing topic name")
                            questions_skipped += 1
                            continue

                        # Check if topic exists
                        try:
                            topic = Topic.objects.get(subject=subject, name=topic_name)
                            topic_created = False
                        except Topic.DoesNotExist:
                            # Create a new topic with proper ordering
                            # Get the highest order value for existing topics in this subject
                            highest_order = Topic.objects.filter(subject=subject).order_by('-order').values_list('order', flat=True).first() or 0

                            # Create the new topic with the next order value
                            topic = Topic.objects.create(
                                subject=subject,
                                name=topic_name,
                                slug=slugify(topic_name),
                                description=f'Topic for {topic_name}',
                                is_active=True,
                                order=highest_order + 1
                            )
                            topic_created = True

                            # Log that we created a new topic
                            logger.info(f"Row {row_num}: Created new topic '{topic_name}' for subject '{subject.name}'")

                            # Add a success message about the new topic
                            if 'new_topics' not in request.session:
                                request.session['new_topics'] = []
                            request.session['new_topics'].append(f"{subject.name}: {topic_name}")

                        # Get or create subtopic (optional)
                        subtopic = None
                        subtopic_name = row.get('subtopic_name', '').strip()
                        if subtopic_name:
                            # Check if subtopic exists
                            try:
                                subtopic = SubTopic.objects.get(topic=topic, name=subtopic_name)
                            except SubTopic.DoesNotExist:
                                # Create a new subtopic with proper ordering
                                # Get the highest order value for existing subtopics in this topic
                                highest_order = SubTopic.objects.filter(topic=topic).order_by('-order').values_list('order', flat=True).first() or 0

                                # Create the new subtopic with the next order value
                                subtopic = SubTopic.objects.create(
                                    topic=topic,
                                    name=subtopic_name,
                                    slug=slugify(f"{topic.slug}-{subtopic_name}"),
                                    description=f'Subtopic for {subtopic_name}',
                                    is_active=True,
                                    order=highest_order + 1
                                )

                                # Log that we created a new subtopic
                                logger.info(f"Row {row_num}: Created new subtopic '{subtopic_name}' for topic '{topic.name}'")

                                # Add a success message about the new subtopic
                                if 'new_subtopics' not in request.session:
                                    request.session['new_subtopics'] = []
                                request.session['new_subtopics'].append(f"{topic.name}: {subtopic_name}")

                        # Create the question
                        question_type = row.get('question_type', '').strip().lower()
                        if question_type not in ['multiple_choice', 'short_answer']:
                            errors.append(f"Row {row_num}: Invalid question type '{question_type}'. Must be 'multiple_choice' or 'short_answer'")
                            questions_skipped += 1
                            continue

                        question_text = row.get('question_text', '').strip()
                        if not question_text:
                            errors.append(f"Row {row_num}: Missing question text")
                            questions_skipped += 1
                            continue

                        difficulty = row.get('difficulty', 'medium').strip().lower()
                        if difficulty not in ['easy', 'medium', 'hard']:
                            difficulty = 'medium'

                        explanation = row.get('explanation', '').strip()

                        # Parse boolean fields
                        is_premium = row.get('is_premium', '').strip().lower() in ['true', 'yes', '1', 't', 'y']
                        is_active = row.get('is_active', '').strip().lower() not in ['false', 'no', '0', 'f', 'n']

                        # We're temporarily disabling strict duplicate detection
                        # This allows all questions to be imported, even if they might be duplicates

                        # Optional: Log a message about potential duplicates for informational purposes only
                        clean_text = question_text.strip()
                        first_words = ' '.join(clean_text.split()[:5])

                        if len(first_words.split()) >= 5:
                            existing_questions = Question.objects.filter(
                                curriculum=curriculum,
                                class_level=class_level,
                                subject=subject,
                                topic=topic,
                                text__icontains=first_words
                            )

                            if existing_questions.exists():
                                # Just log it, but don't skip the question
                                logger.info(f"Row {row_num}: Potential duplicate question detected, but importing anyway")

                        # Create the question regardless of potential duplicates

                        # Create the question
                        question = Question.objects.create(
                            text=question_text,
                            question_type=question_type,
                            difficulty=difficulty,
                            explanation=explanation,
                            curriculum=curriculum,
                            class_level=class_level,
                            subject=subject,
                            topic=topic,
                            subtopic=subtopic,
                            is_active=is_active,
                            is_premium=is_premium,
                            created_by=request.user
                        )

                        # Add the new question ID to our list
                        new_question_ids.append(question.id)

                        # Handle multiple choice questions
                        if question_type == 'multiple_choice':
                            # Get choices
                            choices = []
                            for i in range(1, 7):  # Up to 6 choices
                                choice_text = row.get(f'choice_{i}', '').strip()
                                if choice_text:
                                    choices.append(choice_text)

                            if len(choices) < 2:
                                errors.append(f"Row {row_num}: Multiple choice questions must have at least 2 choices")
                                question.delete()
                                questions_skipped += 1
                                continue

                            # Get correct choice
                            correct_choice = row.get('correct_choice', '').strip()
                            try:
                                correct_choice = int(correct_choice)
                                if correct_choice < 1 or correct_choice > len(choices):
                                    raise ValueError
                            except (ValueError, TypeError):
                                errors.append(f"Row {row_num}: Invalid correct choice '{correct_choice}'. Must be a number between 1 and {len(choices)}")
                                question.delete()
                                questions_skipped += 1
                                continue

                            # Create choices
                            for i, choice_text in enumerate(choices, start=1):
                                QuestionChoice.objects.create(
                                    question=question,
                                    text=choice_text,
                                    is_correct=(i == correct_choice)
                                )

                        # Handle short answer questions
                        elif question_type == 'short_answer':
                            # Get answers
                            answers = []
                            for i in range(1, 4):  # Up to 3 short answers
                                answer_text = row.get(f'short_answer_{i}', '').strip()
                                if answer_text:
                                    answers.append(answer_text)

                            if not answers:
                                errors.append(f"Row {row_num}: Short answer questions must have at least 1 acceptable answer")
                                question.delete()
                                questions_skipped += 1
                                continue

                            # Parse exact match setting
                            is_exact_match = row.get('is_exact_match', '').strip().lower() not in ['false', 'no', '0', 'f', 'n']

                            # Create short answers
                            for answer_text in answers:
                                ShortAnswer.objects.create(
                                    question=question,
                                    text=answer_text,
                                    is_exact_match=is_exact_match
                                )

                        questions_created += 1

                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    questions_skipped += 1

            # Show success message
            if questions_created > 0:
                encoding_info = ""
                if successful_encoding:
                    if "replacement" in successful_encoding:
                        encoding_info = " Some special characters may have been replaced."
                    else:
                        encoding_info = f" (File encoding: {successful_encoding})"

                # Auto-create quizzes for subjects/topics that have questions but no quiz
                # Group questions by curriculum, class level, subject, and topic
                question_groups = {}
                for question in Question.objects.filter(id__in=new_question_ids):
                    key = (
                        question.curriculum,
                        question.class_level,
                        question.subject,
                        question.topic
                    )
                    if key not in question_groups:
                        question_groups[key] = []
                    question_groups[key].append(question)

                quizzes_created = 0
                quizzes_updated = 0

                # Process each group of questions
                for (curriculum, class_level, subject, topic), questions in question_groups.items():
                    # First, check if a topic-specific quiz exists (if topic is not None)
                    existing_quiz = None
                    if topic:
                        existing_quiz = Quiz.objects.filter(
                            curriculum=curriculum,
                            class_level=class_level,
                            subject=subject,
                            topic=topic,
                            is_active=True
                        ).first()

                        if existing_quiz:
                            # Update the existing topic-specific quiz
                            # Increase question_count if needed
                            total_questions = Question.objects.filter(
                                curriculum=curriculum,
                                class_level=class_level,
                                subject=subject,
                                topic=topic,
                                is_active=True
                            ).count()

                            if total_questions > existing_quiz.question_count:
                                existing_quiz.question_count = min(40, total_questions)
                                existing_quiz.save()
                                quizzes_updated += 1

                    # If no topic-specific quiz exists or topic is None, check for a general subject quiz
                    if not existing_quiz:
                        existing_quiz = Quiz.objects.filter(
                            quiz_type='general',
                            curriculum=curriculum,
                            class_level=class_level,
                            subject=subject,
                            topic__isnull=True,
                            is_active=True
                        ).first()

                        if existing_quiz:
                            # Update the existing general quiz
                            # Increase question_count if needed
                            total_questions = Question.objects.filter(
                                curriculum=curriculum,
                                class_level=class_level,
                                subject=subject,
                                is_active=True
                            ).count()

                            if total_questions > existing_quiz.question_count:
                                existing_quiz.question_count = min(40, total_questions)
                                existing_quiz.save()
                                quizzes_updated += 1

                    # If no quiz exists at all, create a new one
                    if not existing_quiz:
                        # Create a new quiz (topic-specific or general)
                        quiz_title = f"{subject.name} - {topic.name} Quiz" if topic else f"{subject.name} General Quiz"
                        quiz_description = f"Test your knowledge of {topic.name}" if topic else f"Test your knowledge of {subject.name}"

                        Quiz.objects.create(
                            title=quiz_title,
                            description=quiz_description,
                            quiz_type='topic' if topic else 'general',
                            curriculum=curriculum,
                            class_level=class_level,
                            subject=subject,
                            topic=topic,
                            question_count=min(40, len(questions)),
                            per_question_time=30,
                            randomize_questions=True,
                            randomize_choices=True,
                            show_immediate_feedback=True,
                            passing_score=70,
                            is_active=True,
                            created_by=request.user
                        )
                        quizzes_created += 1

                quiz_message = ""
                if quizzes_created > 0 or quizzes_updated > 0:
                    quiz_message = f" Also "
                    if quizzes_created > 0:
                        quiz_message += f"created {quizzes_created} new quiz(zes)"
                    if quizzes_created > 0 and quizzes_updated > 0:
                        quiz_message += " and "
                    if quizzes_updated > 0:
                        quiz_message += f"updated {quizzes_updated} existing quiz(zes)"
                    quiz_message += "."

                # Add message about new topics if any were created
                topic_message = ""
                if 'new_topics' in request.session and request.session['new_topics']:
                    new_topics = request.session['new_topics']
                    if len(new_topics) <= 5:
                        topic_list = ", ".join(new_topics)
                        topic_message = f" Created {len(new_topics)} new topics: {topic_list}."
                    else:
                        topic_message = f" Created {len(new_topics)} new topics."
                    # Clear the session variable
                    del request.session['new_topics']
                    request.session.modified = True

                # Add message about new subtopics if any were created
                subtopic_message = ""
                if 'new_subtopics' in request.session and request.session['new_subtopics']:
                    new_subtopics = request.session['new_subtopics']
                    if len(new_subtopics) <= 5:
                        subtopic_list = ", ".join(new_subtopics)
                        subtopic_message = f" Created {len(new_subtopics)} new subtopics: {subtopic_list}."
                    else:
                        subtopic_message = f" Created {len(new_subtopics)} new subtopics."
                    # Clear the session variable
                    del request.session['new_subtopics']
                    request.session.modified = True

                messages.success(request, f"<strong>Success!</strong> Imported {questions_created} questions successfully.{encoding_info}{quiz_message}{topic_message}{subtopic_message}")

            # Show warning for skipped questions
            if questions_skipped > 0:
                if errors:
                    error_details = "<br><strong>Details:</strong><ul class='mb-0 mt-2'>"
                    for error in errors[:10]:
                        error_details += f"<li>{error}</li>"
                    if len(errors) > 10:
                        error_details += f"<li>... and {len(errors) - 10} more errors. Check your CSV file and try again.</li>"
                    error_details += "</ul>"
                    messages.warning(request, f"<strong>Warning:</strong> Skipped {questions_skipped} questions due to errors.{error_details}")
                else:
                    messages.warning(request, f"<strong>Warning:</strong> Skipped {questions_skipped} questions due to errors.")

        except Exception as e:
            messages.error(request, f"<strong>Error!</strong> Failed to process CSV file: {str(e)}")

    # Get all curricula for the form
    curricula = Curriculum.objects.filter(is_active=True)

    context = {
        'curricula': curricula,
        'title': 'Import Questions',
    }
    return render(request, 'my_admin/import_questions.html', context)


@staff_member_required
def download_template(request):
    """Download a CSV template for importing questions."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="question_import_template.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'curriculum_code', 'class_level_name', 'subject_name', 'topic_name', 'subtopic_name',
        'question_type', 'question_text', 'difficulty', 'explanation', 'is_premium', 'is_active',
        'choice_1', 'choice_2', 'choice_3', 'choice_4', 'choice_5', 'choice_6', 'correct_choice',
        'short_answer_1', 'short_answer_2', 'short_answer_3', 'is_exact_match'
    ])

    # Add a sample row for multiple choice
    writer.writerow([
        'GH', 'SHS 2', 'Mathematics', 'Algebra', '',
        'multiple_choice', 'What is 2+2?', 'easy', 'Basic addition', 'false', 'true',
        '3', '4', '5', '6', '', '', '2',
        '', '', '', ''
    ])

    # Add a sample row for short answer
    writer.writerow([
        'GH', 'Primary 6', 'English', 'Grammar', 'Nouns',
        'short_answer', 'What is the capital of Ghana?', 'medium', 'The capital city of Ghana is Accra', 'false', 'true',
        '', '', '', '', '', '', '',
        'Accra', 'accra', 'ACCRA', 'false'
    ])

    return response
