# -*- coding: utf-8 -*-
from django.contrib.auth.models import User 
from api.models import *
import csv


def add_questions():
    with open('setup/column_meaning.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.DictReader(file)
        mas = list(csv_file)[2:6]
        q1 = Question.objects.create(text=mas[0]['full_version'], is_active=True)
        q1.save()
        q2 = Question.objects.create(text=mas[1]['full_version'], is_active=True)
        q2.save()
        q3 = Question.objects.create(text=mas[2]['full_version'], is_active=True)
        q3.save()
        q4 = Question.objects.create(text=mas[3]['full_version'], is_active=True)
        q4.save()

def add_courses():
    s = set()
    with open('setup/train_data.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.DictReader(file)
        for r in csv_file:
            s.add(r['question_1'])
        
    for i in s:
        c = Course.objects.create(name=i)
        c.save()
    

def add_answers_and_data():
    with open('setup/train_data.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.DictReader(file)
        for r in csv_file:
            a1 = Answer.objects.create(text=r['question_2'], question=Question.objects.get(pk=1))
            a1.save()
            a2 = Answer.objects.create(text=r['question_3'], question=Question.objects.get(pk=2))
            a2.save()
            a3 = Answer.objects.create(text=r['question_4'], question=Question.objects.get(pk=3))
            a3.save()
            a4 = Answer.objects.create(text=r['question_5'], question=Question.objects.get(pk=4))
            a4.save()
            data = Data.objects.create(course=Course.objects.get(name=r['question_1']),
                                       is_relevant=r['is_relevant'],
                                       object=r['object'],
                                       is_positive=r['is_positive'])
            data.answers.add(a1, a2, a3, a4)
            data.save()

User.objects.create_superuser('superuser', 'superuser@gmail.com', 'superuser')
add_questions()
add_courses()
add_answers_and_data()



