from django.urls import path

from .views import DepartmentYearReport

app_name = "api_departments"

urlpatterns = [
    path("<int:pk>/report/", DepartmentYearReport.as_view(), name="report"),
]
