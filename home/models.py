from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableManager, TranslatableModel, TranslatedFields

from category.models import Category


def upload_to_departments(_, filename):
    return f"departments/{timezone.now().timestamp()}_{filename}"


class Department(TranslatableModel):
    class Meta:
        verbose_name = _("Кафедра")
        verbose_name_plural = _("Кафедры")
        db_table = "departments"
        ordering = ("translations__name",)

    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_("Название кафедры"))
    )
    image = models.ImageField(
        upload_to=upload_to_departments,
        null=True,
        blank=True,
        verbose_name=_("Изображение"),
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    objects = TranslatableManager()

    def teachers_count(self):
        return self.teachers.exclude(status=3).count()

    def get_total_points(self):
        total_points = self.teachers.exclude(status=3).aggregate(
            total=models.Sum("post__category__coefficient")
        )["total"]

        return round(total_points, 1)

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class ControlLimit(models.Model):
    class Meta:
        verbose_name = "Контрольный предел"
        verbose_name_plural = "Контрольные пределы"
        ordering = ("low_limit", "high_limit")

    low_limit = models.IntegerField(verbose_name="Нижний предел")
    high_limit = models.IntegerField(verbose_name="Верхний предел")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )

    def __str__(self):
        return f"{self.low_limit} - {self.high_limit}"
