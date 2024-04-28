from django.db import models


class Question(models.Model):
    text = models.CharField(blank=False, null=False, max_length=256, verbose_name='Вопрос')
    is_active = models.BooleanField(blank=False, null=False, default=False, verbose_name='Активен')

    class Meta():
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'

    def __str__(self) -> str:
        return self.text[:50] + '...'

class Course(models.Model):
    name = models.CharField(blank=False, null=False, max_length=256, verbose_name='Название')

    class Meta():
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'

    def __str__(self) -> str:
        return self.name

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    text = models.CharField(blank=False, null=False, max_length=256, verbose_name='Ответ')

    class Meta():
        verbose_name_plural = 'Ответы'
        verbose_name = 'Ответ'

    def __str__(self) -> str:
        return self.text[:50] + '...'
    
class Data(models.Model):
    class ObjectChoices(models.IntegerChoices):
        WEBINAR = (0, 'Вэбинар')
        PROGRAM = (1, 'Программа')
        TEACHER = (2, 'Преподаватель')

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    answers = models.ManyToManyField(Answer, verbose_name='Ответы')

    is_relevant = models.IntegerField(blank=True, null=True, verbose_name='Отзыв релевантный?')
    object = models.IntegerField(choices=ObjectChoices.choices, blank=True, null=True, verbose_name='К чему относятся?')
    is_positive = models.IntegerField(blank=True, null=True, verbose_name='Отзыв положительный?')

    class Meta():
        verbose_name_plural = 'Наборы для нейросети'
        verbose_name = 'Набор для нейросети'

    def __str__(self) -> str:
        return f"{self.pk} - {self.course}"
    
        
