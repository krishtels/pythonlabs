from pyexpat.errors import messages


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, RedirectView, ListView
from lab3.settings import TEACHER, STUDENT
from .models import Teacher, User, Student
from .permissions import TeacherPermissionsMixin, StudentPermissionsMixin, SuperUserPermissionsMixin
from diary.permissions import ScoreJournalMixin
from diary.models import Lesson, Score
from .forms import UserCreateForm, UserUpdateForm, StudentForm, StudentFormSet, TeacherForm, TeacherFormSet


class TeacherListView(LoginRequiredMixin, ListView):
    template_name = 'people/teacher_list.html'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager').filter(user_status=TEACHER)
        return queryset



class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'people/teacher_detail.html'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager').filter(user_status=TEACHER)
        return queryset


class StudentDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    template_name = 'people/student_detail.html'

    def get_queryset(self):
        queryset = User.objects.select_related('student__group').filter(user_status=STUDENT)
        return queryset


class StudentAccountDetailView(LoginRequiredMixin, StudentPermissionsMixin, ScoreJournalMixin, DetailView):
    template_name = 'people/student_account.html'
    context_object_name = 'student'

    def get_object(self, queryset=None):
        return User.objects.select_related('student').get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(StudentAccountDetailView, self).get_context_data(**kwargs)
        date_period = self.create_date_period_list()
        lessons = Lesson.objects.filter(group__students=self.request.user.student.id)
        scores = Score.objects.filter(student_id=self.request.user.pk,
                                      created__in=date_period).values('id', 'lesson_id', 'score', 'created')

        context['date_period'] = date_period
        context['lessons'] = lessons
        context['scores_dict'] = self.create_scores_dict(date_period, scores, lessons, 'lesson_id')
        return context


class StudentCreateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'people/student_create.html'
    success_url = reverse_lazy('student_add')
    success_message = 'Ученик успешно добавлен.'

    def get_context_data(self, **kwargs):
        data = super(StudentCreateView, self).get_context_data(**kwargs)
        data['student_form'] = StudentForm()
        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        student_form = StudentForm(self.request.POST)
        if form.is_valid() and student_form.is_valid():
            user = form.save(commit=False)
            user.user_status = STUDENT
            student = student_form.save(commit=False)
            student.user = user
            user.save()
            student.save()
            return self.form_valid(form)
        else:
            messages.error(request, 'Ошибка сохранения !')
            return self.render_to_response({'form': form, 'student_form': student_form})


class StudentUpdateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = User
    queryset = User.objects.filter(user_status=STUDENT)
    form_class = UserUpdateForm
    template_name = 'people/student_update.html'
    success_message = 'Данные ученика успешно обновлены.'

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(self.request.POST)
        student_formset = StudentFormSet(self.request.POST, prefix='student')
        if student_formset.is_valid():
            student_formset.save()
            return super(StudentUpdateView, self).post(self.request.POST)

        else:
            messages.error(request, 'Ошибка сохранения !')
            return self.render_to_response(
                {'form': form, 'student_form': student_formset}
            )

    def get_context_data(self, **kwargs):
        data = super(StudentUpdateView, self).get_context_data(**kwargs)
        student_formset = StudentFormSet(queryset=Student.objects.filter(user_id=self.kwargs['pk']), prefix='student')

        data['student_form'] = student_formset
        return data

    def get_success_url(self):
        return reverse_lazy('student_update', kwargs={'pk': self.kwargs['pk']})


class TeacherCreateView(LoginRequiredMixin, SuperUserPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'people/teacher_create.html'
    success_url = reverse_lazy('teacher_add')
    success_message = 'Преподаватель успешно добавлен.'

    def get_context_data(self, **kwargs):
        data = super(TeacherCreateView, self).get_context_data(**kwargs)
        data['teacher_form'] = TeacherForm()
        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        teacher_form = TeacherForm(self.request.POST)
        if form.is_valid() and teacher_form.is_valid():
            user = form.save(commit=False)
            user.user_status = TEACHER
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            user.save()
            teacher.save()
            return self.form_valid(form)
        else:
            messages.error(request, 'Ошибка сохранения !')
            return self.render_to_response({'form': form, 'teacher_form': teacher_form})


class TeacherUpdateView(LoginRequiredMixin, SuperUserPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = User
    queryset = User.objects.filter(user_status=TEACHER)
    form_class = UserUpdateForm
    template_name = 'people/teacher_update.html'
    success_message = 'Данные преподавателя успешно обновлены.'

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(self.request.POST)
        teacher_formset = TeacherFormSet(self.request.POST, prefix='teacher')
        if teacher_formset.is_valid():
            teacher_formset.save()
            return super(TeacherUpdateView, self).post(self.request.POST)

        else:
            messages.error(request, 'Ошибка сохранения !')
            return self.render_to_response(
                {'form': form, 'teacher_form': teacher_formset}
            )

    def get_context_data(self, **kwargs):
        data = super(TeacherUpdateView, self).get_context_data(**kwargs)
        teacher_formset = TeacherFormSet(queryset=Teacher.objects.filter(user_id=self.kwargs['pk']), prefix='teacher')

        data['teacher_form'] = teacher_formset
        return data

    def get_success_url(self):
        return reverse_lazy('teacher_update', kwargs={'pk': self.kwargs['pk']})


class UserTypeRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('teacher_list')
