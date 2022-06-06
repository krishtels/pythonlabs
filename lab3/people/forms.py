from django import forms
from django.forms import modelformset_factory

from .models import Student, User


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'birth_date', 'sex', 'photo', 'description']
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
                   'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
                   'password': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
                   'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
                   'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                   'birth_date': forms.DateInput(attrs={'placeholder': 'Дата рождения', 'type': 'date'}),
                   'sex': forms.Select(attrs={'placeholder': 'Пол'}),
                   'photo': forms.FileInput(attrs={'class': 'input-file'}),
                   'description': forms.Textarea(attrs={'placeholder': 'Характеристика', 'rows': 5, 'cols': 30}),
                   }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'sex', 'birth_date', 'photo', 'description']
        widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
                   'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                   'birth_date': forms.DateInput(attrs={'type': 'date', 'data-date-format': 'yyyy-mm-dd'},
                                                 format=('%Y-%m-%d')),
                   'sex': forms.Select(attrs={'placeholder': 'Пол'}),
                   'photo': forms.FileInput(attrs={'class': 'input-file'}),
                   'description': forms.Textarea(attrs={'placeholder': 'Характеристика', 'rows': 5, 'cols': 40}),
                   }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('group',)
        widgets = {'group': forms.Select()}


StudentFormSet = modelformset_factory(Student, form=StudentForm, max_num=1, extra=1)

