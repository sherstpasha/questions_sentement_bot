from django.contrib import admin, messages
from django.contrib.auth.models import Group, User
from .models import *

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    pass
