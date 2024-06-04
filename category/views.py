from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views import generic

from category.models import Category, StatisticsScientific, get_permission_queryset
from posts.models import AcademicYear


class CategoryAdminListView(LoginRequiredMixin, generic.ListView):
    template_name = "administrator/categories/list.html"
    model = Category
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        resp = super(CategoryAdminListView, self).get_context_data(**kwargs)
        resp["group_list"] = Group.objects.all()
        return resp

    def get_queryset(self):
        categories = get_permission_queryset(self.request.user).filter(is_delete=False)
        if self.request.GET.get("select-group"):
            return categories.filter(group=self.request.GET.get("select-group"))
        if self.request.GET.get("name"):
            return categories.filter(name__icontains=self.request.GET.get("name"))
        return categories


class StatisticsScientificView(generic.ListView):
    template_name = "public/posts/static_scientific.html"
    model = StatisticsScientific

    def get_context_data(self, *, object_list=None, **kwargs):
        resp = super(StatisticsScientificView, self).get_context_data(**kwargs)
        status_teachers = []
        academic_years = AcademicYear.objects.all()[:4]
        for academic_year in academic_years:

            status = {
                "year": f"{academic_year.years}",
                "gt_150": academic_year.academic_points.gt_150,
                "lt_150": academic_year.academic_points.lt_150,
                "lt_100": academic_year.academic_points.lt_100,
                "lt_55": academic_year.academic_points.lt_55,
            }

            status_teachers.insert(0, status)
        resp["status_teachers"] = status_teachers
        return resp
