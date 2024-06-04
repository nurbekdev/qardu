from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import AcademicPoints, Category, CategoryType, StatisticsScientific


@admin.register(CategoryType)
class CategoryTypeAdmin(TranslatableAdmin):
    pass


@admin.register(StatisticsScientific)
class StatisticsScientificAdmin(TranslatableAdmin):
    pass


@admin.register(AcademicPoints)
class AcademicPointsAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    pass
