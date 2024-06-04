from datetime import date

from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.response import Response

from home.models import ControlLimit, Department
from posts.models import Post

from .serializers import DepartmentSerializer


class CreateDepartmentApiView(generics.CreateAPIView):
    queryset = Department.objects.all()
    model = Department
    serializer_class = DepartmentSerializer


class GetUpdateDeleteDepartmentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    model = Department
    serializer_class = DepartmentSerializer


class DepartmentReportView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    model = Department

    def get(self, request, *args, **kwargs):
        year = date.today().year
        if self.request.GET.get("year"):
            year = self.request.GET.get("year")

        response = []
        for month in range(1, 13):
            point = 0
            for post in Post.objects.filter(
                teacher__in=self.get_object().teacher_set.all(),
                date__month=month,
                date__year=year,
            ):
                point += post.category.coefficient
            response.append({"year": year, "month": month, "point": point})

        if ControlLimit.objects.last():
            # TODO refactor
            response["low_line"] = ControlLimit.objects.last().low_limit
            response["high_line"] = ControlLimit.objects.last().high_limit

        return Response(response, status=200)


class DepartmentYearReport(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    model = Department

    def get(self, request, *args, **kwargs):
        cur_year = date.today().year

        department = self.get_object()

        response = {}
        response["year"] = sorted(
            set(
                Post.objects.filter(teacher__department=department)
                .distinct()
                .values_list("date__year", flat=True)
            )
        )
        response["group"] = []

        if len(response["year"]) == 0:
            response["year"] = [cur_year]
        if len(response["year"]) < 5:
            for i in range(5 - len(response["year"])):
                response["year"].append(response["year"][-1] + 1)

            for group in Group.objects.all():
                response["group"].append(
                    {
                        "name": group.name,
                        "category": [],
                        "total_points": [],
                        "id": group.id,
                    }
                )
                total_points = [0] * len(response["year"])
                for category in group.category_set.filter(
                    post__teacher__department=department
                ).distinct():
                    points = []
                    for year in response["year"]:
                        date_from = date(year=year - 1, month=9, day=1)
                        date_to = date(year=year, month=8, day=31)

                        points.append(
                            Post.objects.filter(
                                category=category,
                                teacher__department=department,
                                date__gte=date_from,
                                date__lte=date_to,
                            )
                            .distinct()
                            .count()
                            * category.coefficient
                        )

                    total_points = map(sum, zip(total_points, points))
                    response["group"][-1]["category"].append(
                        {"name": category.name, "points": points}
                    )

                response["group"][-1]["total_points"] = total_points

        if ControlLimit.objects.last():
            response["low_line"] = ControlLimit.objects.last().low_limit
            response["high_line"] = ControlLimit.objects.last().high_limit

        return Response(response, status=200)
