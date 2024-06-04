from django.urls import path

from .views import (
    DepartmentAdminListView,
    TeacherAdminDetailView,
    TeacherAdminListView,
    TeacherLevelAdminListView,
)

app_name = "home_admin"

urlpatterns = [
    path(
        "departments/list/", DepartmentAdminListView.as_view(), name="department_list"
    ),
    path("teachers/list/", TeacherAdminListView.as_view(), name="teacher_list"),
    path("teachers/<int:pk>", TeacherAdminDetailView.as_view(), name="teacher_detail"),
    path(
        "teacher_levels/list/",
        TeacherLevelAdminListView.as_view(),
        name="teacher_level_list",
    ),
]
