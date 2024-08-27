# from django.urls import path
# from . import views

# app_name = 'quiz'

# urlpatterns = [
#     path('', views.upload_file, name='upload_file'),
#     path('quiz_types/', views.quiz_types, name='quiz_types'),
#     path('quiz/<str:t_id>/<str:quiz_type>/', views.display_quiz, name='display_quiz'),
# ]

from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('quiz_types/', views.quiz_types, name='quiz_types'),
    path('quiz/<str:t_id>/<str:quiz_type>/', views.display_quiz, name='display_quiz'),
]