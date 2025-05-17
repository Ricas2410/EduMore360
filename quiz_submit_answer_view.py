@login_required
def submit_answer(request, quiz_attempt_id, question_id):
    """Submit an answer for a question."""
    if request.method != 'POST':
        return redirect('quiz:take_quiz', quiz_id=quiz_attempt_id)

    quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id, is_active=True)

    # Check if the quiz is still in progress
    if quiz_attempt.status != 'in_progress':
        messages.warning(request, "This quiz is no longer in progress.")
        return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # Get the question attempt or create a new one
    question_attempt, created = QuestionAttempt.objects.get_or_create(
        quiz_attempt=quiz_attempt,
        question=question
    )

    # Get time spent on this question
    time_spent = request.POST.get('time_spent', 0)
    try:
        time_spent = int(time_spent)
    except (ValueError, TypeError):
        time_spent = 0
    
    # Check if the question timed out
    timed_out = request.POST.get('timed_out') == 'true'
    question_attempt.time_spent = time_spent
    question_attempt.timed_out = timed_out

    # Process the answer based on question type
    is_correct = False
    if not timed_out:  # Only check correctness if not timed out
        if question.question_type == 'multiple_choice':
            choice_id = request.POST.get('choice')
            if choice_id:
                choice = get_object_or_404(QuestionChoice, id=choice_id, question=question)
                question_attempt.selected_choice = choice
                is_correct = choice.is_correct
        else:  # short_answer
            provided_answer = request.POST.get('answer', '').strip()
            question_attempt.provided_answer = provided_answer

            # Check if the answer is correct using our validator
            correct_answers = ShortAnswer.objects.filter(question=question)
            is_correct = ShortAnswerValidator.validate_answer(provided_answer, correct_answers)

    # Update the question attempt
    question_attempt.is_correct = is_correct
    question_attempt.save()

    # Update the quiz attempt score
    correct_count = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt, is_correct=True).count()
    quiz_attempt.correct_answers = correct_count
    quiz_attempt.score = int((correct_count / quiz_attempt.total_questions) * 100)
    quiz_attempt.save()

    # Get the next question ID if available
    next_question_id = request.POST.get('next_question_id')
    
    # Check if we should show feedback
    show_feedback = request.POST.get('show_feedback') == 'true'
    
    if show_feedback:
        # Redirect to feedback page
        return redirect('quiz:question_feedback', 
                        quiz_attempt_id=quiz_attempt.id, 
                        question_id=question.id,
                        next_question_id=next_question_id or '')
    
    # Check if all questions have been answered
    attempted_count = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempt).count()
    if attempted_count >= quiz_attempt.total_questions:
        quiz_attempt.status = 'completed'
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()
        return redirect('quiz:quiz_results', quiz_attempt_id=quiz_attempt.id)

    # Continue to the next question
    if next_question_id:
        return redirect(f'quiz:take_quiz?question_id={next_question_id}', quiz_id=quiz_attempt.quiz.id)
    else:
        return redirect('quiz:take_quiz', quiz_id=quiz_attempt.quiz.id)
