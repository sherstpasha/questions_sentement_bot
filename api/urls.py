from django.urls import path, include
from .views import *


urlpatterns = [
    path('questions/', QuestionsView.as_view()),
    path('questions/<int:id>/', QuestionIdView.as_view()),
    path('data/', DataView.as_view()),
    path('data/<int:id>/', DataIdView.as_view()),
    path('answers/', AnswersView.as_view()),
    path('answers/<int:id>/', AnswerIdView.as_view()),
    path('courses/', CoursesView.as_view()),
    path('courses/<int:id>/', CourseIdView.as_view()),
]