from django import forms

from lab3.settings import STUDENT, TEACHER
from .models import Score, Lesson, Group
from people.models import User, Teacher


class ScoreCreateForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=User.objects.filter(user_status=STUDENT), to_field_name='first_name')
    created = forms.DateInput(attrs={'placeholder': 'Дата занятия', 'type': 'date'})
    score = forms.Select(attrs={'placeholder': 'Оценка'})

    def __init__(self, group, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['student'] = forms.ModelChoiceField(queryset=User.objects.prefetch_related("student")
                                                        .filter(student__group=group), to_field_name='first_name')

    class Meta:
        model = Score
        fields = ['student', 'created', 'score']


class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name']
        widgets = {
               'name': forms.TextInput(attrs={'placeholder': 'Название предмета'}),
               }


class GroupCreateForm(forms.ModelForm):
    lessons = forms.ModelMultipleChoiceField(queryset=Lesson.objects.all(), to_field_name='name')

    class Meta:
        model = Group
        fields = ['number', 'lessons']
        widgets = {
               'number': forms.TextInput(attrs={'placeholder': 'Введите номер группы'}),
               }
