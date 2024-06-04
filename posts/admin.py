from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import AcademicYear, Document, Post


@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    pass


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("years", "from_date", "to_date")
    search_fields = ("years",)
    list_display_links = ("years",)

    fields = ("from_date", "to_date")
