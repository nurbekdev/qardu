from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HomeConfig(AppConfig):
    name = "home"
    verbose_name = _("Общее")
    verbose_name_plural = _("Общее")
