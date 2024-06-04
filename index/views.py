import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views import generic

from oauth.models import Teacher
from posts.models import AcademicYear, Post


class BaseIndexView(generic.TemplateView):
    """Base view to handle common operations for both Admin and Public views."""

    def get_academic_year(self):
        """Retrieve and return the current or selected academic year and teacher list sorted by total points."""
        current_academic_year_id = self.request.GET.get("academic_year")
        if current_academic_year_id:
            current_academic_year = AcademicYear.objects.filter(
                id=current_academic_year_id
            ).last()
        else:
            today = datetime.date.today()
            current_academic_year = AcademicYear.objects.filter(
                from_date__lte=today, to_date__gte=today
            ).last()

        if current_academic_year:
            teachers = Teacher.objects.annotate(
                total_points=Sum("post__category__coefficient")
            ).order_by("-total_points")
        else:
            teachers = (
                Teacher.objects.none()
            )  # Handle the case where no academic year is found

        return current_academic_year, teachers[:40]

    @staticmethod
    def generate_month_list(from_date, to_date):
        """Generate a list of months between from_date and to_date."""
        month_list = []
        while from_date <= to_date:
            month_list.append(from_date.strftime("%b"))
            from_date += datetime.timedelta(
                days=31
            )  # Move to the next month approximately
        return month_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["academic_year_list"] = AcademicYear.objects.all()

        current_academic_year, teachers = self.get_academic_year()
        if current_academic_year:
            month_list = self.generate_month_list(
                current_academic_year.from_date, current_academic_year.to_date
            )
        else:
            month_list = []

        context.update(
            {
                "month_list": month_list,
                "teacher_list": teachers,
                "current_academic_year": (
                    current_academic_year.id if current_academic_year else None
                ),
            }
        )
        return context


class IndexAdminView(LoginRequiredMixin, BaseIndexView):
    template_name = "administrator/index.html"


class IndexPublicView(BaseIndexView):
    template_name = "public/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = Post.objects.order_by("-id")[:40]
        return context
