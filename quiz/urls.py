from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # Quiz selection
    path('', views.quiz_home, name='quiz_home'),

    # Quiz taking
    path('take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('question/<int:quiz_attempt_id>/<int:question_id>/', views.answer_question, name='answer_question'),
    path('submit-answer/<int:quiz_attempt_id>/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('feedback/<int:quiz_attempt_id>/<int:question_id>/', views.question_feedback, name='question_feedback'),
    path('feedback/<int:quiz_attempt_id>/<int:question_id>/<str:next_question_id>/', views.question_feedback, name='question_feedback_with_next'),

    # Quiz results
    path('results/<int:quiz_attempt_id>/', views.quiz_results, name='quiz_results'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('resume/<int:quiz_attempt_id>/', views.resume_quiz, name='resume_quiz'),
    path('start/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('subject/<slug:subject_slug>/', views.subject_quizzes, name='subject_quizzes'),

    # Practice exam
    path('practice-exam/<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/',
         views.practice_exam_setup, name='practice_exam_setup'),

    # Curriculum-specific paths
    path('<str:curriculum_code>/', views.quiz_class_level_list, name='quiz_class_level_list'),
    path('<str:curriculum_code>/<int:class_level_id>/', views.quiz_subject_list, name='quiz_subject_list'),
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/', views.quiz_topic_list, name='quiz_topic_list'),
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/general/',
         views.start_general_quiz, name='start_general_quiz'),
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/topics/<slug:topic_slug>/',
         views.start_topic_quiz, name='start_topic_quiz'),

    # Study mode
    path('study/<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/<slug:topic_slug>/',
         views.study_mode, name='study_mode'),
    path('study/<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/<slug:topic_slug>/<int:note_id>/',
         views.study_mode, name='study_mode'),
    path('study-note/<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/<slug:topic_slug>/<int:note_id>/',
         views.study_note, name='study_note'),
    path('mark-note-completed/<int:note_id>/', views.mark_note_completed, name='mark_note_completed'),

    # Practice questions
    path('check-answer/<int:question_id>/<int:choice_id>/', views.check_answer, name='check_answer'),
    path('check-short-answer/<int:question_id>/', views.check_short_answer, name='check_short_answer'),

    # AJAX endpoints for dynamic form updates
    path('get-class-levels/', views.get_class_levels, name='get_class_levels'),
    path('get-subjects/', views.get_subjects, name='get_subjects'),
    path('get-topics/', views.get_topics, name='get_topics'),
]
