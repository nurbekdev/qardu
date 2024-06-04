import datetime

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields

from oauth.models import User


def get_permission_queryset(user):
    """
    Get the queryset of categories based on the user's permissions.
    """
    qs = Category.objects

    if user.is_superuser:
        return qs.all()

    return qs.filter(group__in=user.groups.all())


class StatisticsScientific(TranslatableModel):
    class Meta:
        verbose_name = _("Статистика научной деятельности")
        verbose_name_plural = _("Статистика научной деятельности")
        ordering = ("-created",)
        db_table = "statistics_scientific"

    translations = TranslatedFields(
        name=models.CharField(
            max_length=255, null=True, blank=True, verbose_name=_("Название")
        )
    )
    category_types = models.ManyToManyField(
        to="CategoryType", verbose_name=_("Типы категорий")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    objects = TranslatableManager()

    # def get_total_series(self):
    #     """Calculates the total series of points per academic year for recent four years."""
    #     series = []
    #
    #     academic_years = AcademicYear.objects.order_by("-from_date")[:4]
    #     for academic_year in academic_years:
    #         total_points = sum(
    #             category_type.get_total_points_categories_date(
    #                 from_date=academic_year.from_date, to_date=academic_year.to_date
    #             ) for category_type in self.category_types.all()
    #         )
    #         series.append({
    #             'year': academic_year.name,
    #             'total_points': round(total_points, 2)
    #         })
    #     return series

    def __str__(self):
        return self.safe_translation_getter("name", default="No Name")


class CategoryType(TranslatableModel):
    class Meta:
        verbose_name = _("Тип категории")
        verbose_name_plural = _("Типы категорий")
        ordering = ("translations__name",)
        db_table = "category_types"

    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_("Название"))
    )
    categories = models.ManyToManyField(
        "Category", verbose_name=_("Категории"), related_name="category_types"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    objects = TranslatableManager()

    def get_total_points_categories_date(self, from_date, to_date):
        """Calculates the total points for the category type within the specified date range."""
        categories = self.categories.annotate(
            total_points=models.Sum(
                models.Case(
                    models.When(
                        post__date__range=(from_date, to_date), then="post__points"
                    ),
                    default=0,
                    output_field=models.IntegerField(),
                )
            )
        )
        total_points = sum(
            cat.total_points * getattr(cat, "coefficient", 1) for cat in categories
        )
        return round(total_points, 2)

    def get_total_series(self):
        """Generates a series of total points per academic year starting from 2019."""
        series = []
        current_year = datetime.date.today().year
        start_year = 2019
        if datetime.date.today().month > 8:
            current_year += 1  # Adjust for the academic year if it's after September

        for year in range(start_year, current_year):
            from_date = datetime.date(year, 9, 1)
            to_date = datetime.date(year + 1, 8, 30)
            total_points = sum(
                category.get_total_points_date(from_date, to_date)
                for category in self.categories.all()
            )
            series.append(round(total_points, 2))
        return series

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class Category(TranslatableModel):
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ("translations__name", "group", "coefficient")
        db_table = "categories"

    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_("Название"))
    )
    is_delete = models.BooleanField(default=False, verbose_name=_("Удалено"))
    coefficient = models.FloatField(default=1, verbose_name=_("Коэффициент"))
    limit = models.IntegerField(null=True, blank=True, verbose_name=_("Лимит"))
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Группа")
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("Автор")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    objects = TranslatableManager()

    def get_total_points(self):
        return round(self.coefficient * self.post_set.count(), 2)

    def get_total_points_date(self, from_date, to_date):
        total_points = (
            self.post_set.filter(date__gte=from_date, date__lte=to_date)
            .distinct()
            .count()
        )
        return round(self.coefficient * total_points, 2)

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class AcademicPoints(models.Model):
    class Meta:
        verbose_name = _("Учебный балл")
        verbose_name_plural = _("Учебные баллы")
        ordering = ("-created",)
        db_table = "academic_points"

    academic_year = models.OneToOneField(
        to="posts.AcademicYear",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="academic_points",
        verbose_name=_("Учебный год"),
    )
    gt_150 = models.IntegerField(
        null=True, blank=True, default=0, verbose_name=_("Больше 150")
    )
    lt_150 = models.IntegerField(
        null=True, blank=True, default=0, verbose_name=_("Меньше 150")
    )
    lt_100 = models.IntegerField(
        null=True, blank=True, default=0, verbose_name=_("Меньше 100")
    )
    lt_55 = models.IntegerField(
        null=True, blank=True, default=0, verbose_name=_("Меньше 55")
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    def __str__(self):
        return f"{self.academic_year} | {self.gt_150} | {self.lt_150} | {self.lt_100} | {self.lt_55}"
