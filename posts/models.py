from datetime import date

from django.db import models
from django.forms import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields

from category.models import AcademicPoints, Category
from oauth.models import Teacher


class AcademicYear(models.Model):
    class Meta:
        verbose_name = _("Учебный год")
        verbose_name_plural = _("Учебные года")
        ordering = ("-from_date",)
        db_table = "academic_years"

    years = models.CharField(
        verbose_name=_("Год"), max_length=64, null=True, blank=True
    )
    from_date = models.DateField(verbose_name=_("Дата начала"))
    to_date = models.DateField(verbose_name=_("Дата окончания"))

    def save(self, *args, **kwargs):
        self.years = f"{self.from_date.year}-{self.to_date.year}"
        super(AcademicYear, self).save(*args, **kwargs)
        AcademicPoints.objects.create(academic_year=self)

    def clean(self):
        if self.from_date >= self.to_date:
            raise forms.ValidationError(
                {
                    "from_date": _(
                        "Это поле должно быть меньше чем поле Дата окончания"
                    ),
                    "to_date": _("Это поле должно быть больше чем поле Дата начала"),
                },
            )

    def __str__(self):
        return f"{self.id} | {self.years}"


class Post(TranslatableModel):
    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")
        ordering = ("-date",)
        db_table = "posts"

    STATUS_CHOICES = (
        (1, _("На рассмотрении")),
        (2, _("Одобрено")),
    )
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Заголовок"), max_length=255),
        body=models.TextField(verbose_name=_("Текст")),
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=1, verbose_name=_("Статус")
    )
    indexing = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Индексация")
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_("Категория")
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Преподаватель"),
    )
    date = models.DateField(verbose_name=_("Дата"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))
    academic_years = models.ForeignKey(
        to=AcademicYear,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Учебный год"),
    )

    objects = TranslatableManager()

    def save(self, *args, **kwargs):
        academic_year = AcademicYear.objects.last()

        if self.date:
            academic_year = academic_year.filter(
                from_date__lte=self.date, to_date__gte=self.date
            )
        else:
            today = date.today()
            academic_year = academic_year.filter(
                from_date__lte=today, to_date__gte=today
            )
        self.academic_years = academic_year
        super(Post, self).save(*args, **kwargs)

    def academic_year(self):
        if int(self.date.strftime("%-m")) < 9:
            year = f'{int(self.date.strftime("%Y")) - 1} - {self.date.strftime("%Y")}'
            return year

        elif int(self.date.strftime("%-m")) > 8:
            year = f'{self.date.strftime("%Y")} - {int(self.date.strftime("%Y")) + 1}'
            return year

    def __str__(self):
        return f"{self.teacher} | {self.safe_translation_getter('title', any_language=True)} | {self.category}"


def upload_to_documents(_, filename):
    return f"documents/{timezone.now().timestamp()}_{filename}"


class Document(models.Model):
    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Документы")
        db_table = "documents"

    file = models.FileField(upload_to=upload_to_documents, verbose_name=_("Файл"))
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, verbose_name=_("Пост"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    def __str__(self):
        return f"{self.id} | {self.file}"
