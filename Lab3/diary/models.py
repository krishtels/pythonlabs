from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse_lazy
from Lab3.settings import GENDER_CHOICES, USER_STATUS_CHOICES, MARK_CHOICES, STUDENT, TEACHER, AUTH_USER_MODEL


class User(AbstractUser):
    sex = models.CharField('Пол', choices=GENDER_CHOICES, max_length=6)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    photo = models.ImageField(default='static/img/default-user.png', blank=True)
    description = models.TextField('Характеристика')
    user_status = models.CharField('Статус пользователя', choices=USER_STATUS_CHOICES, max_length=15)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Student(models.Model):
    group = models.ForeignKey('Group', related_name='students', verbose_name='Состоит в классе',
                              on_delete=models.CASCADE)
    user = models.OneToOneField(AUTH_USER_MODEL, related_name='student', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.user_id})

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(models.Model):
    position = models.CharField('Должность', max_length=99)
    group_manager = models.ForeignKey('Group', related_name='teacher', verbose_name='Руководит классом',
                                      on_delete=models.SET_NULL, null=True, blank=True)
    lessons = models.ManyToManyField('Lesson', related_name='teachers', verbose_name='Ведет предметы')
    user = models.OneToOneField(AUTH_USER_MODEL, related_name='teacher', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('teacher_detail', kwargs={'pk': self.user_id})

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Lesson(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'Справочник предметов'


class Group(models.Model):
    number = models.SmallIntegerField('Номер группы')
    lessons = models.ManyToManyField(Lesson, related_name='group', verbose_name='Пары класса')
    create_group = models.DateField('Дата поступления группы учеников')

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class RatingItemStatus(models.Model):
    """Справочник статусов оценок: обычная, годовая, четверть, отменено."""
    name = models.CharField('Статус оценки', max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'статус оценки'
        verbose_name_plural = 'Справочник статусов оценок'


class Journal(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Наименование класса')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Предмет')
    student = models.ForeignKey(AUTH_USER_MODEL, related_name='mark_student', on_delete=models.CASCADE,
                                limit_choices_to={'user_status': STUDENT}, verbose_name='Студент')
    teacher = models.ForeignKey(AUTH_USER_MODEL, related_name='mark_teacher', on_delete=models.SET_NULL,
                                null=True, limit_choices_to={'user_status': TEACHER}, verbose_name='Учитель')

    mark = models.SmallIntegerField(choices=MARK_CHOICES, verbose_name='Оценка')
    mark_status = models.ForeignKey(RatingItemStatus, on_delete=models.CASCADE, verbose_name='Статус оценки')
    created = models.DateField(verbose_name='Дата создания')

    def __str__(self):
        return str(self.score)

    def get_absolute_url(self):
        return reverse_lazy('journal_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'запись журнала'
        verbose_name_plural = 'Оценки'
        unique_together = ['student', 'lesson', 'created']
