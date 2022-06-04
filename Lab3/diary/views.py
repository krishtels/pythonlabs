from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView
from Lab3.settings import STUDENT, TEACHER
from django.db.models import Count, Sum, Avg
from .forms import UserCreateForm, StudentForm, StudentFormSet, UserUpdateForm
from .models import Teacher, Student, User, Lesson, Journal, Group
from .permissions import TeacherPermissionsMixin, StudentPermissionsMixin, JournalMixin, TeacherLessonPermissionsMixin


class TeacherListView(LoginRequiredMixin, ListView):
    template_name = 'diary/teacher_list.html'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager__group').filter(user_status=TEACHER)
        return queryset


class TeacherDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    model = Teacher
    template_name = 'diary/teacher_detail.html'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager__group').filter(user_status=TEACHER)
        return queryset


class StudentDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    template_name = 'diary/student_detail.html'

    def get_queryset(self):
        queryset = User.objects.select_related('student__group').filter(user_status=STUDENT)
        return queryset


class StudentAccountDetailView(LoginRequiredMixin, StudentPermissionsMixin, JournalMixin, DetailView):
    template_name = 'diary/student_account.html'
    context_object_name = 'student'

    def get_object(self, queryset=None):
        return User.objects.select_related('student').get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(StudentAccountDetailView, self).get_context_data(**kwargs)
        date_period = self.create_date_period_list()
        lessons = Lesson.objects.filter(group__students=self.request.user.student.id)
        marks = Journal.objects.filter(student_id=self.request.user.pk,
                                       created__in=date_period).values('id', 'lesson_id', 'mark', 'created')

        count_marks = marks.values('mark').annotate(count_mark=Count('mark')).order_by('-mark')
        total_marks = count_marks.aggregate(sum_count=Sum('count_mark'),
                                            sum_score=Avg('mark'),
                                            sum_score_percent=Avg('mark') * 20)

        student_rating = {10: 0, 9: 0, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0}
        for item in count_marks:
            student_rating[item['mark']] = item['count_mark']

        context['rating'] = student_rating
        context['total_marks'] = total_marks
        context['date_period'] = date_period
        context['lessons'] = lessons
        context['journal_dict'] = self.create_journal_dict(date_period, marks, lessons, 'lesson_id')
        return context


class StudentCreateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'diary/student_create.html'
    success_url = reverse_lazy('student_add')
    success_message = 'Ученик усешно добавлен.'

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
    template_name = 'diary/student_update.html'
    success_message = 'Данные ученика успешно обновлены.'

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(self.request.POST)
        student_formset = StudentFormSet(self.request.POST, prefix='student')
        if student_formset.is_valid():
            student_formset.save()
            return super(StudentUpdateView, self).post(self.request.POST)
        else:
            messages.error(request, 'Ошибка сохранения!')
            return self.render_to_response({'form': form, 'student_form': student_formset})

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


class GroupStudentListView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    template_name = 'diary/group_list.html'
    context_object_name = 'users_teachers'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager__group').filter(user_status=TEACHER)
        return queryset


class GroupDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    model = Group
    template_name = 'diary/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['students'] = User.objects.select_related('student__group').filter(student__group_id=self.kwargs['pk'])
        return context


class JournalLessonListView(LoginRequiredMixin, TeacherLessonPermissionsMixin, JournalMixin, ListView):
    template_name = 'diary/journal_lesson_list.html'
    context_object_name = 'marks'
    permission_denied_message = 'В доступе отказанно'

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.lesson = None
        self.group = None

    def get_queryset(self):
        group_student = Group.objects.select_related('group')
        self.group = get_object_or_404(group_student, id=self.kwargs['group_id'])
        self.lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])
        queryset = Journal.objects.select_related('group', 'lesson') \
            .filter(group_id=self.kwargs['group_id'], lesson_id=self.kwargs['lesson_id'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(JournalLessonListView, self).get_context_data(**kwargs)
        date_period = self.create_date_period_list()
        students = User.objects.select_related('student', 'student__group').filter(student__group=self.group)

        marks = Journal.objects.select_related('group', 'lesson') \
            .filter(created__in=date_period, lesson_id=self.lesson, group_id=self.group)

        context['date_period'] = date_period
        context['students'] = students
        context['marks_dict'] = self.create_scores_dict(date_period,
                                                        marks.values('id', 'student', 'mark', 'created'),
                                                        students, 'student')
        context['group'] = self.group
        context['lesson'] = self.lesson
        return context


class AddScore(LoginRequiredMixin, TeacherLessonPermissionsMixin, View):
    def post(self, request):
        mark_id = request.POST.get('journal_id')
        if mark_id == '0':
            mark_id = None
        mark_params = {
            'mark': request.POST.get('mark_value'),
            'group_id': request.POST.get('group'),
            'lesson_id': request.POST.get('lesson'),
            'student_id': request.POST.get('student'),
            'teacher_id': request.POST.get('teacher'),
            'mark_status_id': request.POST.get('mark_status'),
            'created': request.POST.get('mark_date'),
        }

        if mark_params['mark']:
            Journal.objects.update_or_create(id=mark_id, defaults=mark_params)
            return JsonResponse({'status': 'ok'})
        else:
            Journal.objects.get(id=mark_id).delete()
            return JsonResponse({'status': 'ok'})