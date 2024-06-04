from django.contrib import admin
from parler.admin import TranslatableAdmin

from home.models import ControlLimit, Department


@admin.register(Department)
class DepartmentAdmin(TranslatableAdmin):
    pass


@admin.register(ControlLimit)
class ControlLimitAdmin(admin.ModelAdmin):
    pass
