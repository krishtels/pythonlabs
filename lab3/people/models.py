from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse_lazy

from lab3.settings import USER_STATUS_CHOICES, GENDER_CHOICES


class User(AbstractUser):
    sex = models.CharField('Пол', choices=GENDER_CHOICES, max_length=1)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    photo = models.ImageField(upload_to='people/', default='diary/static/img/default-user.png', blank=True)
    description = models.TextField('Характеристика')
    user_status = models.CharField('Статус пользователя', choices=USER_STATUS_CHOICES, max_length=15)
    updated = models.DateField('Дата обновления', auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Teacher(models.Model):
    position = models.CharField('Должность', max_length=99)
    group_manager = models.ForeignKey('diary.Group', related_name='teacher', verbose_name='Курирует группу',
                                      on_delete=models.SET_NULL, null=True, blank=True)
    lessons = models.ManyToManyField('diary.Lesson', related_name='teachers', verbose_name='Ведет предметы')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='teacher', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('teacher_detail', kwargs={'pk': self.user_id})

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Student(models.Model):
    group = models.ForeignKey('diary.Group', related_name='students', verbose_name='Состоит в группе',
                              on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='student', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.user_id})

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

