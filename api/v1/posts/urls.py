from django.urls import path

from .views import (
    CreatePostApiView,
    ExportPosts,
    ExportTeacherPosts,
    GetUpdateDeletePostView,
    PostListView,
    PostReportView,
)

app_name = "api_post"

urlpatterns = [
    path("create/", CreatePostApiView.as_view(), name="create"),
    path("<int:pk>", GetUpdateDeletePostView.as_view(), name="get_update_delete"),
    path("list/", PostListView.as_view(), name="list"),
    path("report/", PostReportView.as_view(), name="report"),
    path("export/", ExportPosts.as_view(), name="post_download_xlsx"),
    path(
        "export/teachers/", ExportTeacherPosts.as_view(), name="teacher_download_xlsx"
    ),
]
