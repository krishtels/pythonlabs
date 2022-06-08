from django import forms
from django.core import validators

from lab3.settings import STUDENT, TEACHER
from .models import Score, Lesson, Group
from people.models import User, Teacher


class ScoreCreateForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=User.objects.filter(user_status=STUDENT), to_field_name='first_name')
    score = forms.Select(attrs={'placeholder': 'Оценка'})

    def __init__(self, group, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['student'] = forms.ModelChoiceField(queryset=User.objects.prefetch_related("student")
                                                        .filter(student__group=group), to_field_name='first_name')

    class Meta:
        model = Score
        fields = ['student', 'created', 'score']
        widgets = {
            'created': forms.DateInput(attrs={'type': 'date', 'data-date-format': 'yyyy-mm-dd'}, format='%Y-%m-%d')
        }


class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название предмета'}),
        }


class GroupCreateForm(forms.ModelForm):
    lessons = forms.ModelMultipleChoiceField(queryset=Lesson.objects.all(), to_field_name='name')
    number = forms.CharField(validators=[validators.RegexValidator(regex=r'\d{6}',
                                                                   message='Номер группы должен состоять из 6 цифр')])

    class Meta:
        model = Group
        fields = ['number', 'lessons']
