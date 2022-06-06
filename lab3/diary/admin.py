from django.contrib import admin
from .models import Lesson, Group, Score


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('number', )


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'score', 'created', 'updated', 'group')
    list_filter = ('created', 'score', 'lesson', 'group')
    search_fields = ('student__first_name', 'student__last_name')
    save_on_top = True
