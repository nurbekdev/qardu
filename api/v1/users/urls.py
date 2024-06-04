from django.urls import path

from .views import (
    AllYearReport,
    CreateTeacherApiView,
    CreateTeacherLevelApiView,
    GetUpdateDeleteTeacherLevelView,
    GetUpdateDeleteTeacherView,
    TeacherListApiView,
    TeacherYearReport,
)

app_name = "api_user"

urlpatterns = [
    path("teachers/create/", CreateTeacherApiView.as_view(), name="teacher_create"),
    path(
        "teachers/<int:pk>",
        GetUpdateDeleteTeacherView.as_view(),
        name="teacher_get_update_delete",
    ),
    path("teachers/list/", TeacherListApiView.as_view(), name="teacher_list"),
    path(
        "teacher_levels/create/",
        CreateTeacherLevelApiView.as_view(),
        name="teacher_level_create",
    ),
    path(
        "teacher_levels/<int:pk>",
        GetUpdateDeleteTeacherLevelView.as_view(),
        name="teacher_level_get_update_delete",
    ),
    path(
        "teachers/<int:pk>/report/", TeacherYearReport.as_view(), name="teacher_report"
    ),
    path("total/report/", AllYearReport.as_view(), name="total_report"),
]
