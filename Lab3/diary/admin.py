from django.contrib import admin
from .models import User, Teacher, Student, Journal, Group, RatingItemStatus, Lesson


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'sex', 'user_status', 'username']
    list_filter = ('user_status',)
    search_fields = ('get_full_name', 'username')
    save_on_top = True
    fields = ('date_joined', 'last_login', 'username', 'password', 'email', 'user_status', 'first_name', 'last_name',
              'birth_date', 'sex', 'photo', 'description', 'is_superuser', 'groups')

    def get_full_name(self, obj):
        return f'{obj.last_name} {obj.first_name}'

    get_full_name.short_description = 'Полное имя'
    get_full_name.admin_order_field = 'last_name'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'group_manager', 'position', 'user')
    list_filter = ('group_manager',)
    search_fields = ('get_full_name',)

    def get_full_name(self, obj):
        return f'{obj.user.last_name} {obj.user.first_name}'

    get_full_name.short_description = 'Полное имя'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'group', 'user')
    list_filter = ('group',)
    search_fields = ('get_full_name',)

    def get_full_name(self, obj):
        return f'{obj.user.last_name} {obj.user.first_name}'

    get_full_name.short_description = 'Полное имя'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Group)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(RatingItemStatus)
class RatingItemStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'score', 'created', 'group')
    list_filter = ('created', 'score', 'lesson', 'group')
    search_fields = ('student__first_name', 'student__last_name')
    save_on_top = True

