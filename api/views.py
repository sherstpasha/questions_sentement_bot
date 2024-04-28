from rest_framework import generics
from rest_framework import viewsets
from .serializers import *
from .models import *


class QuestionsView(generics.ListAPIView):
    queryset = Question.objects.filter(is_active=True)
    serializer_class = QuestionSerializer

class QuestionIdView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswersView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = CreateAnswerSerializer
    serializer_action_classes = {
               'list': AnswerSerializer,
               'create': CreateAnswerSerializer,
            }
    
class AnswerIdView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    
class DataView(generics.ListCreateAPIView):
    queryset = Data.objects.all()
    serializer_class = CreateDataSerializer
    serializer_action_classes = {
               'list': DataSerializer,
               'create': CreateDataSerializer,
            }

class DataIdView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class CoursesView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseIdView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
