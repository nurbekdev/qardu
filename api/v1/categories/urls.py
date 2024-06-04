from django.urls import path

from .views import (
    CreateCategoryApiView,
    GetUpdateDeleteCategoryView,
    ReportCategoryView,
    ReportGroupyView,
)

app_name = "api_category"

urlpatterns = [
    path("create/", CreateCategoryApiView.as_view(), name="create"),
    path("<int:pk>/", GetUpdateDeleteCategoryView.as_view(), name="get_update_delete"),
    path("report/", ReportCategoryView.as_view(), name="report"),
    path("report/group/", ReportGroupyView.as_view(), name="report_group"),
]
