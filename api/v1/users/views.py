from datetime import date

from django.contrib.auth.models import Group
from django.db.models import FloatField, Q, Sum
from django.db.models.functions import Coalesce
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from home.models import ControlLimit
from oauth.models import Teacher, TeacherLevel
from posts.models import AcademicYear, Post

from ..posts.paginations import MyLimitOffsetPagination
from . import serializers
from .serializers import TeacherStatisticSerializer


class CreateTeacherApiView(generics.CreateAPIView):
    """
    Create teacher
    """

    queryset = Teacher.objects.all()
    model = Teacher
    serializer_class = serializers.TeacherSerializer


class TeacherListApiView(generics.ListAPIView):
    """
    List of teachers
    """

    serializer_class = TeacherStatisticSerializer
    pagination_class = MyLimitOffsetPagination

    def get_queryset(self):
        academic_year = self.get_academic_year()
        return self.get_filtered_teachers(academic_year)

    def get_academic_year(self):
        """Retrieve the specified academic year or the current one if not specified."""
        academic_id = self.request.GET.get("academic_year")
        today = date.today()
        if academic_id:
            try:
                return AcademicYear.objects.get(id=academic_id)
            except AcademicYear.DoesNotExist:
                pass  # Allow fallback to default if specified academic year does not exist

        return AcademicYear.objects.filter(
            from_date__lte=today, to_date__gte=today
        ).last()

    @staticmethod
    def get_filtered_teachers(academic_year):
        """Annotate and filter teachers based on the academic year and other conditions."""
        teachers = (
            Teacher.objects.annotate(
                total_point=Coalesce(
                    Sum(
                        "post__category__coefficient",
                        filter=Q(post__academic_years=academic_year)
                        | Q(post__category__id=29),  # TODO: What is 29?
                    ),
                    0,
                    output_field=FloatField(),
                )
            )
            .exclude(status=3)
            .order_by("-total_point")
        )

        return teachers.distinct()


class GetUpdateDeleteTeacherView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update or delete teacher
    """

    queryset = Teacher.objects.all()
    model = Teacher
    serializer_class = serializers.TeacherSerializer


class CreateTeacherLevelApiView(generics.CreateAPIView):
    """
    Create teacher level
    """

    queryset = TeacherLevel.objects.all()
    model = TeacherLevel
    serializer_class = serializers.TeacherLevelSerializer


class GetUpdateDeleteTeacherLevelView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update or delete teacher level
    """

    queryset = TeacherLevel.objects.all()
    model = TeacherLevel
    serializer_class = serializers.TeacherLevelSerializer


class TeacherReportView(generics.RetrieveAPIView):
    """
    Get teacher report
    """

    queryset = Teacher.objects.all()
    model = Teacher

    def get(self, request, *args, **kwargs):
        year = date.today().year
        if self.request.GET.get("year"):
            year = self.request.GET.get("year")

        teacher = self.get_object()
        response = []
        for month in range(1, 13):
            point = 0
            for post in teacher.post_set.filter(date__month=month, date__year=year):
                point += post.category.coefficient
            response.append({"year": year, "month": month, "point": point})

        return Response(response, status=200)


class TeacherYearReport(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    model = Teacher

    def get(self, request, *args, **kwargs):

        teacher = self.get_object()
        response = {}
        response["academic_years"] = []
        response["group"] = []

        for group in Group.objects.all():
            response["group"].append(
                {"name": group.name, "category": [], "total_points": [], "id": group.id}
            )

            total_points = [0, 0, 0, 0, 0]
            for category in group.category_set.filter(post__teacher=teacher).distinct():
                points = []
                academic_years = AcademicYear.objects.all()[:5]
                for academic_year in reversed(academic_years):
                    response["academic_years"].append(academic_year.years)
                    points.append(
                        Post.objects.filter(
                            category=category,
                            teacher=teacher,
                            academic_years=academic_year,
                        ).count()
                        * category.coefficient
                    )

                if (
                    category.id == 29
                ):  # Если стартовый балл, то должен для каждого года считать стартовый балл
                    points = [max(points)] * len(points)
                total_points = map(sum, zip(total_points, points))

                response["group"][-1]["category"].append(
                    {
                        "name": category.name,
                        "points": points,
                    }
                )

            response["group"][-1]["total_points"] = total_points

        if ControlLimit.objects.last():
            response["low_line"] = ControlLimit.objects.last().low_limit
            response["high_line"] = ControlLimit.objects.last().high_limit
        return Response(response, status=200)


class AllYearReport(APIView):
    """
    Get all year report
    """

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        response = {}
        response["year"] = sorted(set(posts.values_list("date__year", flat=True)))
        response["academic_years"] = []
        response["group"] = []

        for group in Group.objects.all():
            response["group"].append(
                {"name": group.name, "category": [], "total_points": [], "id": group.id}
            )

            total_points = [0] * len(response["year"])
            for category in group.category_set.all():
                points = []
                academic_years = AcademicYear.objects.all()[:5]
                for academic_year in reversed(academic_years):
                    response["academic_years"].append(academic_year.years)
                    points.append(
                        Post.objects.filter(
                            category=category, academic_years=academic_year
                        ).count()
                        * category.coefficient
                    )

                if (
                    category.id == 29
                ):  # Если стартовый балл, то должен для каждого года считать стартовый балл
                    points = [max(points)] * len(points)
                total_points = map(sum, zip(total_points, points))

                response["group"][-1]["category"].append(
                    {
                        "name": category.name,
                        "points": points,
                    }
                )

            response["group"][-1]["total_points"] = total_points

        return Response(response, status=200)
