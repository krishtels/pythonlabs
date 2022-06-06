from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from lab3.settings import SCORE_CHOICES, STUDENT, TEACHER


class Lesson(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Список предметов'


class Group(models.Model):
    number = models.CharField('Номер группы', max_length=6)
    lessons = models.ManyToManyField(Lesson, related_name='group', verbose_name='Пары класса')
    create_group = models.DateField('Дата создания группы')
    updated = models.DateField('Дата обновления', auto_now=True)
    created = models.DateField('Дата создания', auto_now_add=True)

    def get_absolute_url(self):
        return reverse_lazy('group_student_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Список групп'


class Score(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Наименование группы')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Предмет')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='score_student', on_delete=models.CASCADE,
                                limit_choices_to={'user_status': STUDENT}, verbose_name='Студент')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='score_teacher', on_delete=models.SET_NULL,
                                null=True, limit_choices_to={'user_status': TEACHER}, verbose_name='Учитель')
    score = models.SmallIntegerField(choices=SCORE_CHOICES, verbose_name='Оценка')
    created = models.DateField(verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return str(self.score)

    def get_absolute_url(self):
        return reverse_lazy('score_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Запись журнала'
        verbose_name_plural = 'Оценки'
        unique_together = ['student', 'lesson', 'created']
