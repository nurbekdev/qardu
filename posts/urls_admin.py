from django.urls import path

from .views import PostListAdminView, delete_post_view, post_create_update_view

app_name = "post_admin"

urlpatterns = [
    path("", PostListAdminView.as_view(), name="list"),
    path("create/", post_create_update_view, name="create"),
    path("update/<int:pk>/", post_create_update_view, name="update"),
    path("delete/<int:pk>/", delete_post_view, name="delete"),
]
