from pyexpat.errors import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Sum, Avg
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, RedirectView, ListView
from lab3.settings import TEACHER, STUDENT
from .models import Teacher, User, Student
from .permissions import TeacherPermissionsMixin, StudentPermissionsMixin
from diary.permissions import ScoreJournalMixin
from diary.models import Lesson, Score
from .forms import UserCreateForm, UserUpdateForm, StudentForm, StudentFormSet


class TeacherListView(LoginRequiredMixin, ListView):
    template_name = 'people/teacher_list.html'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager').filter(user_status=TEACHER)
        return queryset


class TeacherDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
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
        #
        # count_scores = scores.values('score').annotate(count_score=Count('score')).order_by('-score')
        # total_scores = count_scores.aggregate(sum_count=Sum('count_score'),
        #                                       sum_score=Avg('score'),
        #                                       sum_score_percent=Avg('score')*20)
        #
        # student_rating = {5: 0, 4: 0, 3: 0, 2: 0}
        # for item in count_scores:
        #     student_rating[item['score']] = item['count_score']

        # context['rating'] = student_rating
        # context['total_scores'] = total_scores
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


class UserTypeRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.user_status == STUDENT:
            return reverse_lazy('student_account')

        else:
            return reverse_lazy('group_student_list')
