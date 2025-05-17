@login_required
def question_feedback(request, quiz_attempt_id, question_id, next_question_id=None):
    """Show feedback for a question after answering."""
    quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id, is_active=True)
    
    # Get the question attempt
    question_attempt = get_object_or_404(QuestionAttempt, 
                                         quiz_attempt=quiz_attempt, 
                                         question=question)
    
    # Get all choices for multiple choice questions
    choices = None
    if question.question_type == 'multiple_choice':
        choices = QuestionChoice.objects.filter(question=question)
    
    # Get correct answers for short answer questions
    correct_answers = None
    if question.question_type == 'short_answer':
        correct_answers = ShortAnswer.objects.filter(question=question)
    
    context = {
        'quiz_attempt': quiz_attempt,
        'question': question,
        'question_attempt': question_attempt,
        'choices': choices,
        'correct_answers': correct_answers,
        'next_question_id': next_question_id,
    }
    
    return render(request, 'quiz/question_feedback.html', context)
