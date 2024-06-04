from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields


def upload_to_profile(_, filename):
    return f"profiles/{timezone.now().timestamp()}_{filename}"


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_teacher(
        self, email, first_name, last_name, fathers_name=None, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_teacher", True)
        return self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            fathers_name=fathers_name,
            **extra_fields,
        )

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("-created",)
        db_table = "users"

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    email = models.EmailField(_("Email"), unique=True)

    first_name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name=_("Имя")
    )
    last_name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name=_("Фамилия")
    )
    fathers_name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name=_("Отчество")
    )
    image_url = models.URLField(
        blank=True, null=True, max_length=255, verbose_name=_("Изображение")
    )
    employee_id_number = models.IntegerField(
        blank=True, null=True, verbose_name=_("ID номер")
    )

    birth_date = models.DateField(
        null=True, blank=True, verbose_name=_("Дата рождения")
    )
    phone = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_("Телефон")
    )

    is_teacher = models.BooleanField(default=False, verbose_name=_("Преподаватель"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    last_login = models.DateTimeField(auto_now=True, verbose_name=_("Последний вход"))

    objects = CustomUserManager()

    def __str__(self):
        if self.fathers_name:
            return f"{self.first_name} {self.last_name} {self.fathers_name}".upper()
        return f"{self.first_name} {self.last_name}".upper()

    def get_full_name(self):
        return self.__str__()

    def get_short_name(self):
        if self.fathers_name:
            return (
                f"{self.first_name} {self.last_name[0]}.{self.fathers_name[0]}.".upper()
            )
        return f"{self.first_name} {self.last_name[0]}.".upper()

    @property
    def is_staff(self):
        return self.is_superuser


class TeacherLevel(TranslatableModel):
    class Meta:
        verbose_name = _("Уровень преподавателя")
        verbose_name_plural = _("Уровни преподавателей")
        ordering = ("translations__name",)

    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_("Уровень преподавателя"))
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    objects = TranslatableManager()

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class AcademicLevel(TranslatableModel):
    class Meta:
        verbose_name = _("Ученое звание")
        verbose_name_plural = _("Ученые звания")
        ordering = ("translations__name",)

    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_("Ученое звание"))
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    objects = TranslatableManager()

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class Group(TranslatableModel):
    class Meta:
        verbose_name = _("Группа")
        verbose_name_plural = _("Группы")
        db_table = "groups"

    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_("Название"))
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    objects = TranslatableManager()

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class Teacher(models.Model):
    class Meta:
        verbose_name = _("Преподаватель")
        verbose_name_plural = _("Преподаватели")
        db_table = "teachers"

    STATUS = ((1, "Штатный"), (2, "Совместитель"), (3, "Выбыл"), (4, "Почасовик"))

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="teacher",
        verbose_name=_("Пользователь"),
    )
    department = models.ForeignKey(
        to="home.Department",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Кафедра"),
        related_name="teachers",
    )

    uuid = models.UUIDField(unique=True, editable=False, verbose_name=_("UUID"))

    position = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Должность"
    )

    level = models.ForeignKey(
        to=TeacherLevel,
        on_delete=models.PROTECT,
        verbose_name="Уровень",
        null=True,
        blank=True,
    )

    academic_title = models.ForeignKey(
        to=AcademicLevel,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Ученое звание",
    )

    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    phone = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Телефон"
    )

    status = models.IntegerField(choices=STATUS, default=1, verbose_name="Статус")

    group = models.ForeignKey(
        to=Group,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Группа",
    )

    ext_date = models.DateField(null=True, blank=True, verbose_name="Дата увольнения")

    objects = models.Manager()

    def __str__(self):
        return self.user.get_full_name()

    def get_total_points(self):
        total_points = self.post_set.aggregate(
            total=models.Sum("category__coefficient")
        )["total"]
        return round(total_points, 1)

    def get_total_points_by_period(self, from_date, to_date):
        total_points = self.post_set.filter(
            (Q(date__gte=from_date) & Q(date__lte=to_date)) | Q(category__id=29)
        ).aggregate(total=models.Sum("category__coefficient"))["total"]

        return round(total_points, 1)
