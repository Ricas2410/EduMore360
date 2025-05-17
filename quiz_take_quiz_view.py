@login_required
def take_quiz(request, quiz_id):
    """View for taking a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    # Check if there's an in-progress attempt for this quiz
    quiz_attempt = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz,
        status='in_progress'
    ).order_by('-started_at').first()

    if not quiz_attempt:
        # Create a new quiz attempt using the QuizService
        quiz_attempt = QuizService.create_quiz_attempt(request.user, quiz)

    # Get the current question ID from the URL parameter
    current_question_id = request.GET.get('question_id')
    
    # If a specific question is requested, use that
    if current_question_id:
        try:
            current_question = Question.objects.get(id=current_question_id)
            # Verify this question belongs to this quiz attempt
            question_attempt, created = QuestionAttempt.objects.get_or_create(
                quiz_attempt=quiz_attempt,
                question=current_question
            )
        except Question.DoesNotExist:
            # If question doesn't exist, get the next unanswered question
            current_question = QuizService.get_next_question(quiz_attempt)
            if current_question:
                question_attempt, created = QuestionAttempt.objects.get_or_create(
                    quiz_attempt=quiz_attempt,
                    question=current_question
                )
    else:
        # Get the next question for this attempt
        current_question = QuizService.get_next_question(quiz_attempt)
        if current_question:
            question_attempt, created = QuestionAttempt.objects.get_or_create(
                quiz_attempt=quiz_attempt,
                question=current_question
            )

    if not current_question:
        # If there are no more questions, redirect to the results page
        quiz_attempt.status = 'completed'
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()
        return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # Get all question attempts for this quiz attempt to build navigation
    all_question_attempts = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt).order_by('id')
    question_ids = list(all_question_attempts.values_list('question_id', flat=True))
    
    # Find previous and next question IDs for navigation
    try:
        current_index = question_ids.index(current_question.id)
        prev_question_id = question_ids[current_index - 1] if current_index > 0 else None
        next_question_id = question_ids[current_index + 1] if current_index < len(question_ids) - 1 else None
    except (ValueError, IndexError):
        prev_question_id = None
        next_question_id = None

    # Get randomized choices for multiple-choice questions
    choices = []
    if current_question.question_type == 'multiple_choice':
        choices = QuestionRandomizer.randomize_choices(current_question)

    # Calculate progress
    total_attempted = all_question_attempts.count()
    progress_percentage = int((total_attempted / quiz_attempt.total_questions) * 100)
    
    # Get the per-question time limit
    per_question_time = quiz.per_question_time

    context = {
        'quiz': quiz_attempt.quiz,
        'quiz_attempt': quiz_attempt,
        'question_attempt': question_attempt,
        'choices': choices,
        'per_question_time': per_question_time,
        'progress_percentage': progress_percentage,
        'current_question_number': current_index + 1 if 'current_index' in locals() else 1,
        'total_questions': quiz_attempt.total_questions,
        'prev_question_id': prev_question_id,
        'next_question_id': next_question_id,
        'all_question_attempts': all_question_attempts,
    }
    return render(request, 'quiz/take_quiz.html', context)
