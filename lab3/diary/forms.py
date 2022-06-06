from django import forms

from lab3.settings import STUDENT
from .models import Score
from people.models import User


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
