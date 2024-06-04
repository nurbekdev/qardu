from datetime import date, datetime, timedelta

from django.contrib.auth.models import Group
from django.http import FileResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import get_permission_queryset
from posts.models import AcademicYear, Post
from posts.services import excel_teachers, excel_writer

from .paginations import MyLimitOffsetPagination
from .serializers import PostSerializer, PostStatisticSerializer


class CreatePostApiView(generics.CreateAPIView):
    """
    Create post
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class GetUpdateDeletePostView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, delete post
    """

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(
            category__in=get_permission_queryset(self.request.user)
        )


class PostListView(generics.ListAPIView):
    """
    List of posts
    """

    serializer_class = PostStatisticSerializer
    pagination_class = MyLimitOffsetPagination

    def get_queryset(self):
        return Post.objects.order_by("-id")


class PostReportView(APIView):
    """
    Get report for post
    """

    def get(self, request, *args, **kwargs):
        """
        Get report for post
        """
        academic_year = self.get_academic_year(request)
        groups = self.calculate_groups(academic_year)
        return Response(groups, status=200)

    def get_academic_year(self, request):
        """
        Get academic year
        """
        academic_id = request.GET.get("academic_year")
        if not academic_id and not str(academic_id).isnumeric():
            return AcademicYear.objects.last()

        today = date.today()
        academic_year_query = AcademicYear.objects.filter(
            from_date__lte=today, to_date__gte=today
        )
        return academic_year_query.filter(id=academic_id).last()

    def calculate_groups(self, academic_year):
        groups = []
        for group in Group.objects.all():
            total_point_list, total_minus_point_list = self.calculate_points_for_group(
                group, academic_year
            )
            groups.append(
                {
                    "group_name": group.name,
                    "total_points": total_point_list,
                    "id": group.id,
                }
            )
            if group.id == 3:  # Special handling for group id 3
                groups.append(
                    {
                        "group_name": group.name,
                        "total_points": total_minus_point_list,
                        "id": -3,
                    }
                )
        return groups

    def calculate_points_for_group(self, group, academic_year):
        from_date = academic_year.from_date
        to_date = academic_year.to_date
        total_point_list = []
        total_minus_point_list = []

        while from_date < to_date:
            point, minus_point = self.calculate_points_for_month(
                group, from_date, to_date
            )
            from_date = self.next_month(from_date, to_date)
            total_point_list.append(round(point, 1))
            total_minus_point_list.append(round(minus_point, 1))

        return total_point_list, total_minus_point_list

    def calculate_points_for_month(self, group, from_date, to_date):
        point = 0
        minus_point = 0
        next_month = self.next_month(from_date, to_date)

        posts = (
            Post.objects.filter(
                date__gte=from_date, date__lt=next_month, category__group=group
            ).distinct()
            if group.id == 3
            else Post.objects.filter(
                date__gte=from_date, date__lt=next_month, category__group=group
            )
        )

        for post in posts:
            coefficient = post.category.coefficient
            if coefficient > 0:
                point += coefficient
            else:
                minus_point -= coefficient

        return point if from_date.month >= 9 or point >= 0 else 0, minus_point

    def next_month(self, from_date, to_date):
        num_month = from_date.month
        next_month = date(from_date.year + (num_month // 12), ((num_month % 12) + 1), 1)
        return min(next_month, to_date + timedelta(days=1))


class ExportPosts(APIView):
    """
    Get posts in xlsx format
    """

    def get(self, request, *args, **kwargs):
        """
        Get posts in xlsx format for the last 3 days
        """
        to_date = datetime.now()
        from_date = to_date - timedelta(days=3)
        xlsx = excel_writer(from_date, to_date)
        return FileResponse(open(xlsx.filename, "rb"), as_attachment=True)


class ExportTeacherPosts(APIView):
    """
    Get teachers in xlsx format
    """

    def get(self, request, *args, **kwargs):
        academic_year = self.get_academic_year(request)
        xlsx = excel_teachers(
            years=academic_year.years,
            start_date=academic_year.from_date,
            end_date=academic_year.to_date,
            department=request.GET.get("department"),
            name=request.GET.get("name"),
            uuid=request.GET.get("uuid"),
            level=request.GET.get("level"),
            order_by=request.GET.get("order_by"),
        )
        return FileResponse(open(xlsx.filename, "rb"), as_attachment=True)

    def get_academic_year(self, request):
        academic_id = request.GET.get("academic_year")
        today = date.today()
        academic_year_query = AcademicYear.objects.filter(
            from_date__lte=today, to_date__gte=today
        )
        return (
            academic_year_query.filter(id=academic_id).last()
            if academic_id
            else academic_year_query.last()
        )
