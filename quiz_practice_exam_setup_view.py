@login_required
def practice_exam_setup(request, curriculum_code, class_level_id, subject_slug):
    """Setup page for creating a practice exam."""
    curriculum = get_object_or_404(Curriculum, code=curriculum_code, is_active=True)
    class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, curriculum=curriculum, class_level=class_level, is_active=True)
    
    # Get all topics for this subject
    topics = Topic.objects.filter(subject=subject, is_active=True).order_by('order', 'name')
    
    if request.method == 'POST':
        # Process the form and create the practice exam
        return practice_exam(request, curriculum_code, class_level_id, subject_slug)
    
    context = {
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'topics': topics,
    }
    
    return render(request, 'quiz/practice_exam_setup.html', context)
