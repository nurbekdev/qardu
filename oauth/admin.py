from django.contrib import admin
from django.contrib.auth.models import Group as AuthGroup
from parler.admin import TranslatableAdmin

from oauth.models import AcademicLevel, Group, Teacher, TeacherLevel, User

admin.site.unregister(AuthGroup)


@admin.register(User)
class UserProfile(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherProfile(admin.ModelAdmin):
    pass


@admin.register(TeacherLevel)
class TeacherLevelAdmin(TranslatableAdmin):
    pass


@admin.register(AcademicLevel)
class AcademicLevelAdmin(TranslatableAdmin):
    pass


@admin.register(Group)
class GroupAdmin(TranslatableAdmin):
    pass
