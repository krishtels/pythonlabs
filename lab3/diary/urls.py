from django.urls import path, include

from .views import GroupStudentListView, GroupStudentDetailView, ScoreLessonListView, AddScoreView, LessonCreateView, \
    GroupCreateView, PermissionView

urlpatterns = [
    path('people/', include('people.urls')),
    path('groups/', GroupStudentListView.as_view(), name='group_student_list'),
    path('permission_denied', PermissionView.as_view(), name='permission_denied'),
    path('groups/add_group', GroupCreateView.as_view(), name='group_add'),
    path('group/<int:pk>/', GroupStudentDetailView.as_view(), name='group_student_detail'),
    path('group/add_lesson', LessonCreateView.as_view(), name='lesson_add'),
    path('<int:group_id>/<int:lesson_id>/', ScoreLessonListView.as_view(), name='score_lesson'),
    path('<int:group_id>/<int:lesson_id>/addscore/', AddScoreView.as_view(), name='add_score'),
]
