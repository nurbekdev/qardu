import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.views import generic

from category.models import Category
from home.models import Department
from oauth.models import AcademicLevel, Teacher, TeacherLevel
from posts.models import AcademicYear, Post


class DepartmentAdminListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 12
    model = Department
    queryset = Department.objects.all()
    template_name = "administrator/departments/list.html"


class TeacherAdminListView(LoginRequiredMixin, generic.ListView):
    model = Teacher
    queryset = Teacher.objects.all()
    paginate_by = 12
    template_name = "administrator/teachers/list.html"

    def get_queryset(self):
        teachers = Teacher.objects.all().order_by(
            "last_name", "first_name", "father_name"
        )
        if self.request.GET.get("name"):
            name = self.request.GET.get("name")
            teachers = teachers.filter(
                Q(first_name__icontains=name)
                | Q(last_name__icontains=name)
                | Q(father_name__contains=name)
            )

        if self.request.GET.get("select-status"):
            teachers = teachers.filter(status=self.request.GET.get("select-status"))

        return teachers

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherAdminListView, self).get_context_data(**kwargs)
        context["teacher_level_list"] = TeacherLevel.objects.all()
        context["teacher_academic_level_list"] = AcademicLevel.objects.all()
        context["department_list"] = Department.objects.all()
        return context


class TeacherAdminDetailView(LoginRequiredMixin, generic.DetailView):
    model = Teacher
    queryset = Teacher.objects.all()
    template_name = "administrator/teachers/detail.html"


class TeacherLevelAdminListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 12
    model = TeacherLevel
    template_name = "administrator/levels/list.html"


class TeacherPublicListView(generic.ListView):
    template_name = "public/teachers/list.html"
    model = Teacher
    paginate_by = 12

    def get_queryset(self):
        teachers = Teacher.objects.all()
        today = datetime.date.today()
        academic_id = self.request.GET.get("academic_year")
        if academic_id:
            academic_year = AcademicYear.objects.filter(id=int(academic_id)).last()
        else:
            academic_year = AcademicYear.objects.filter(
                from_date__lte=today, to_date__gte=today
            ).last()

        if not academic_year:
            return teachers

        start_date = academic_year.from_date
        end_date = academic_year.to_date
        teachers = teachers.filter(
            Q(post__date__gte=start_date) & Q(post__date__lte=end_date)
            | Q(post__category__id=29)
        )

        if self.request.GET.get("department"):
            teachers = teachers.filter(department=self.request.GET.get("department"))
        if self.request.GET.get("uuid"):
            teachers = teachers.filter(uuid=self.request.GET.get("uuid"))
        if self.request.GET.get("level"):
            teachers = teachers.filter(level=self.request.GET.get("level"))
        if self.request.GET.get("name"):
            name = self.request.GET.get("name")
            teachers = teachers.filter(
                Q(first_name__icontains=name)
                | Q(last_name__icontains=name)
                | Q(father_name__contains=name)
            )
        if self.request.GET.get("order_by") == "points_asc":
            return teachers.annotate(
                total_points=Sum("post__category__coefficient")
            ).order_by("total_points")
        if self.request.GET.get("order_by") == "points_desc":
            return teachers.annotate(
                total_points=Sum("post__category__coefficient")
            ).order_by("-total_points")
        return teachers.annotate(
            total_points=Sum("post__category__coefficient")
        ).order_by(
            "user__last_name", "user__first_name", "user__father_name", "-total_points"
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherPublicListView, self).get_context_data(**kwargs)
        context["department_list"] = Department.objects.all()
        context["teacher_level_list"] = TeacherLevel.objects.all()
        context["academic_year_list"] = AcademicYear.objects.all()
        today = datetime.date.today()

        current_academic_year = AcademicYear.objects.filter(
            from_date__lte=today, to_date__gte=today
        ).last()
        if current_academic_year:
            context["current_academic_year"] = current_academic_year.id

        return context


class TeacherPublicDetailView(generic.DetailView):
    template_name = "public/teachers/detail.html"
    model = Teacher

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherPublicDetailView, self).get_context_data(**kwargs)
        context["teacher_list"] = Teacher.objects.all()
        context["post_list"] = self.object.post_set.order_by("-date")
        context["category_list"] = []
        for category in Category.objects.filter(post__teacher=self.object).distinct():
            context["category_list"].append(
                {
                    "category": category,
                    "count": category.post_set.filter(teacher=self.object).count,
                }
            )
        return context


class DepartmentPublicListView(generic.ListView):
    template_name = "public/departments/list.html"
    model = Department
    paginate_by = 12

    def get_queryset(self):
        department_list = Department.objects.all()
        today = datetime.date.today()
        academic_id = self.request.GET.get("academic_year")
        if academic_id:
            academic_year = AcademicYear.objects.filter(id=int(academic_id)).last()
        else:
            academic_year = AcademicYear.objects.filter(
                from_date__lte=today, to_date__gte=today
            ).last()

        if not academic_year:
            return department_list

        start_date = academic_year.from_date
        end_date = academic_year.to_date

        department_list = department_list.filter(
            Q(teachers__post__date__gte=start_date)
            & Q(teachers__post__date__lte=end_date)
            | Q(teachers__post__category__id=29)
        ).distinct()
        department_list = department_list.annotate(
            total_coefficient=Sum("teachers__post__category__coefficient"),
            academ_points=Sum(
                "teachers__post__category__coefficient",
                # filter=Q(teacher__post__category__group=Group.objects.get(id=3)),
            ),
            scien_points=Sum(
                "teachers__post__category__coefficient",
                # filter=Q(teacher__post__category__group=Group.objects.get(id=2)),
            ),
            org_points=Sum(
                "teachers__post__category__coefficient",
                # filter=Q(teacher__post__category__group=Group.objects.get(id=1)),
            ),
        )

        if self.request.GET.get("name"):
            return department_list.filter(
                name__icontains=self.request.GET.get("name")
            ).order_by("-total_coefficient")
        return department_list.order_by("-total_coefficient")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DepartmentPublicListView, self).get_context_data(**kwargs)
        context["academic_year_list"] = AcademicYear.objects.all()
        today = datetime.date.today()
        current_academic_year = AcademicYear.objects.filter(
            from_date__lte=today, to_date__gte=today
        ).last()
        if current_academic_year:
            context["current_academic_year"] = current_academic_year.id
        return context


class DepartmentPublicDetailView(generic.DetailView):
    template_name = "public/departments/detail.html"
    model = Department

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DepartmentPublicDetailView, self).get_context_data(**kwargs)
        context["department_list"] = Department.objects.all()
        context["post_list"] = Post.objects.filter(
            teacher__department=self.object
        ).order_by("-date")

        context["year_list"] = sorted(
            set(
                Post.objects.filter(
                    teacher__in=self.object.teacher_set.all()
                ).values_list("date__year", flat=True)
            )
        )
        context["category_list"] = []
        for category in Category.objects.filter(
            post__teacher__department=self.object
        ).distinct():
            context["category_list"].append(
                {
                    "category": category,
                    "count": category.post_set.filter(teacher__department=self.object)
                    .distinct()
                    .count(),
                }
            )
        return context
