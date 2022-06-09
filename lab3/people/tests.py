from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.test import TestCase, RequestFactory

from diary.models import Group, Lesson
from lab3.settings import TEACHER, STUDENT
from people.models import User, Student
from people.views import TeacherListView, TeacherDetailView, StudentCreateView, StudentUpdateView, StudentDetailView, \
    StudentAccountDetailView


class UserTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.lesson = Lesson.objects.create(name='lesson name')
        self.group = Group.objects.create(number='053501')
        self.group.lessons.add(self.lesson)
        self.teacher = User.objects.create_user(
            username='jacob', email='jacob@mail.ru', password='top_secret', user_status=TEACHER)
        self.student = User.objects.create_user(
            username='ivan', email='ivan@mail.ru', password='top_secret', user_status=STUDENT)
        self.stud_user = Student.objects.create(
            user=self.student, group=self.group
        )

    def test_teacher_list(self):
        request = self.factory.get('/diary/teacher/')
        request.user = self.teacher
        response = TeacherListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_teacher_detail(self):
        request = self.factory.get('/diary/teacher')
        request.user = self.teacher
        response = TeacherDetailView.as_view()(request, pk=self.teacher.pk)
        self.assertEqual(response.status_code, 200)

    def test_student_create(self):
        request = self.factory.post('/diary/student/add/')
        request.user = self.teacher
        response = StudentCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_student_update(self):
        request = self.factory.post('/diary/student/update/')
        request.user = self.teacher
        response = StudentUpdateView.as_view()(request, pk=self.student.pk)
        self.assertEqual(response.status_code, 200)

    def test_student_detail(self):
        request = self.factory.get('/diary/student/info/')
        request.user = self.teacher
        response = StudentDetailView.as_view()(request, pk=self.student.pk)
        self.assertEqual(response.status_code, 200)

    def test_student_account(self):
        request = self.factory.get('/diary/student/')
        request.user = self.student
        response = StudentAccountDetailView.as_view()(request)
        self.assertEqual(response.status_code, 200)




