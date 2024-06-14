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
        verbose_name = _("O'quv yili")
        verbose_name_plural = _("O'quv yillari")
        ordering = ("-from_date",)
        db_table = "academic_years"

    years = models.CharField(
        verbose_name=_("Yil"), max_length=64, null=True, blank=True
    )
    from_date = models.DateField(verbose_name=_("Boshlanish sanasi"))
    to_date = models.DateField(verbose_name=_("Tugash sanasi"))

    def save(self, *args, **kwargs):
        self.years = f"{self.from_date.year}-{self.to_date.year}"
        super(AcademicYear, self).save(*args, **kwargs)
        if not AcademicPoints.objects.filter(academic_year=self).exists():
            AcademicPoints.objects.create(academic_year=self)

    def clean(self):
        if self.from_date >= self.to_date:
            raise forms.ValidationError(
                {
                    "from_date": _(
                        "Bu maydon Tugash sanasi maydonidan kichik bo'lishi kerak"
                    ),
                    "to_date": _("Bu maydon Boshlanish sanasi maydonidan katta bo'lishi kerak"),
                },
            )

    def __str__(self):
        return f"{self.id} | {self.years}"


class Post(TranslatableModel):
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Postlar")
        ordering = ("-date",)
        db_table = "posts"

    STATUS_CHOICES = (
        (1, _("Ko'rib chiqilmoqda")),
        (2, _("Tasdiqlangan")),
    )
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Sarlavha"), max_length=255),
        body=models.TextField(verbose_name=_("Matn")),
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=1, verbose_name=_("Holat")
    )
    indexing = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Indeksatsiya")
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_("Kategoriya")
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("O'qituvchi"),
    )
    date = models.DateField(verbose_name=_("Sana"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan"))
    academic_years = models.ForeignKey(
        to=AcademicYear,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("O'quv yili"),
    )

    objects = TranslatableManager()

    def save(self, *args, **kwargs):
        if self.date:
            academic_year = AcademicYear.objects.filter(
                from_date__lte=self.date, to_date__gte=self.date
            ).first()
        else:
            today = date.today()
            academic_year = AcademicYear.objects.filter(
                from_date__lte=today, to_date__gte=today
            ).first()

        self.academic_years = academic_year
        super(Post, self).save(*args, **kwargs)

    def get_academic_year_display(self):
        if int(self.date.strftime("%-m")) < 9:
            year = f'{int(self.date.strftime("%Y")) - 1} - {self.date.strftime("%Y")}'
        else:
            year = f'{self.date.strftime("%Y")} - {int(self.date.strftime("%Y")) + 1}'
        return year

    def __str__(self):
        return f"{self.teacher} | {self.safe_translation_getter('title', any_language=True)} | {self.category}"


def upload_to_documents(_, filename):
    return f"documents/{timezone.now().timestamp()}_{filename}"


class Document(models.Model):
    class Meta:
        verbose_name = _("Hujjat")
        verbose_name_plural = _("Hujjatlar")
        db_table = "documents"

    file = models.FileField(upload_to=upload_to_documents, verbose_name=_("Fayl"))
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, verbose_name=_("Post"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan"))

    def __str__(self):
        return f"{self.id} | {self.file}"
