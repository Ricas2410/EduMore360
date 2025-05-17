@login_required
def practice_exam(request, curriculum_code, class_level_id, subject_slug):
    """Create and start a practice exam for a subject."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    
    # Get selected topics from the form
    selected_topic_ids = request.POST.getlist('topics')
    question_count = request.POST.get('question_count', 40)
    
    try:
        question_count = int(question_count)
        if question_count < 1:
            question_count = 40
    except (ValueError, TypeError):
        question_count = 40
    
    # Create a practice exam quiz
    quiz = Quiz.objects.create(
        title=f"Practice Exam - {subject.name}",
        description=f"Practice exam for {subject.name}",
        quiz_type='practice',
        curriculum=curriculum,
        class_level=class_level,
        subject=subject,
        question_count=question_count,
        per_question_time=30,  # 30 seconds per question
        randomize_questions=True,
        randomize_choices=True,
        passing_score=70,
        is_active=True,
        created_by=request.user if request.user.is_staff else None,
    )
    
    # Create a new quiz attempt
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        status='in_progress',
        total_questions=question_count
    )
    
    # Get questions for the practice exam
    if selected_topic_ids:
        # Get questions from selected topics
        questions = Question.objects.filter(
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            topic_id__in=selected_topic_ids,
            is_active=True
        )
    else:
        # Get questions from all topics in the subject
        questions = Question.objects.filter(
            curriculum=curriculum,
            class_level=class_level,
            subject=subject,
            is_active=True
        )
    
    # Filter out premium questions if user is not premium
    if not request.user.is_premium:
        questions = questions.filter(is_premium=False)
    
    # Randomize and limit to question count
    questions = questions.order_by('?')[:question_count]
    
    # Create question attempts for each question
    for question in questions:
        QuestionAttempt.objects.create(
            quiz_attempt=quiz_attempt,
            question=question
        )
    
    # Redirect to the quiz taking page
    return redirect('quiz:take_quiz', quiz_id=quiz.id)
