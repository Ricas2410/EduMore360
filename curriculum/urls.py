from django.urls import path
from . import views

app_name = 'curriculum'

urlpatterns = [
    # Curriculum selection
    path('', views.curriculum_list, name='curriculum_list'),
    path('<str:curriculum_code>/', views.class_level_list, name='class_level_list'),
    path('<str:curriculum_code>/<int:class_level_id>/', views.subject_list, name='subject_list'),

    # Subject and branch navigation
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/', views.subject_detail, name='subject_detail'),
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/branches/<slug:branch_slug>/',
         views.branch_detail, name='branch_detail'),

    # Topic and subtopic navigation
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/topics/<slug:topic_slug>/',
         views.topic_detail, name='topic_detail'),
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/branches/<slug:branch_slug>/topics/<slug:topic_slug>/',
         views.branch_topic_detail, name='branch_topic_detail'),
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/topics/<slug:topic_slug>/subtopics/<slug:subtopic_slug>/',
         views.subtopic_detail, name='subtopic_detail'),

    # Note viewing
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/topics/<slug:topic_slug>/notes/<slug:note_slug>/',
         views.note_detail, name='note_detail'),
    path('<str:curriculum_code>/<int:class_level_id>/<slug:subject_slug>/topics/<slug:topic_slug>/subtopics/<slug:subtopic_slug>/notes/<slug:note_slug>/',
         views.subtopic_note_detail, name='subtopic_note_detail'),

    # Progress tracking
    path('topics/<int:topic_id>/mark-started/', views.mark_topic_started, name='mark_topic_started'),
    path('subtopics/<int:subtopic_id>/mark-started/', views.mark_subtopic_started, name='mark_subtopic_started'),
]
