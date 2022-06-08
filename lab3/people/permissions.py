import logging

from django.shortcuts import redirect

from lab3.settings import TEACHER, STUDENT
from .models import Teacher


logger = logging.getLogger('main')


class TeacherPermissionsMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            logger.info('User tried to get access to the page he cant use')
            return redirect('permission_denied')

        return super().dispatch(request, *args, **kwargs)

    def has_permissions(self):
        return self.request.user.is_superuser or self.request.user.user_status == TEACHER


class StudentPermissionsMixin(TeacherPermissionsMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            logger.info('User tried to get access to the page he cant use')
            return redirect('permission_denied')

        return super().dispatch(request, *args, **kwargs)

    def has_permissions(self):
        return self.request.user.is_superuser or self.request.user.user_status == STUDENT


class SuperUserPermissionsMixin(TeacherPermissionsMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            logger.info('User tried to get access to the page he cant use')
            return redirect('permission_denied')

        return super().dispatch(request, *args, **kwargs)

    def has_permissions(self):
        return self.request.user.is_superuser


class TeacherLessonPermissionsMixin(TeacherPermissionsMixin):
    message = 'You are not allowed here'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            logger.info('User tried to get access to the page he cant use')
            return redirect('permission_denied')

        return super().dispatch(request, *args, **kwargs)

    def has_permissions(self):
        if self.request.method == 'POST':
            lesson_id = self.request.POST.get('lesson')

        else:
            lesson_id = self.kwargs['lesson_id']

        teacher = Teacher.objects.prefetch_related('lessons').filter(user=self.request.user, lessons=lesson_id).exists()
        return teacher or self.request.user.is_superuser


