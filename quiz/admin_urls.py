from django.urls import path
from . import admin_views

app_name = 'quiz_admin'

urlpatterns = [
    # Quiz management
    path('create-quiz/', admin_views.create_quiz, name='create_quiz'),
    path('add-questions/<int:quiz_id>/', admin_views.add_questions, name='add_questions'),
    path('review-quiz/<int:quiz_id>/', admin_views.review_quiz, name='review_quiz'),
    path('import-questions/', admin_views.import_questions, name='import_questions'),
    path('download-template/', admin_views.download_template, name='download_template'),
    path('edit-question/<int:question_id>/', admin_views.edit_question, name='edit_question'),
    path('update-question/<int:question_id>/', admin_views.update_question, name='update_question'),

    # AJAX endpoints
    path('save-question/<int:quiz_id>/', admin_views.save_question, name='save_question'),
    path('delete-question/<int:question_id>/', admin_views.delete_question, name='delete_question'),
    path('get-class-levels/', admin_views.get_class_levels, name='get_class_levels'),
    path('get-subjects/', admin_views.get_subjects, name='get_subjects'),
    path('get-topics/', admin_views.get_topics, name='get_topics'),
]
