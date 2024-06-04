from django.urls import path

from .views import (
    DepartmentPublicDetailView,
    DepartmentPublicListView,
    TeacherPublicDetailView,
    TeacherPublicListView,
)

app_name = "home_public"

urlpatterns = [
    path("teachers/", TeacherPublicListView.as_view(), name="teacher_list"),
    path(
        "teachers/<int:pk>/", TeacherPublicDetailView.as_view(), name="teacher_detail"
    ),
    path("departments/", DepartmentPublicListView.as_view(), name="department_list"),
    path(
        "departments/<int:pk>/",
        DepartmentPublicDetailView.as_view(),
        name="department_detail",
    ),
]
