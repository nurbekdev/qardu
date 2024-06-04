from django.urls import path

from .views import (
    PostCreateView,
    PostDetailPublicView,
    PostListPublicView,
    PostOwnListPublicView,
    PostUpdateView,
)

app_name = "post_public"

urlpatterns = [
    path("list/", PostListPublicView.as_view(), name="list"),
    path("<int:pk>/", PostDetailPublicView.as_view(), name="detail"),
    path("mine/", PostOwnListPublicView.as_view(), name="my_list"),
    path("mine/create/", PostCreateView.as_view(), name="create"),
    path("mine/<int:pk>/update/", PostUpdateView.as_view(), name="update"),
]
