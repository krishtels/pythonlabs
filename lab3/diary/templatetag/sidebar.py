from django import template
from people.models import Teacher, User


register = template.Library()


@register.inclusion_tag('people/student_sidebar.html', name='student_sidebar')
def student_sidebar(user):
    group_student = User.objects.select_related('student__group').filter(pk=user.id)
    user_group_manager = User.objects.select_related('teacher')\
        .filter(teacher__group_manager=group_student.student.group_id)
    return {'user': user, 'user_group_manager': user_group_manager}


@register.inclusion_tag('people/teacher_sidebar.html', name='teacher_sidebar')
def teacher_sidebar(user):
    teacher = Teacher.objects.filter(user=user.id)
    return {'teacher': teacher, 'user': user}

