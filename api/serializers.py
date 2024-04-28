from dataclasses import fields
from rest_framework import serializers

from .utils import nn
from .models import *


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text')

class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'text')

class AnswerSerializer(CreateAnswerSerializer):
    class Meta(CreateAnswerSerializer.Meta):
        depth = 2

class CreateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('id', 'timestamp', 'course', 'answers', 'is_relevant', 'object', 'is_positive')

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        data = Data.objects.create(**validated_data)
        (data.is_relevant, 
         data.object, 
         data.is_positive) = nn(map(lambda x: (x.question.text, x.text), 
                                    answers))
        data.answers.add(*answers)
        data.save()
        return data

class DataSerializer(CreateDataSerializer):
    class Meta(CreateDataSerializer.Meta):
        depth = 2
