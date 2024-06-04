from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "oauth"
    verbose_name = _("Авторизация")
