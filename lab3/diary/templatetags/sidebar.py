from django import template

from people.models import Teacher


register = template.Library()


@register.inclusion_tag('people/student_sidebar.html', name='student_sidebar')
def student_sidebar(user):
    return {'user': user}


@register.inclusion_tag('people/teacher_sidebar.html', name='teacher_sidebar')
def teacher_sidebar(user):
    teacher = Teacher.objects.filter(user=user.id)
    return {'teacher': teacher, 'user': user}

