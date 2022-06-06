from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from diary.forms import ScoreCreateForm
from diary.models import Group, Lesson, Score
from diary.permissions import ScoreJournalMixin
from lab3.settings import TEACHER
from people.models import User, Teacher
from people.permissions import TeacherPermissionsMixin, TeacherLessonPermissionsMixin
from django.shortcuts import get_object_or_404, render, redirect


class GroupStudentListView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    template_name = 'diary/group_list.html'
    context_object_name = 'users_teachers'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager').filter(user_status=TEACHER)
        return queryset


class GroupStudentDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    model = Group
    template_name = 'diary/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super(GroupStudentDetailView, self).get_context_data(**kwargs)
        context['students'] = User.objects.select_related('student__group')\
            .filter(student__group_id=self.kwargs['pk'])
        return context


class ScoreLessonListView(LoginRequiredMixin, TeacherLessonPermissionsMixin, ScoreJournalMixin, ListView):
    template_name = 'diary/journal_lesson_list.html'
    context_object_name = 'scores'
    permission_denied_message = 'В доступе отказанно'

    def get_queryset(self):
        group_student = Group.objects.all()
        self.group = get_object_or_404(group_student, id=self.kwargs['group_id'])
        self.lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])
        queryset = Score.objects.select_related('group', 'lesson')\
            .filter(group_id=self.kwargs['group_id'], lesson_id=self.kwargs['lesson_id'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ScoreLessonListView, self).get_context_data(**kwargs)
        date_period = self.create_date_period_list()
        students = User.objects.select_related('student', 'student__group').filter(student__group=self.group)
        scores = Score.objects.select_related('group', 'lesson')\
            .filter(created__in=date_period, lesson_id=self.lesson, group_id=self.group)

        context['date_period'] = date_period
        context['students'] = students
        context['scores_dict'] = self.create_scores_dict(date_period,
                                                         scores.values('id', 'student', 'score', 'created'),
                                                         students, 'student')
        context['group'] = self.group
        context['lesson'] = self.lesson
        return context


class AddScoreView(LoginRequiredMixin, TeacherPermissionsMixin, View):
    template_name = 'diary/score_create.html'
    success_url = reverse_lazy('score_lesson')
    success_message = 'Оценка успешно добавлена.'
    form_class = ScoreCreateForm

    def get(self, request, *args, **kwargs):
        u = self.request.path.split('/')
        group = Group.objects.get(id=u[-4])
        form = ScoreCreateForm(group)
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return render(request, "diary/score_create.html", context=context)

    def post(self, request, *args, **kwargs):
        u = self.request.path.split('/')
        group = Group.objects.get(id=u[-4])
        form = self.form_class(group, request.POST)
        context = self.get_context_data(**kwargs)

        if form.is_valid():
            score = form.save(commit=False)
            mark = score.score

            score = Score.objects.get_or_create(
                student=score.student,
                lesson=Lesson.objects.get(id=u[-3]),
                created=score.created
            )[0]
            score.group = Group.objects.get(id=u[-4])
            score.teacher = User.objects.get(id=request.user.id)
            score.score = mark
            score.save()

            return redirect(reverse_lazy("score_lesson", kwargs={
                'group_id': score.group.pk,
                'lesson_id': score.lesson.pk
            }))
        else:
            return render(request, "diary/score_create.html", context={
                'form': form,
                **context
        })

    def get_context_data(self, **kwargs):
        context = {}
        u = self.request.path.split('/')
        lesson = Lesson.objects.get(id=u[-3])
        group = Group.objects.get(id=u[-4])
        teacher = Teacher.objects.filter(user_id=self.request.user.id)
        context['lesson'] = lesson
        context['group'] = group
        context['teacher'] = teacher
        return context

