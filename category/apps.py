from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoryConfig(AppConfig):
    name = "category"
    verbose_name = _("Категория")
    verbose_name_plural = _("Категории")
