from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator

from curriculum.models import Subject, Topic, Note
from quiz.models import Question


def search(request):
    """Search view for the application."""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    page = request.GET.get('page', 1)

    results = []
    total_count = 0

    if query:
        if search_type == 'all' or search_type == 'subjects':
            # Search subjects
            subjects = Subject.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).filter(is_active=True)

            for subject in subjects:
                results.append({
                    'type': 'subject',
                    'title': subject.name,
                    'description': subject.description,
                    'url': subject.get_absolute_url(),
                    'curriculum': subject.curriculum.name,
                    'class_level': subject.class_level.name,
                })

            total_count += subjects.count()

        if search_type == 'all' or search_type == 'topics':
            # Search topics
            topics = Topic.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).filter(is_active=True)

            for topic in topics:
                results.append({
                    'type': 'topic',
                    'title': topic.name,
                    'description': topic.description,
                    'url': topic.get_absolute_url(),
                    'subject': topic.subject.name,
                    'curriculum': topic.subject.curriculum.name,
                    'class_level': topic.subject.class_level.name,
                })

            total_count += topics.count()

        if search_type == 'all' or search_type == 'notes':
            # Search notes
            notes = Note.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).filter(is_active=True)

            for note in notes:
                results.append({
                    'type': 'note',
                    'title': note.title,
                    'description': note.content[:200] + '...' if len(note.content) > 200 else note.content,
                    'url': note.get_absolute_url(),
                    'topic': note.topic.name,
                    'subject': note.topic.subject.name,
                })

            total_count += notes.count()

        if search_type == 'all' or search_type == 'questions':
            # Search questions
            questions = Question.objects.filter(
                Q(text__icontains=query)
            ).filter(is_active=True)

            for question in questions:
                results.append({
                    'type': 'question',
                    'title': f"Question: {question.text[:100]}...",
                    'description': question.explanation[:200] + '...' if len(question.explanation) > 200 else question.explanation,
                    'url': f"/quiz/question/{question.id}/",
                    'subject': question.subject.name,
                    'topic': question.topic.name if question.topic else '',
                })

            total_count += questions.count()

    # Sort results by relevance (simple implementation)
    # In a real implementation, you might want to use more sophisticated ranking
    results.sort(key=lambda x: query.lower() in x['title'].lower(), reverse=True)

    # Paginate results
    paginator = Paginator(results, 10)  # Show 10 results per page
    page_obj = paginator.get_page(page)

    context = {
        'query': query,
        'search_type': search_type,
        'results': page_obj,
        'total_count': total_count,
    }

    return render(request, 'search/search_results.html', context)


def advanced_search(request):
    """Advanced search view with PostgreSQL full-text search."""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    curriculum = request.GET.get('curriculum', '')
    class_level = request.GET.get('class_level', '')
    subject = request.GET.get('subject', '')
    page = request.GET.get('page', 1)

    results = []
    total_count = 0

    if query:
        search_query = SearchQuery(query)

        if search_type == 'all' or search_type == 'subjects':
            # Search subjects with full-text search
            subject_vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
            subjects = Subject.objects.annotate(
                rank=SearchRank(subject_vector, search_query)
            ).filter(rank__gt=0).filter(is_active=True).order_by('-rank')

            # Apply filters
            if curriculum:
                subjects = subjects.filter(curriculum__code=curriculum)
            if class_level:
                subjects = subjects.filter(class_level__id=class_level)

            for subject in subjects:
                results.append({
                    'type': 'subject',
                    'title': subject.name,
                    'description': subject.description,
                    'url': subject.get_absolute_url(),
                    'curriculum': subject.curriculum.name,
                    'class_level': subject.class_level.name,
                    'rank': subject.rank,
                })

            total_count += subjects.count()

        if search_type == 'all' or search_type == 'topics':
            # Search topics with full-text search
            topic_vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
            topics = Topic.objects.annotate(
                rank=SearchRank(topic_vector, search_query)
            ).filter(rank__gt=0).filter(is_active=True).order_by('-rank')

            # Apply filters
            if curriculum:
                topics = topics.filter(subject__curriculum__code=curriculum)
            if class_level:
                topics = topics.filter(subject__class_level__id=class_level)
            if subject:
                topics = topics.filter(subject__slug=subject)

            for topic in topics:
                results.append({
                    'type': 'topic',
                    'title': topic.name,
                    'description': topic.description,
                    'url': topic.get_absolute_url(),
                    'subject': topic.subject.name,
                    'curriculum': topic.subject.curriculum.name,
                    'class_level': topic.subject.class_level.name,
                    'rank': topic.rank,
                })

            total_count += topics.count()

        if search_type == 'all' or search_type == 'notes':
            # Search notes with full-text search
            note_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
            notes = Note.objects.annotate(
                rank=SearchRank(note_vector, search_query)
            ).filter(rank__gt=0).filter(is_active=True).order_by('-rank')

            # Apply filters
            if curriculum:
                notes = notes.filter(topic__subject__curriculum__code=curriculum)
            if class_level:
                notes = notes.filter(topic__subject__class_level__id=class_level)
            if subject:
                notes = notes.filter(topic__subject__slug=subject)

            for note in notes:
                results.append({
                    'type': 'note',
                    'title': note.title,
                    'description': note.content[:200] + '...' if len(note.content) > 200 else note.content,
                    'url': note.get_absolute_url(),
                    'topic': note.topic.name,
                    'subject': note.topic.subject.name,
                    'rank': note.rank,
                })

            total_count += notes.count()

        if search_type == 'all' or search_type == 'questions':
            # Search questions with full-text search
            question_vector = SearchVector('text', weight='A') + SearchVector('explanation', weight='B')
            questions = Question.objects.annotate(
                rank=SearchRank(question_vector, search_query)
            ).filter(rank__gt=0).filter(is_active=True).order_by('-rank')

            # Apply filters
            if curriculum:
                questions = questions.filter(curriculum__code=curriculum)
            if class_level:
                questions = questions.filter(class_level__id=class_level)
            if subject:
                questions = questions.filter(subject__slug=subject)

            for question in questions:
                results.append({
                    'type': 'question',
                    'title': f"Question: {question.text[:100]}...",
                    'description': question.explanation[:200] + '...' if len(question.explanation) > 200 else question.explanation,
                    'url': f"/quiz/question/{question.id}/",
                    'subject': question.subject.name,
                    'topic': question.topic.name if question.topic else '',
                    'rank': question.rank,
                })

            total_count += questions.count()

    # Sort results by rank
    results.sort(key=lambda x: x.get('rank', 0), reverse=True)

    # Paginate results
    paginator = Paginator(results, 10)  # Show 10 results per page
    page_obj = paginator.get_page(page)

    # Get data for filter dropdowns
    from curriculum.models import Curriculum, ClassLevel, Subject

    curricula = Curriculum.objects.filter(is_active=True)
    class_levels = ClassLevel.objects.filter(is_active=True)
    subjects = Subject.objects.filter(is_active=True)

    context = {
        'query': query,
        'search_type': search_type,
        'curriculum': curriculum,
        'class_level': class_level,
        'subject': subject,
        'results': page_obj,
        'total_count': total_count,
        'curricula': curricula,
        'class_levels': class_levels,
        'subjects': subjects,
    }

    return render(request, 'search/advanced_search.html', context)
