from django.contrib.auth.models import Group
from rest_framework import generics

from category.models import Category

from .serializers import CategoryReportSerializer, CategorySerializer, GroupSerializer


class CreateCategoryApiView(generics.CreateAPIView):
    queryset = Category.objects.all()
    model = Category
    serializer_class = CategorySerializer


class GetUpdateDeleteCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    model = Category
    serializer_class = CategorySerializer


class ReportCategoryView(generics.ListAPIView):
    queryset = Category.objects.exclude(id=29)  # TODO id 29 - стартовый бал фильтр
    serializer_class = CategoryReportSerializer


class ReportGroupyView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
