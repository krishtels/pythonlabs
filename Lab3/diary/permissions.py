from datetime import datetime
from django.core.exceptions import PermissionDenied
from Lab3.settings import TEACHER, STUDENT
from .models import Teacher


class TeacherPermissionsMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def has_permissions(self):
        return self.request.user.is_superuser or self.request.user.user_status == TEACHER


class StudentPermissionsMixin(TeacherPermissionsMixin):
    def has_permissions(self):
        return self.request.user.is_superuser or self.request.user.user_status == STUDENT


class TeacherLessonPermissionsMixin(TeacherPermissionsMixin):
    def has_permissions(self):
        if self.request.method == 'POST':
            lesson_id = self.request.POST.get('lesson')
        else:
            lesson_id = self.kwargs['lesson_id']

        teacher = Teacher.objects.prefetch_related('lessons').filter(user=self.request.user, lessons=lesson_id).exists()
        return teacher or self.request.user.is_superuser


class JournalMixin:
    def create_date_period_list(self):
        day_delta = datetime.timedelta(days=1)
        try:
            start_date = datetime.datetime.strptime(self.request.GET.get('start-date'), '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(self.request.GET.get('end-date'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=15)
        return [start_date + i * day_delta for i in range((end_date - start_date).days + 1)]

    @staticmethod
    def create_scores_dict(date_period, marks, grouping_object, grouping_object_name):
        marks_dict = {}
        for date in date_period:
            marks_dict[date] = {}
            for obj in grouping_object:
                marks_dict[date][obj.id] = 0
                if marks:
                    for mark in marks:
                        if obj.id == mark[grouping_object_name] and date == mark['created']:
                            marks_dict[date][obj.id] = mark['mark']
                            break
        return marks_dict
