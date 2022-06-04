from django.urls import path
from .views import TeacherListView, TeacherDetailView, StudentDetailView, StudentAccountDetailView, \
    StudentUpdateView, StudentCreateView, GroupStudentListView, GroupDetailView, JournalLessonListView, AddScore


urlpatterns = [
    path('teacher/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/info/<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('student/add/', StudentCreateView.as_view(), name='student_add'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('student/info/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/', StudentAccountDetailView.as_view(), name='student_lk'),
    path('groups/', GroupStudentListView.as_view(), name='group_student_list'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group_student_detail'),
    path('<int:group_id>/<int:lesson_id>/', JournalLessonListView.as_view(), name='journal_lesson'),
    path('addscore/', AddScore.as_view(), name='add_score'),
]
